from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any

from backend.helpers.argument_crafter import craft_tool_arguments
from backend.helpers.common import Service, get_openai_client
from backend.helpers.tool_catalog import runtime_tools_for_service, tool_context_for_service


@dataclass(frozen=True)
class ResolvedTool:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class LLMResolvedTool:
    service: Service
    tool: str
    arguments: dict[str, Any]


LLM_TOOL_SELECTION_PROMPT = """
You are selecting exactly one tool for a single service bucket.

Return valid JSON only with this shape:
{
  "service": "gmail|googlecalendar|googledrive|slack|linear|github|perplexity",
  "tool": "exact tool name from the allowed list",
  "arguments": {"...": "..."}
}

Rules:
- Use only one tool.
- The tool name must be one of the allowed tools.
- The arguments object must include only fields that tool accepts.
- Fill required arguments from the user's query when possible.
- If a required argument is missing, still return the best partial arguments you can infer.
- For Slack destinations: channel names usually use # and DMs usually use @ or words like "DM" / "direct message".
- If destination ID is missing for an action like send/history/thread, prefer an ID-discovery tool first.
- Do not add commentary or markdown.
""".strip()


LLM_FOLLOW_UP_TOOL_PROMPT = """
You are deciding the next tool step for a single service after seeing prior tool call results.

Return valid JSON only with one of these shapes:
{
    "done": true
}

or

{
    "done": false,
    "tool": "exact tool name from allowed tools",
    "arguments": {"...": "..."}
}

Rules:
- Use done=true when the user's request is already satisfied for this service.
- Use done=false only if another tool call is genuinely needed.
- The tool must be from the allowed tools list.
- Include only parameters accepted by that tool.
- Prefer using IDs or keys returned from earlier tool results when follow-up detail is needed.
- For Slack send/history/thread actions, convert destination names to conversation IDs via discovery before final action.
- Do not add commentary or markdown.
""".strip()


def _allowed_tools_for_service(service: Service) -> list[str]:
    return runtime_tools_for_service(service)


def _looks_like_slack_conversation_id(value: str) -> bool:
    return bool(re.fullmatch(r"[CDG][A-Za-z0-9]+", value.strip()))


def _choose_slack_discovery_tool(
    *,
    query: str,
    channel: str,
    allowed_tools: list[str],
) -> ResolvedTool | None:
    lowered_query = query.lower()
    lowered_channel = channel.lower()
    wants_dm_lookup = (
        channel.strip().startswith("@")
        or "direct message" in lowered_query
        or " dm " in f" {lowered_query} "
        or "@" in lowered_channel
    )

    if wants_dm_lookup and "slack_list_users" in allowed_tools:
        return ResolvedTool(name="slack_list_users", arguments={})

    if "slack_list_conversations" in allowed_tools:
        return ResolvedTool(name="slack_list_conversations", arguments={})

    if "slack_list_users" in allowed_tools:
        return ResolvedTool(name="slack_list_users", arguments={})

    return None


def _slack_preflight_resolution(
    *,
    service: Service,
    tool_name: str,
    arguments: dict[str, Any],
    query: str,
    allowed_tools: list[str],
) -> ResolvedTool | None:
    if service != "slack":
        return None

    if tool_name not in {
        "slack_send_message",
        "slack_conversations_history",
        "slack_get_thread",
        "slack_get_full_conversation",
    }:
        return None

    channel = arguments.get("channel")
    if not isinstance(channel, str) or not channel.strip():
        return None

    if _looks_like_slack_conversation_id(channel):
        return None

    return _choose_slack_discovery_tool(
        query=query,
        channel=channel,
        allowed_tools=allowed_tools,
    )


def _parse_llm_tool_resolution(
    service: Service, data: dict[str, Any]
) -> LLMResolvedTool | None:
    tool_name = data.get("tool")
    if not isinstance(tool_name, str):
        return None

    allowed_tools = set(_allowed_tools_for_service(service))
    if tool_name not in allowed_tools:
        return None

    arguments = data.get("arguments", {})
    if not isinstance(arguments, dict):
        arguments = {}

    return LLMResolvedTool(service=service, tool=tool_name, arguments=arguments)


