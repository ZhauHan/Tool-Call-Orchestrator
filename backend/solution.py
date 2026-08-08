from __future__ import annotations

import json
import os

from backend.chat_schema import ChatMessage, ChatRequest, ChatResponse
from backend.helpers.chat_execution import ToolExecutionRecorder
from backend.helpers.service_classifier import (
    Ambiguous,
    ClassifiedService,
    ClassifiedServices,
    classify_service,
    generate_clarifying_question,
)
from backend.helpers.tool_given_service import (
    ResolvedTool,
    resolve_follow_up_tool_with_llm,
    resolve_tool_for_service,
    resolve_tools_for_services,
    tools_for_service,
)


def chat(request: ChatRequest) -> ChatResponse:
    """Entry point for POST /chat."""
    last_message = request.messages[-1]
    latest_user_content = next(
        (message.content for message in reversed(request.messages) if message.role == "user"),
        last_message.content,
    )
    conversation_context = "\n".join(
        f"{message.role}: {message.content}" for message in request.messages
    )
    routing_context = (
        f"Conversation history:\n{conversation_context}\n\n"
        f"Latest user request:\n{latest_user_content}"
    )

    history_window = int(os.getenv("CHAT_ROUTING_HISTORY_WINDOW", "6"))
    recent_messages = request.messages[-history_window:]
    recent_conversation_context = "\n".join(
        f"{message.role}: {message.content}" for message in recent_messages
    )
    routing_input = (
        f"Recent conversation history:\n{recent_conversation_context}\n\n"
        f"Latest user request:\n{latest_user_content}"
    )

    # Route using recent history and an explicit latest-user marker so the
    # model can keep continuity without overfitting to stale turns.
    result = classify_service(routing_input)

    recorder = ToolExecutionRecorder(user_query=routing_context)
    max_steps = int(os.getenv("CHAT_MAX_TOOL_STEPS", "6"))

    def run_service_steps(service: str, initial: ResolvedTool) -> None:
        seen_signatures: set[str] = set()
        current: ResolvedTool | None = initial
        steps = 0

        while current is not None and steps < max_steps:
            signature = json.dumps(
                {"name": current.name, "arguments": current.arguments},
                sort_keys=True,
                ensure_ascii=True,
            )
            if signature in seen_signatures:
                break
            seen_signatures.add(signature)

            should_continue = recorder.record_tool_call(current.name, current.arguments)
            steps += 1
            if not should_continue:
                break

            history = [tool_call.model_dump() for tool_call in recorder.tool_calls]
            current = resolve_follow_up_tool_with_llm(service, routing_context, history)

    match result:
        case Ambiguous(question=question, candidates=candidates):
            clarifying_question = generate_clarifying_question(
                user_text=routing_input,
                fallback_question=question,
                candidates=candidates,
            )
            return ChatResponse(
                messages=[
                    *request.messages,
                    ChatMessage(role="assistant", content=clarifying_question),
                ],
                tool_calls=[],
            )

        case ClassifiedService(service=service):
            resolved = resolve_tool_for_service(service, routing_context)

            run_service_steps(service, resolved)

        case ClassifiedServices(services=services):
            resolved_tools = resolve_tools_for_services(services, routing_context)

            for resolved in resolved_tools:
                service = next((svc for svc in services if resolved.name in tools_for_service(svc)), services[0])
                run_service_steps(service, resolved)

    assistant_content = " ".join(recorder.assistant_parts).strip()
    if not assistant_content:
        assistant_content = "I handled the request."

    return ChatResponse(
        messages=[
            *request.messages,
            ChatMessage(role="assistant", content=assistant_content),
        ],
        tool_calls=recorder.tool_calls,
    )
