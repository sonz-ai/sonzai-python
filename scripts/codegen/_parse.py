"""Parse openapi.json into generator-friendly Operation objects."""

from __future__ import annotations

import keyword
import re
from dataclasses import dataclass, field
from typing import Any, Literal

# Spec paths omit /api/v1 — prepend it at parse time.
_PATH_PREFIX = "/api/v1"

# Mapping of (tag, operation_id) → historical SDK method name.
# Keeps generated method names aligned with the public API contract when
# the spec's operationId would otherwise introduce a breaking rename.
METHOD_NAME_OVERRIDES: dict[tuple[str, str], str] = {
    ("memory", "getMemoryTree"): "list",
    ("memory", "searchMemories"): "search",
    ("memory", "resetMemory"): "reset",
    ("memory", "getMemoryTimeline"): "timeline",
}

# Mapping of (tag, operation_id, wire_param_name) → python_name override.
# Keeps generated kwarg names aligned with the public API contract when
# the spec uses a different name.
QUERY_PARAM_OVERRIDES: dict[tuple[str, str, str], str] = {
    ("memory", "searchMemories", "q"): "query",
}

# Map of (tag, operation_id) → historical SDK response class name.
# Applied after response_class is set. Keeps the generated output
# aligned with sonzai.types / sonzai re-exports that predate the
# spec's naming conventions.
RESPONSE_CLASS_OVERRIDES: dict[tuple[str, str], str] = {
    ("memory", "resetMemory"): "MemoryResetResponse",
    # Add more as overrides are identified.
}

# Map of class name → import module path for classes that live outside
# sonzai._generated.models (e.g. legacy types in sonzai.types).
# Used by _emit.py to emit correct import statements.
EXTERNAL_CLASS_IMPORTS: dict[str, str] = {
    "MemoryResetResponse": "sonzai.types",
    # DeleteWisdomResponse: sonzai.types version has all-default fields (safe
    # for Fix-3 empty-body fallback), unlike the spec-generated version which
    # has required fields.
    "DeleteWisdomResponse": "sonzai.types",
    # Add more as overrides are identified.
}


@dataclass
class Parameter:
    name: str
    python_name: str
    location: Literal["path", "query", "header"]
    required: bool
    type_hint: str
    default: Any = None
    description: str | None = None


@dataclass
class InputBodyField:
    name: str
    python_name: str
    type_hint: str
    required: bool
    default: Any = None


@dataclass
class Operation:
    operation_id: str
    http_method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    path: str
    method_name: str
    tag: str
    path_params: list[Parameter] = field(default_factory=list)
    query_params: list[Parameter] = field(default_factory=list)
    input_body_class: str | None = None
    input_body_fields: list[InputBodyField] = field(default_factory=list)
    response_class: str | None = None
    is_streaming: bool = False
    is_paginated: bool = False
    pagination_mode: Literal["offset", "cursor"] | None = None
    pagination_item_key: str | None = None
    pagination_item_type: str | None = None
    pagination_total_key: str | None = None
    description: str | None = None
    python_path: str = ""  # path with {camelCase} replaced by {snake_case} + /api/v1 prefix
    path_expression: str = ""  # python_path with str params wrapped in quote()


def _build_python_path(path: str, path_params: list[Parameter]) -> str:
    """Return a Python f-string-safe path: snake_case params + /api/v1 prefix."""
    result = path
    # Replace camelCase path placeholders with snake_case python_name
    for pp in path_params:
        result = result.replace("{" + pp.name + "}", "{" + pp.python_name + "}")
    # Prepend /api/v1 if the spec omits it
    if not result.startswith(_PATH_PREFIX):
        result = _PATH_PREFIX + result
    return result


def render_path_expression(op: "Operation") -> str:
    """Return a Python expression that constructs the path with URL-quoted string params.

    For path ``/api/v1/agents/{agent_id}/users/{user_id}/x``, emits:
        f"/api/v1/agents/{quote(agent_id, safe='')}/users/{quote(user_id, safe='')}/x"
    """
    result = op.python_path
    # Walk through path params, wrapping string-typed ones with quote().
    for pp in op.path_params:
        needle = "{" + pp.python_name + "}"
        if pp.type_hint.startswith("str"):
            result = result.replace(needle, "{quote(" + pp.python_name + ", safe='')}")
    return result