def _compact_history_for_llm(tool_history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compacted: list[dict[str, Any]] = []
    for row in tool_history[-6:]:
        name = row.get("name")
        arguments = row.get("arguments", {})
        result = row.get("result")
        error = row.get("error")

        try:
            compact_result = json.dumps(result, ensure_ascii=False)
        except Exception:
            compact_result = str(result)

        if len(compact_result) > 4000:
            compact_result = compact_result[:4000] + "..."

        compacted.append(
            {
                "name": name,
                "arguments": arguments,
                "result": compact_result,
                "error": error,
            }
        )
    return compacted


def resolve_tool_with_llm(service: Service, query: str) -> LLMResolvedTool | None:
    client = get_openai_client()
    if client is None:
        return None

    allowed_tools = _allowed_tools_for_service(service)
    if not allowed_tools:
        return None

    allowed_tool_context = tool_context_for_service(service)

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_TOOL_SELECTOR_MODEL", "gpt-4.1-mini"),
            input=[
                {
                    "role": "system",
                    "content": LLM_TOOL_SELECTION_PROMPT
                    + "\n\nAllowed service: "
                    + service
                    + "\nAllowed tools: "
                    + ", ".join(allowed_tools),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "query": query,
                            "allowed_tool_definitions": allowed_tool_context,
                        }
                    ),
                },
            ],
        )
        raw = getattr(response, "output_text", "")
        data = json.loads(raw)
        if isinstance(data, dict):
            parsed = _parse_llm_tool_resolution(service, data)
            if parsed is not None:
                return parsed
    except Exception:
        return None

    return None


def resolve_follow_up_tool_with_llm(
    service: Service,
    query: str,
    tool_history: list[dict[str, Any]],
) -> ResolvedTool | None:
    client = get_openai_client()
    if client is None:
        return None

    allowed_tools = _allowed_tools_for_service(service)
    if not allowed_tools:
        return None

    compact_history = _compact_history_for_llm(tool_history)
    allowed_tool_context = tool_context_for_service(service)

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_TOOL_SELECTOR_MODEL", "gpt-4.1-mini"),
            input=[
                {
                    "role": "system",
                    "content": LLM_FOLLOW_UP_TOOL_PROMPT
                    + "\n\nAllowed service: "
                    + service
                    + "\nAllowed tools: "
                    + ", ".join(allowed_tools),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "query": query,
                            "tool_history": compact_history,
                            "allowed_tool_definitions": allowed_tool_context,
                        }
                    ),
                },
            ],
        )
        raw = getattr(response, "output_text", "")
        data = json.loads(raw)
        if not isinstance(data, dict):
            return None

        if bool(data.get("done", False)):
            return None

        parsed = _parse_llm_tool_resolution(service, data)
        if parsed is None:
            return None

        normalized_args = craft_tool_arguments(
            tool_name=parsed.tool,
            query=query,
            service=service,
            context={
                "llm_arguments": parsed.arguments,
                "tool_history": compact_history,
            },
        )
        preflight = _slack_preflight_resolution(
            service=service,
            tool_name=parsed.tool,
            arguments=normalized_args,
            query=query,
            allowed_tools=allowed_tools,
        )
        if preflight is not None:
            return preflight

        return ResolvedTool(name=parsed.tool, arguments=normalized_args)
    except Exception:
        return None


def tools_for_service(service: Service) -> list[str]:
    return _allowed_tools_for_service(service)


def tools_for_services(services: list[Service]) -> list[str]:
    tool_names: list[str] = []
    seen: set[str] = set()
    for service in services:
        for tool_name in tools_for_service(service):
            if tool_name not in seen:
                seen.add(tool_name)
                tool_names.append(tool_name)
    return tool_names


def resolve_tool_for_service(service: Service, query: str) -> ResolvedTool:
    allowed = _allowed_tools_for_service(service)

    llm_resolution = resolve_tool_with_llm(service, query)
    if llm_resolution is not None:
        normalized_args = craft_tool_arguments(
            tool_name=llm_resolution.tool,
            query=query,
            service=service,
            context=llm_resolution.arguments,
        )
        preflight = _slack_preflight_resolution(
            service=service,
            tool_name=llm_resolution.tool,
            arguments=normalized_args,
            query=query,
            allowed_tools=allowed,
        )
        if preflight is not None:
            return preflight

        return ResolvedTool(name=llm_resolution.tool, arguments=normalized_args)

    if not allowed:
        raise ValueError(f"No tools available for service: {service}")

    tool_name = allowed[0]
    arguments = craft_tool_arguments(tool_name=tool_name, query=query, service=service)
    preflight = _slack_preflight_resolution(
        service=service,
        tool_name=tool_name,
        arguments=arguments,
        query=query,
        allowed_tools=allowed,
    )
    if preflight is not None:
        return preflight

    return ResolvedTool(name=tool_name, arguments=arguments)


def resolve_tools_for_services(services: list[Service], query: str) -> list[ResolvedTool]:
    return [resolve_tool_for_service(service, query) for service in services]
