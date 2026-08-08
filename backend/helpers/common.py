from __future__ import annotations

import os
from typing import Any, Literal, TypeAlias

Service: TypeAlias = Literal[
    "gmail",
    "googlecalendar",
    "googledrive",
    "slack",
    "linear",
    "github",
    "perplexity",
]


def get_openai_client() -> Any | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
    except Exception:
        return None
    return OpenAI(api_key=api_key)
