from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any
from backend.helpers.common import Service, get_openai_client


@dataclass(frozen=True)
class ClassifiedService:
    service: Service
    confidence: float = 1.0


@dataclass(frozen=True)
class ClassifiedServices:
    services: list[Service]
    confidence: float = 1.0


@dataclass(frozen=True)
class Ambiguous:
    question: str
    candidates: list[Service]


ClassifierResult = ClassifiedService | ClassifiedServices | Ambiguous

_SERVICES: tuple[Service, ...] = (
    "gmail",
    "googlecalendar",
    "googledrive",
    "slack",
    "linear",
    "github",
    "perplexity",
)

def _default_ambiguous() -> Ambiguous:
    return Ambiguous(
        question="Which service should I use?",
        candidates=list(_SERVICES),
    )


CLASSIFIER_SYSTEM_PROMPT = """
You are a strict router for a multi-tool assistant.

Classify the user's request into one of these service buckets:
gmail, googlecalendar, googledrive, slack, linear, github, perplexity.

Rules:
- If the prompt clearly needs exactly one service, return {"type": "classified", "service": "...", "confidence": 0.0-1.0}.
- If the prompt clearly needs multiple services, return {"type": "classified_many", "services": ["..."], "confidence": 0.0-1.0}.
- If the prompt is underspecified or genuinely ambiguous, return {"type": "ambiguous", "question": "...", "candidates": ["..."]}.

Do not answer the user's request.
Return only valid JSON.
""".strip()


CLARIFYING_QUESTION_SYSTEM_PROMPT = """
You rewrite clarifying questions for a multi-tool assistant.

Rules:
- Ask exactly one short question.
- Keep it under 25 words.
- Mention candidate services naturally when provided.
- Do not answer the original request.
- Return only JSON: {"question":"..."}
""".strip()


def _parse_llm_result(data: dict[str, Any]) -> ClassifierResult:
    result_type = data.get("type")
    if result_type == "classified":
        service = data.get("service")
        if service in _SERVICES:
            return ClassifiedService(service=service, confidence=float(data.get("confidence", 1.0)))

    if result_type == "classified_many":
        services = [service for service in data.get("services", []) if service in _SERVICES]
        if services:
            return ClassifiedServices(services=services, confidence=float(data.get("confidence", 1.0)))

    candidates = [service for service in data.get("candidates", []) if service in _SERVICES]
    return Ambiguous(
        question=str(data.get("question", "Which service should I use?")),
        candidates=candidates or list(_SERVICES),
    )


def classify_with_llm(text: str) -> ClassifierResult:
    client = get_openai_client()
    if client is None:
        return _default_ambiguous()
    try:
        response = client.responses.create(
            model= os.getenv("OPENAI_CLASSIFIER_MODEL", "gpt-4.1-mini"),
            input=[
                {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        )
        raw = getattr(response, "output_text", "")
        data = json.loads(raw)
        if isinstance(data, dict):
            return _parse_llm_result(data)
    except Exception:
        pass

    return _default_ambiguous()


def classify_service(text: str, *, prefer_llm: bool = True) -> ClassifierResult:
    if prefer_llm:
        return classify_with_llm(text)
    return _default_ambiguous()


def generate_clarifying_question(
    user_text: str,
    fallback_question: str,
    candidates: list[Service],
) -> str:
    """Generate a concise, user-friendly clarifying question.

    Falls back to the caller-provided question if OpenAI is unavailable
    or the model output is malformed.
    """
    client = get_openai_client()
    if client is None:
        return fallback_question

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_CLASSIFIER_MODEL", "gpt-4.1-mini"),
            input=[
                {"role": "system", "content": CLARIFYING_QUESTION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "user_request": user_text,
                            "fallback_question": fallback_question,
                            "candidates": candidates,
                        }
                    ),
                },
            ],
        )
        raw = getattr(response, "output_text", "")
        data = json.loads(raw)
        if isinstance(data, dict):
            question = data.get("question")
            if isinstance(question, str) and question.strip():
                return question.strip()
    except Exception:
        pass

    return fallback_question