def parse_spec(spec: dict[str, Any]) -> dict[str, list[Operation]]:
    """Return a dict of tag → list of Operation objects."""
    by_tag: dict[str, list[Operation]] = {}
    schemas = spec.get("components", {}).get("schemas", {})

    for path, ops in spec.get("paths", {}).items():
        for verb, op in ops.items():
            verb_upper = verb.upper()
            if verb_upper not in ("GET", "POST", "PUT", "PATCH", "DELETE"):
                continue

            tags = op.get("tags") or ["default"]
            tag = _snake(tags[0])
            op_id = op.get("operationId") or _op_id_from_path(verb_upper, path)
            method_name = _snake(op_id)

            # Apply method name override if defined
            override_name = METHOD_NAME_OVERRIDES.get((tag, op_id))
            if override_name:
                method_name = override_name

            operation = Operation(
                operation_id=op_id,
                http_method=verb_upper,
                path=path,
                method_name=method_name,
                tag=tag,
                description=op.get("summary") or op.get("description"),
            )

            for p in op.get("parameters", []):
                param = _build_parameter(p)
                if param.location == "path":
                    operation.path_params.append(param)
                elif param.location == "query":
                    operation.query_params.append(param)

            # Apply query param python_name overrides
            for qp in operation.query_params:
                qp_override = QUERY_PARAM_OVERRIDES.get((tag, op_id, qp.name))
                if qp_override:
                    qp.python_name = qp_override

            rb = op.get("requestBody", {}).get("content", {})
            json_body = rb.get("application/json", {}).get("schema", {})
            ref = json_body.get("$ref") or ""
            if ref:
                operation.input_body_class = ref.rsplit("/", 1)[-1]

            # Extract explicit input body fields for IDE autocomplete
            if operation.input_body_class:
                schema = schemas.get(operation.input_body_class, {})
                required_fields = set(schema.get("required", []))
                for fname, fdesc in schema.get("properties", {}).items():
                    if fname.startswith("$"):  # skip $schema etc
                        continue
                    ftype = _type_hint(fdesc.get("type"), fname in required_fields)
                    operation.input_body_fields.append(
                        InputBodyField(
                            name=fname,
                            python_name=_snake(fname).replace(".", "_"),
                            type_hint=ftype,
                            required=fname in required_fields,
                            default=fdesc.get("default"),
                        )
                    )

            resp = op.get("responses", {}).get("200", {}).get("content", {})
            json_resp = resp.get("application/json", {}).get("schema", {})
            resp_ref = json_resp.get("$ref") or ""
            if resp_ref:
                operation.response_class = resp_ref.rsplit("/", 1)[-1]

            if "text/event-stream" in resp:
                operation.is_streaming = True

            # Apply response class name override if defined
            resp_override = RESPONSE_CLASS_OVERRIDES.get((tag, op_id))
            if resp_override:
                operation.response_class = resp_override

            _detect_pagination(operation, schemas)

            # Build python_path after all params are collected
            operation.python_path = _build_python_path(path, operation.path_params)
            # Build path_expression with URL-quoted string params
            operation.path_expression = render_path_expression(operation)

            by_tag.setdefault(tag, []).append(operation)

    return by_tag


def _detect_pagination(op: Operation, schemas: dict[str, Any]) -> None:
    if op.http_method != "GET":
        return
    qnames = {p.name for p in op.query_params}
    if "limit" not in qnames:
        return

    mode: Literal["offset", "cursor"] | None = None
    if "offset" in qnames:
        mode = "offset"
    elif "cursor" in qnames or "page_token" in qnames:
        mode = "cursor"
    else:
        return

    if not op.response_class:
        return

    schema = schemas.get(op.response_class, {})
    props = schema.get("properties", {})

    item_key: str | None = None
    item_type: str | None = None
    for name, desc in props.items():
        t = desc.get("type")
        is_array = t == "array" or (isinstance(t, list) and "array" in t)
        if is_array:
            items = desc.get("items", {})
            iref = items.get("$ref") or ""
            if iref:
                item_type = iref.rsplit("/", 1)[-1]
                item_key = name
                break

    if not item_key or not item_type:
        return

    op.is_paginated = True
    op.pagination_mode = mode
    op.pagination_item_key = item_key
    op.pagination_item_type = item_type
    op.pagination_total_key = "total" if "total" in props else None


def _build_parameter(p: dict[str, Any]) -> Parameter:
    name = p.get("name", "")
    location = p.get("in", "query")
    required = bool(p.get("required", False))
    schema = p.get("schema", {})
    py_type = _type_hint(schema.get("type"), required)
    default = schema.get("default")
    python_name = _snake(name).replace(".", "_")
    if keyword.iskeyword(python_name):
        python_name = f"{python_name}_"
    return Parameter(
        name=name,
        python_name=python_name,
        location=location,
        required=required,
        type_hint=py_type,
        default=default,
        description=p.get("description"),
    )


def _type_hint(openapi_type: str | list[str] | None, required: bool) -> str:
    mapping = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "array": "list[Any]",
        "object": "dict[str, Any]",
    }
    if isinstance(openapi_type, list):
        primary = next((t for t in openapi_type if t != "null"), "string")
    else:
        primary = openapi_type or "string"
    base = mapping.get(primary, "Any")
    if required:
        return base
    return f"{base} | None"


def _snake(name: str) -> str:
    s1 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    s2 = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s1)
    return s2.replace("-", "_").replace(" ", "_").lower()


def _op_id_from_path(verb: str, path: str) -> str:
    pieces = [p for p in path.strip("/").split("/") if not p.startswith("{")]
    return f"{verb.lower()}_{'_'.join(pieces)}"
