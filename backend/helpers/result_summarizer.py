from __future__ import annotations

import base64
import json
import os
import re
from typing import Any

from backend.helpers.common import get_openai_client


def first_string(value: object) -> str | None:
    if isinstance(value, str):
        cleaned = value.strip()
        return cleaned or None

    if isinstance(value, dict):
        for item in value.values():
            nested = first_string(item)
            if nested:
                return nested

    if isinstance(value, list):
        for item in value:
            nested = first_string(item)
            if nested:
                return nested

    return None


def _short_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _looks_like_base64(value: str) -> bool:
    text = value.strip()
    if len(text) < 24:
        return False
    if len(text) % 4 != 0:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9+/=\-_]+", text))


def _decode_if_base64(value: str) -> str:
    if not _looks_like_base64(value):
        return value

    normalized = value.replace("-", "+").replace("_", "/")
    try:
        raw = base64.b64decode(normalized, validate=False)
        decoded = raw.decode("utf-8", errors="strict").strip()
        if decoded and all(ch == "\n" or ch == "\r" or ch == "\t" or 32 <= ord(ch) <= 126 for ch in decoded):
            return decoded
    except Exception:
        return value
    return value


def _collect_text_hints(value: object, prefix: str = "", limit: int = 120) -> list[str]:
    hints: list[str] = []

    if isinstance(value, dict):
        for key, nested in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(nested, str):
                decoded = _decode_if_base64(nested)
                cleaned = decoded.strip()
                if cleaned:
                    hints.append(f"{path}: {cleaned[:280]}")
            elif isinstance(nested, (int, float, bool)):
                hints.append(f"{path}: {nested}")
            elif isinstance(nested, (dict, list)):
                hints.extend(_collect_text_hints(nested, path, limit=limit))
            if len(hints) >= limit:
                return hints[:limit]
        return hints

    if isinstance(value, list):
        for idx, nested in enumerate(value):
            path = f"{prefix}[{idx}]" if prefix else f"[{idx}]"
            if isinstance(nested, str):
                decoded = _decode_if_base64(nested)
                cleaned = decoded.strip()
                if cleaned:
                    hints.append(f"{path}: {cleaned[:280]}")
            elif isinstance(nested, (int, float, bool)):
                hints.append(f"{path}: {nested}")
            elif isinstance(nested, (dict, list)):
                hints.extend(_collect_text_hints(nested, path, limit=limit))
            if len(hints) >= limit:
                return hints[:limit]
        return hints

    if isinstance(value, str):
        cleaned = _decode_if_base64(value).strip()
        if cleaned:
            hints.append(f"{prefix or 'value'}: {cleaned[:280]}")
    elif isinstance(value, (int, float, bool)):
        hints.append(f"{prefix or 'value'}: {value}")

    return hints[:limit]


def _item_label(item: object) -> str:
    if isinstance(item, dict):
        nested = first_string(item)
        if nested:
            return nested
        return _short_json(item)
    if isinstance(item, str):
        return item.strip()
    return _short_json(item)


def summarize_tool_result(tool_name: str, tool_result: object | None) -> str | None:
    if tool_result is None:
        return None

    if isinstance(tool_result, (str, int, float, bool)):
        return str(tool_result)

    if isinstance(tool_result, list):
        if not tool_result:
            return f"{tool_name} returned no items."
        labels = [_item_label(item) for item in tool_result]
        if len(labels) > 20:
            shown = ", ".join(labels[:20])
            return f"{tool_name} returned {len(labels)} items: {shown}, and {len(labels) - 20} more."
        return f"{tool_name} returned {len(labels)} items: {', '.join(labels)}."

    if isinstance(tool_result, dict):
        parts: list[str] = []
        for key, value in tool_result.items():
            if isinstance(value, list):
                if not value:
                    parts.append(f"{key}: none")
                    continue
                labels = [_item_label(item) for item in value]
                if len(labels) > 20:
                    shown = ", ".join(labels[:20])
                    parts.append(f"{key} ({len(labels)}): {shown}, and {len(labels) - 20} more")
                else:
                    parts.append(f"{key} ({len(labels)}): {', '.join(labels)}")
            elif isinstance(value, dict):
                parts.append(f"{key}: {_short_json(value)}")
            else:
                parts.append(f"{key}: {value}")

        if parts:
            return "; ".join(parts)

    return None


_LLM_SUMMARY_PROMPT = """
You summarize tool results for users.

Rules:
- Answer the user's request directly using the tool result.
- Keep only relevant fields.
- If the user asks for content/body/value, prioritize readable message text.
- Prefer human-readable values over IDs unless IDs are explicitly requested.
- Keep it concise (1-4 sentences or a short bullet list).
- Do not invent facts.

Return JSON only:
{
  "summary": "..."
}
""".strip()


def summarize_tool_result_with_llm(
    *,
    tool_name: str,
    user_query: str,
    tool_result: object | None,
) -> str | None:
    if tool_result is None:
        return None

    client = get_openai_client()
    if client is None:
        return None

    try:
        raw_json = json.dumps(tool_result, ensure_ascii=False)
    except Exception:
        raw_json = str(tool_result)

    if len(raw_json) > 8000:
        raw_json = raw_json[:8000] + "..."

    text_hints = _collect_text_hints(tool_result)
    if len(text_hints) > 80:
        text_hints = text_hints[:80]

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini"),
            input=[
                {"role": "system", "content": _LLM_SUMMARY_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "user_query": user_query,
                            "tool_name": tool_name,
                            "result_text_hints": text_hints,
                            "result_json": raw_json,
                        }
                    ),
                },
            ],
        )
        raw = getattr(response, "output_text", "")
        data = json.loads(raw)
        if not isinstance(data, dict):
            return None
        summary = data.get("summary")
        if isinstance(summary, str) and summary.strip():
            return summary.strip()
        return None
    except Exception:
        return None
