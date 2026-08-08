from __future__ import annotations

import json
import os
from typing import Any

from backend.chat_schema import ToolCallLog
from backend.helpers.common import get_openai_client
from backend.helpers.result_summarizer import (
    first_string,
    summarize_tool_result,
    summarize_tool_result_with_llm,
)


def plain_value(value: object) -> object:
    if hasattr(value, "model_dump"):
        dumped = value.model_dump()  # type: ignore[no-any-return]
        if isinstance(dumped, dict) and "result" in dumped:
            return dumped["result"]
        return dumped
    if isinstance(value, (dict, list, str, int, float, bool)) or value is None:
        return value
    return str(value)


def _augment_arguments_from_result(
    tool_name: str,
    arguments: dict[str, object],
    previous_result: object | None,
) -> dict[str, object]:
    if previous_result is None:
        return dict(arguments)

    from backend.main import get_tool_spec

    tool_spec = get_tool_spec(tool_name)
    merged = dict(arguments)
    previous_plain = plain_value(previous_result)
    missing_required_fields = [
        field_name
        for field_name, field_info in tool_spec.args_model.model_fields.items()
        if field_info.is_required() and merged.get(field_name) in (None, "")
    ]

    if not missing_required_fields:
        return merged

    client = get_openai_client()
    if client is None:
        return merged

    try:
        field_schema = tool_spec.args_model.model_json_schema()
        response = client.responses.create(
            model=os.getenv("OPENAI_ARGUMENT_AUGMENTER_MODEL", "gpt-4.1-mini"),
            input=[
                {
                    "role": "system",
                    "content": (
                        "Fill missing required tool arguments from previous tool result. "
                        "Return JSON only: {\"arguments\": {...}}. "
                        "Use only keys that exist in the schema. "
                        "If value is unknown, omit the key."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "tool_name": tool_name,
                            "current_arguments": merged,
                            "missing_required_fields": missing_required_fields,
                            "tool_schema": field_schema,
                            "previous_result": previous_plain,
                        }
                    ),
                },
            ],
        )
        raw = getattr(response, "output_text", "")
        data = json.loads(raw)
        if not isinstance(data, dict):
            return merged

        llm_args = data.get("arguments", {})
        if not isinstance(llm_args, dict):
            return merged

        allowed_fields = set(tool_spec.args_model.model_fields.keys())
        for key, value in llm_args.items():
            if key in allowed_fields and merged.get(key) in (None, ""):
                merged[key] = value
    except Exception:
        return merged

    return merged


def _invoke_tool_with_chain(
    tool_name: str,
    arguments: dict[str, object],
    previous_result: object | None,
) -> tuple[object | None, str | None, object | None, dict[str, object]]:
    from backend.main import get_tool_spec

    tool_spec = get_tool_spec(tool_name)
    merged_arguments = _augment_arguments_from_result(tool_name, arguments, previous_result)

    try:
        tool_result = tool_spec.invoke(**merged_arguments)
        plain = plain_value(tool_result)
        return plain, None, plain, merged_arguments
    except Exception as exc:
        if merged_arguments != arguments:
            try:
                tool_result = tool_spec.invoke(**arguments)
                plain = plain_value(tool_result)
                return plain, None, plain, arguments
            except Exception as retry_exc:
                return None, str(retry_exc), previous_result, arguments

        return None, str(exc), previous_result, merged_arguments


def _friendly_tool_error(error: str) -> str:
    lowered = error.lower()

    if "extra inputs are not permitted" in lowered:
        return "I could not run that tool because some request fields were not supported."

    if "is required" in lowered:
        return "I am missing required information for that step. Please provide more details."

    return "I could not complete that step due to a tool error."


def _is_recoverable_tool_error(tool_name: str, error: str) -> bool:
    lowered = error.lower()
    return tool_name == "slack_send_message" and "unknown slack channel or dm" in lowered


class ToolExecutionRecorder:
    """Owns tool-call state and response snippets for a single chat turn."""

    def __init__(self, user_query: str) -> None:
        self.tool_calls: list[ToolCallLog] = []
        self.assistant_parts: list[str] = []
        self.previous_result: object | None = None
        self.user_query = user_query

    def record_tool_call(self, tool_name: str, arguments: dict[str, object]) -> bool:
        tool_result, error, next_previous_result, used_arguments = _invoke_tool_with_chain(
            tool_name,
            arguments,
            self.previous_result,
        )
        self.tool_calls.append(
            ToolCallLog(
                name=tool_name,
                arguments=used_arguments,
                result=tool_result,
                error=error,
            )
        )
        self.previous_result = next_previous_result

        if error is None:
            llm_summary = summarize_tool_result_with_llm(
                tool_name=tool_name,
                user_query=self.user_query,
                tool_result=tool_result,
            )
            if llm_summary:
                self.assistant_parts.append(llm_summary)
                return True

            structured_summary = summarize_tool_result(tool_name, tool_result)
            if structured_summary:
                self.assistant_parts.append(structured_summary)
                return True

            if isinstance(tool_result, dict):
                summary = first_string(tool_result)
                if summary:
                    self.assistant_parts.append(summary)
                    return True

            self.assistant_parts.append(f"Used {tool_name}.")
            return True

        if _is_recoverable_tool_error(tool_name, error):
            self.assistant_parts.append(
                "I could not resolve that Slack destination yet, so I will look it up first."
            )
            return True

        self.assistant_parts.append(_friendly_tool_error(error))
        return False
