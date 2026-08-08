from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from backend.helpers.common import Service, get_openai_client


@dataclass(frozen=True)
class CapabilityAssessment:
    supported: bool
    should_execute: bool = True
    reason: str | None = None


def _tool_catalog_for_service(tool_names: list[str]) -> list[dict[str, str]]:
    from backend.main import get_tool_spec

    catalog: list[dict[str, str]] = []
    for name in tool_names:
        try:
            spec = get_tool_spec(name)
            catalog.append(
                {
                    "name": name,
                    "description": spec.description,
                    "docstring": spec.docstring,
                }
            )
        except Exception:
            continue
    return catalog


_CAPABILITY_PROMPT = """
You are checking whether a user request can be completed with the provided tools.

Return JSON only:
{
  "supported": true|false,
    "should_execute": true|false,
  "reason": "short user-facing explanation"
}

Rules:
- If the request is possible with one or more listed tools, supported=true.
- If impossible with listed tools, supported=false and explain what capability is missing.
- For all services: if the latest user request is a question-style request without explicit action intent
  (for example asks "what/how/which" and does not ask to send/post/create/update/delete/reply),
    return supported=true, should_execute=false, with a reason answering capability and asking for an explicit action.
- For capability/intention questions (for example "can you send message on slack?", "are you able to post?"),
    return supported=true, should_execute=false, so no tool action is executed yet and respond truthfully and politely.
- Only return should_execute=true when the user is explicitly asking to perform the action now.
- Be concise and factual.
""".strip()


def _extract_latest_user_request(user_query: str) -> str:
    marker = "Latest user request:"
    if marker in user_query:
        return user_query.split(marker, 1)[1].strip()
    return user_query.strip()


def _is_explicit_slack_send_intent(text: str) -> bool:
    lowered = text.lower()
    # Covers prompts like "send as slack message", "notify", "dm", "post to slack".
    return bool(
        re.search(
            r"\b(send|post|notify|message|dm|direct message|slack message)\b",
            lowered,
        )
    ) and ("slack" in lowered or "dm" in lowered or "direct message" in lowered)


def _has_explicit_action_intent(text: str) -> bool:
    lowered = text.lower()
    return bool(
        re.search(
            r"\b(send|post|notify|create|update|delete|remove|reply|schedule|move|copy|share|attach|draft|search|find|list|get|fetch)\b",
            lowered,
        )
    )


def _looks_like_capability_question(text: str) -> bool:
    lowered = text.lower().strip()
    return bool(
        re.search(
            r"^(can you|are you able|do you support|is it possible|what can you|which tools)",
            lowered,
        )
    )


def assess_request_capability(
    service: Service,
    user_query: str,
    tool_names: list[str],
) -> CapabilityAssessment:
    latest_request = _extract_latest_user_request(user_query)

    if tool_names and _has_explicit_action_intent(latest_request) and not _looks_like_capability_question(latest_request):
        # Permissive mode: prefer execution over false "unsupported" negatives.
        return CapabilityAssessment(supported=True, should_execute=True)

    # Deterministic override for explicit Slack-send actions to avoid LLM false negatives.
    if (
        service == "slack"
        and "slack_send_message" in tool_names
        and _is_explicit_slack_send_intent(latest_request)
    ):
        return CapabilityAssessment(supported=True, should_execute=True)

    client = get_openai_client()
    if client is None:
        return CapabilityAssessment(supported=True)

    catalog = _tool_catalog_for_service(tool_names)

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_CAPABILITY_MODEL", "gpt-4.1-mini"),
            input=[
                {"role": "system", "content": _CAPABILITY_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "service": service,
                            "query": user_query,
                            "latest_user_request": latest_request,
                            "tools": catalog,
                        }
                    ),
                },
            ],
        )
        raw = getattr(response, "output_text", "")
        data = json.loads(raw)
        if not isinstance(data, dict):
            return CapabilityAssessment(supported=True)

        supported = bool(data.get("supported", True))
        should_execute = bool(data.get("should_execute", supported))
        reason = data.get("reason")
        if isinstance(reason, str):
            reason = reason.strip() or None
        else:
            reason = None
        if not supported:
            # Keep the gate weak: if there are tools and this looks like an
            # action request, treat as executable and let runtime/tool errors
            # provide the final guardrail.
            if tool_names and _has_explicit_action_intent(latest_request) and not _looks_like_capability_question(latest_request):
                supported = True
                should_execute = True
            else:
                should_execute = False
        return CapabilityAssessment(
            supported=supported,
            should_execute=should_execute,
            reason=reason,
        )
    except Exception:
        return CapabilityAssessment(supported=True)
