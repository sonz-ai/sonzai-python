"""Parse openapi.json into generator-friendly Operation objects."""

from __future__ import annotations

import keyword
import re
from dataclasses import dataclass, field
from typing import Any, Literal


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
class Operation:
    operation_id: str
    http_method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    path: str
    method_name: str
    tag: str
    path_params: list[Parameter] = field(default_factory=list)
    query_params: list[Parameter] = field(default_factory=list)
    input_body_class: str | None = None
    response_class: str | None = None
    is_streaming: bool = False
    is_paginated: bool = False
    pagination_mode: Literal["offset", "cursor"] | None = None
    pagination_item_key: str | None = None
    pagination_item_type: str | None = None
    pagination_total_key: str | None = None
    description: str | None = None


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

            rb = op.get("requestBody", {}).get("content", {})
            json_body = rb.get("application/json", {}).get("schema", {})
            ref = json_body.get("$ref") or ""
            if ref:
                operation.input_body_class = ref.rsplit("/", 1)[-1]

            resp = op.get("responses", {}).get("200", {}).get("content", {})
            json_resp = resp.get("application/json", {}).get("schema", {})
            resp_ref = json_resp.get("$ref") or ""
            if resp_ref:
                operation.response_class = resp_ref.rsplit("/", 1)[-1]

            if "text/event-stream" in resp:
                operation.is_streaming = True

            _detect_pagination(operation, schemas)

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
