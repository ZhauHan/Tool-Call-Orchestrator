from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from backend.helpers.common import Service

_DOCS_DIR = Path(__file__).resolve().parents[2] / "docs" / "mcp_tool_definitions"


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    parameters: list[dict[str, Any]]


def parse_tool_definitions_from_file(path: Path) -> list[ToolDefinition]:
    lines = path.read_text(encoding="utf-8").splitlines()
    definitions: list[ToolDefinition] = []
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()
        if (
            stripped
            and " " not in stripped
            and re.fullmatch(r"[A-Za-z0-9_]+", stripped)
            and stripped.lower() not in {"server", "description", "parameters", "returns"}
        ):
            tool_name = stripped
            description = ""
            parameters: list[dict[str, Any]] = []
            i += 1

            while i < len(lines):
                row = lines[i].strip()
                if not row:
                    i += 1
                    continue

                if row.startswith("Description:"):
                    description = row.removeprefix("Description:").strip()
                    i += 1
                    continue

                if row.startswith("Parameters:"):
                    i += 1
                    while i < len(lines):
                        param_line = lines[i].strip()
                        if not param_line:
                            i += 1
                            continue
                        if not param_line.startswith("-"):
                            break

                        match = re.match(
                            r"-\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\):\s*(.*)",
                            param_line,
                        )
                        if match:
                            parameters.append(
                                {
                                    "name": match.group(1),
                                    "meta": match.group(2),
                                    "required": "required" in match.group(2).lower(),
                                    "description": match.group(3),
                                }
                            )
                        i += 1
                    continue

                if (
                    row
                    and " " not in row
                    and re.fullmatch(r"[A-Za-z0-9_]+", row)
                    and row != tool_name
                ):
                    break

                if row.startswith("==="):
                    break

                i += 1

            definitions.append(
                ToolDefinition(
                    name=tool_name,
                    description=description,
                    parameters=parameters,
                )
            )
            continue

        i += 1

    return definitions


def build_tool_definitions_index() -> dict[str, ToolDefinition]:
    index: dict[str, ToolDefinition] = {}
    if not _DOCS_DIR.exists():
        return index

    for path in _DOCS_DIR.glob("*.md"):
        try:
            definitions = parse_tool_definitions_from_file(path)
        except Exception:
            continue

        for definition in definitions:
            index[definition.name] = definition

    return index


TOOL_DEFINITIONS_BY_NAME: dict[str, ToolDefinition] = build_tool_definitions_index()


def runtime_tools_for_service(service: Service) -> list[str]:
    try:
        from backend.main import get_all_tool_specs

        tool_specs = get_all_tool_specs()
        names = [
            tool_name
            for tool_name, spec in tool_specs.items()
            if getattr(spec, "service", None) == service
        ]
        return sorted(set(names))
    except Exception:
        return []


def tool_context_for_service(service: Service) -> list[dict[str, Any]]:
    names = runtime_tools_for_service(service)
    if not names:
        return []

    context: list[dict[str, Any]] = []

    runtime_specs: dict[str, Any] = {}
    try:
        from backend.main import get_all_tool_specs

        runtime_specs = get_all_tool_specs()
    except Exception:
        runtime_specs = {}

    for name in names:
        definition = TOOL_DEFINITIONS_BY_NAME.get(name)
        params: list[str] = []
        required_params: list[str] = []
        description = ""

        if definition is not None:
            description = definition.description
            params = [
                param.get("name")
                for param in definition.parameters
                if isinstance(param, dict) and isinstance(param.get("name"), str)
            ]
            required_params = [
                param.get("name")
                for param in definition.parameters
                if isinstance(param, dict)
                and isinstance(param.get("name"), str)
                and bool(param.get("required"))
            ]

        runtime_spec = runtime_specs.get(name)
        if runtime_spec is not None:
            if not description:
                description = str(
                    getattr(runtime_spec, "description", "")
                    or getattr(runtime_spec, "docstring", "")
                )
            try:
                fields = runtime_spec.args_model.model_fields
                runtime_params = list(fields.keys())
                runtime_required = [
                    field_name for field_name, info in fields.items() if info.is_required()
                ]
                params = sorted(set(params) | set(runtime_params)) if params else runtime_params
                required_params = (
                    sorted(set(required_params) | set(runtime_required))
                    if required_params
                    else runtime_required
                )
            except Exception:
                pass

        context.append(
            {
                "name": name,
                "description": description,
                "required_params": required_params,
                "params": params,
            }
        )

    return context
