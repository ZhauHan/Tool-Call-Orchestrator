"""Helper modules for the candidate's chat solution.

Modules:
- common: shared Service type and OpenAI client factory
- service_classifier: request-to-service routing and clarification prompts
- capability_resolver: capability and execution-intent assessment
- tool_catalog: tool metadata from runtime registry and MCP docs
- tool_selector: LLM-driven tool selection and follow-up planning
- argument_crafter: argument generation and schema-based coercion
- result_summarizer: LLM and fallback result summarization
- chat_execution: tool invocation, argument augmentation, and turn-local recording
"""

__all__ = [
	"argument_crafter",
	"capability_resolver",
	"chat_execution",
	"common",
	"result_summarizer",
	"service_classifier",
	"tool_catalog",
	"tool_given_service",
	"tool_selector",
]
