from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from backend.helpers.common import Service, get_openai_client

_DOCS_DIR = Path(__file__).resolve().parents[2] / "docs" / "mcp_tool_definitions"

_SERVICE_DOC_FILES: dict[Service, str] = {
    "gmail": "gmail.md",
    "googlecalendar": "google-calendar.md",
    "googledrive": "google-drive.md",
    "slack": "slack.md",
    "linear": "linear.md",
    "github": "github.md",
    "perplexity": "perplexity.md",
}

_ARG_CRAFTER_PROMPT = """
You map a user request to arguments for a specific tool.

Return JSON only with this shape:
{
  "arguments": {"param": "value"}
}

Rules:
- Use only parameters from allowed_params.
- Include required_params whenever they can be inferred from the query/context.
- If a value is unknown, omit it instead of guessing.
- Do not include explanation text.
""".strip()


def _tool_schema_from_docs(service: Service, tool_name: str) -> tuple[set[str], set[str]]:
    """Return (all_params, required_params) for a tool from split MCP docs."""
    path = _DOCS_DIR / _SERVICE_DOC_FILES[service]
    if not path.exists():
        return set(), set()

    all_params: set[str] = set()
    required_params: set[str] = set()
    in_tool = False
    in_params = False

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        if stripped == tool_name:
            in_tool = True
            in_params = False
            continue

        if in_tool and stripped and not line.startswith(" ") and stripped != tool_name:
            break

        if not in_tool:
            continue

        if stripped.startswith("Parameters:"):
            in_params = True
            continue

        if in_params and stripped.startswith("-"):
            match = re.match(r"-\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)", stripped)
            if not match:
                continue
            param = match.group(1)
            meta = match.group(2).lower()
            all_params.add(param)
            if "required" in meta:
                required_params.add(param)

        if in_params and stripped.startswith("==="):
            break

    return all_params, required_params


def _filter_to_known_params(args: dict[str, Any], allowed_params: set[str]) -> dict[str, Any]:
    if not allowed_params:
        return args
    return {key: value for key, value in args.items() if key in allowed_params}


def _camel_to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _normalize_arg_keys(args: dict[str, Any], allowed_params: set[str]) -> dict[str, Any]:
    """Normalize LLM keys (e.g., maxResults -> max_results) and keep only allowed params."""
    normalized: dict[str, Any] = {}
    for key, value in args.items():
        if key in allowed_params:
            normalized[key] = value
            continue

        snake_key = _camel_to_snake(key)
        if snake_key in allowed_params:
            normalized[snake_key] = value
            continue

        lowered_key = key.lower()
        if lowered_key in allowed_params:
            normalized[lowered_key] = value
            continue

    return normalized


def _tool_schema_from_runtime(tool_name: str) -> tuple[set[str], set[str]]:
    """Fallback schema from ToolSpec when docs parsing is unavailable."""
    try:
        from backend.main import get_tool_spec

        spec = get_tool_spec(tool_name)
        fields = spec.args_model.model_fields
        allowed = set(fields.keys())
        required = {name for name, info in fields.items() if info.is_required()}
        return allowed, required
    except Exception:
        return set(), set()


def _coerce_value_to_runtime_field(tool_name: str, key: str, value: Any) -> Any:
    try:
        from backend.main import get_tool_spec

        spec = get_tool_spec(tool_name)
        field = spec.args_model.model_fields.get(key)
        if field is None:
            return value

        annotation = field.annotation
        origin = getattr(annotation, "__origin__", None)

        if annotation is str and isinstance(value, list):
            items = [str(item).strip() for item in value if str(item).strip()]
            return ",".join(items)

        if origin is list and isinstance(value, str):
            parts = [item.strip() for item in value.split(",") if item.strip()]
            return parts if parts else [value]
    except Exception:
        return value

    return value


def _coerce_argument_values(tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
    coerced: dict[str, Any] = {}
    for key, value in args.items():
        coerced[key] = _coerce_value_to_runtime_field(tool_name, key, value)
    return coerced


def _craft_args_with_llm(
    *,
    tool_name: str,
    service: Service,
    query: str,
    allowed_params: set[str],
    required_params: set[str],
    context: dict[str, Any],
) -> dict[str, Any] | None:
    client = get_openai_client()
    if client is None:
        return None

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_ARGUMENT_CRAFTER_MODEL", "gpt-4.1-mini"),
            input=[
                {"role": "system", "content": _ARG_CRAFTER_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "service": service,
                            "tool_name": tool_name,
                            "query": query,
                            "allowed_params": sorted(allowed_params),
                            "required_params": sorted(required_params),
                            "context": context,
                        }
                    ),
                },
            ],
        )
        raw = getattr(response, "output_text", "")
        data = json.loads(raw)
        if not isinstance(data, dict):
            return None
        args = data.get("arguments", {})
        if not isinstance(args, dict):
            return None
        return _normalize_arg_keys(args, allowed_params)
    except Exception:
        return None


def _postprocess_arguments(
    *,
    tool_name: str,
    query: str,
    args: dict[str, Any],
) -> dict[str, Any]:
    """Apply minimal safety defaults after LLM argument generation."""
    if tool_name == "GMAIL_FETCH_EMAILS":
        # Prefer content-rich payloads so downstream summarization has text to use.
        args.setdefault("include_payload", True)
        args.setdefault("verbose", True)
        if args.get("ids_only") is True:
            args["ids_only"] = False

        lowered = query.lower()
        if "most recent" in lowered or "latest" in lowered:
            args.setdefault("max_results", 1)

    return args


def craft_tool_arguments(
    tool_name: str,
    query: str,
    service: Service,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Craft tool arguments using LLM only, constrained by MCP docs schema."""
    base_context = dict(context or {})
    docs_allowed, docs_required = _tool_schema_from_docs(service, tool_name)
    runtime_allowed, runtime_required = _tool_schema_from_runtime(tool_name)

    if docs_allowed and runtime_allowed:
        allowed_params = docs_allowed & runtime_allowed
        required_params = docs_required & runtime_required
    elif docs_allowed:
        allowed_params = docs_allowed
        required_params = docs_required
    else:
        allowed_params = runtime_allowed
        required_params = runtime_required

    llm_args = _craft_args_with_llm(
        tool_name=tool_name,
        service=service,
        query=query,
        allowed_params=allowed_params,
        required_params=required_params,
        context=base_context,
    )

    if llm_args is None:
        normalized = _normalize_arg_keys(base_context, allowed_params)
        normalized = _coerce_argument_values(tool_name, normalized)
        postprocessed = _postprocess_arguments(
            tool_name=tool_name,
            query=query,
            args=normalized,
        )
        return _coerce_argument_values(
            tool_name,
            _normalize_arg_keys(postprocessed, allowed_params),
        )

    merged = dict(base_context)
    merged.update(llm_args)
    normalized = _normalize_arg_keys(merged, allowed_params)
    normalized = _coerce_argument_values(tool_name, normalized)
    postprocessed = _postprocess_arguments(
        tool_name=tool_name,
        query=query,
        args=normalized,
    )
    return _coerce_argument_values(
        tool_name,
        _normalize_arg_keys(postprocessed, allowed_params),
    )
