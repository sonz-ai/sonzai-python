# Step 3 B.1: Resource Generator Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the resource-method code generator and prove it on 3 spec tags (`memory`, `inventory`, `agents`). This is B.1 of the 4-part B series from the spec (`docs/superpowers/specs/2026-04-22-step3-b-auto-generate-resources-design.md`). B.2 hardens the generator, B.3 migrates all 29 resources, B.4 wires drift hooks.

**Architecture:** A Python script in `scripts/codegen/` walks `openapi.json`, groups operations by tag, and emits `src/sonzai/_generated/resources/<tag>.py` files via a Jinja2 template. Each file contains a sync class + async class with one method per operation. Input-body encoding uses `encode_body` (from A.2). Paginated responses return `Page[T]` / `AsyncPage[T]` (from A.3). Typed exceptions propagate via `_http.py`'s raise path (from A.1).

**Tech Stack:** Jinja2 (new dev dep — or use stdlib `string.Template` if preferred), `openapi-core` is NOT used (we parse `openapi.json` directly with pydantic spec types or raw dict walking). No new runtime deps.

**Dependencies:** A.1 (typed errors), A.2 (encode_body), A.3 (Page/AsyncPage), A.4 (streaming classifier) should land before this. A.5 (retry) is transparent to generated code.

---

## File Structure

**Created:**
- `scripts/codegen/__init__.py` — marker
- `scripts/codegen/generate_resources.py` — entrypoint script
- `scripts/codegen/_parse.py` — `openapi.json` → Python `Operation` objects
- `scripts/codegen/_emit.py` — Jinja templates → Python source
- `scripts/codegen/templates/resource.py.j2` — per-tag module template
- `scripts/codegen/templates/method_sync.j2` — sync method template
- `scripts/codegen/templates/method_async.j2` — async method template
- `scripts/codegen/templates/method_list_sync.j2` — sync paginated list method
- `scripts/codegen/templates/method_list_async.j2` — async paginated list method
- `scripts/codegen/fixtures/mini_spec.json` — canonical small spec for generator unit tests
- `scripts/codegen/fixtures/expected_memory.py` — golden-file output for the PoC
- `tests/test_codegen.py` — generator unit + golden-file tests
- `src/sonzai/_generated/resources/__init__.py` — auto-generated init

**Modified:**
- `pyproject.toml` — add `jinja2` to `[project.optional-dependencies].dev`
- `justfile` — extend `regenerate-sdk` recipe to run the resource generator

---

## Task 1: Parse `openapi.json` → `Operation` objects

**Files:**
- Create: `scripts/codegen/_parse.py`
- Test: `tests/test_codegen.py`
- Create: `scripts/codegen/fixtures/mini_spec.json`

- [ ] **Step 1: Create the mini spec fixture**

Create `scripts/codegen/fixtures/mini_spec.json`:

```json
{
  "openapi": "3.0.3",
  "info": {"title": "mini", "version": "0"},
  "paths": {
    "/api/v1/agents/{agent_id}/facts/all": {
      "get": {
        "operationId": "listAllFacts",
        "tags": ["memory"],
        "parameters": [
          {"name": "agent_id", "in": "path", "required": true, "schema": {"type": "string"}},
          {"name": "user_id", "in": "query", "required": false, "schema": {"type": "string"}},
          {"name": "limit", "in": "query", "required": false, "schema": {"type": "integer", "default": 50}},
          {"name": "offset", "in": "query", "required": false, "schema": {"type": "integer", "default": 0}}
        ],
        "responses": {"200": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/ListAllFactsResponse"}}}}}
      }
    },
    "/api/v1/agents/{agent_id}/facts": {
      "post": {
        "operationId": "addFact",
        "tags": ["memory"],
        "parameters": [{"name": "agent_id", "in": "path", "required": true, "schema": {"type": "string"}}],
        "requestBody": {"required": true, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AddFactInputBody"}}}},
        "responses": {"200": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/StoredFact"}}}}}
      }
    }
  },
  "components": {
    "schemas": {
      "ListAllFactsResponse": {
        "properties": {"facts": {"type": "array", "items": {"$ref": "#/components/schemas/StoredFact"}}, "total": {"type": "integer"}},
        "required": ["facts", "total"]
      },
      "AddFactInputBody": {
        "properties": {"content": {"type": "string"}, "fact_type": {"type": "string"}, "user_id": {"type": "string"}},
        "required": ["content", "fact_type"]
      },
      "StoredFact": {"properties": {"fact_id": {"type": "string"}, "content": {"type": "string"}}, "required": ["fact_id", "content"]}
    }
  }
}
```

- [ ] **Step 2: Write failing parser test**

Create `tests/test_codegen.py`:

```python
"""Tests for the resource code generator."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.codegen._parse import Operation, Parameter, parse_spec

FIXTURES = Path(__file__).resolve().parent.parent / "scripts/codegen/fixtures"


class TestSpecParse:
    def test_groups_operations_by_tag(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        assert set(by_tag.keys()) == {"memory"}
        assert len(by_tag["memory"]) == 2

    def test_list_operation_detected_as_paginated(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        list_op = next(o for o in by_tag["memory"] if o.operation_id == "listAllFacts")
        assert list_op.is_paginated is True
        assert list_op.pagination_mode == "offset"
        assert list_op.pagination_item_key == "facts"
        assert list_op.pagination_item_type == "StoredFact"
        assert list_op.pagination_total_key == "total"

    def test_post_operation_has_input_body(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        add_op = next(o for o in by_tag["memory"] if o.operation_id == "addFact")
        assert add_op.is_paginated is False
        assert add_op.input_body_class == "AddFactInputBody"
        assert add_op.response_class == "StoredFact"

    def test_path_params_extracted(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        add_op = next(o for o in by_tag["memory"] if o.operation_id == "addFact")
        assert [p.name for p in add_op.path_params] == ["agent_id"]
        assert add_op.path_params[0].required is True

    def test_query_params_have_defaults(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        list_op = next(o for o in by_tag["memory"] if o.operation_id == "listAllFacts")
        limit = next(p for p in list_op.query_params if p.name == "limit")
        assert limit.default == 50
```

- [ ] **Step 3: Run test — expect ImportError**

Run: `uv run --extra dev pytest tests/test_codegen.py -v`
Expected: ImportError.

- [ ] **Step 4: Create `scripts/codegen/__init__.py` and `scripts/codegen/_parse.py`**

`scripts/codegen/__init__.py`: empty file.

`scripts/codegen/_parse.py`:

```python
"""Parse openapi.json into generator-friendly Operation objects."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Literal

PLURAL_PATTERN = re.compile(r".*(s|es)$")


@dataclass
class Parameter:
    name: str
    python_name: str                 # snake_case
    location: Literal["path", "query", "header"]
    required: bool
    type_hint: str                   # "str", "int", "bool", "str | None"
    default: Any = None
    description: str | None = None


@dataclass
class Operation:
    operation_id: str
    http_method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    path: str                        # original path with {param} placeholders
    method_name: str                 # snake_case Python name
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

            # Parameters
            for p in op.get("parameters", []):
                param = _build_parameter(p)
                if param.location == "path":
                    operation.path_params.append(param)
                elif param.location == "query":
                    operation.query_params.append(param)

            # Request body
            rb = op.get("requestBody", {}).get("content", {})
            json_body = rb.get("application/json", {}).get("schema", {})
            ref = json_body.get("$ref") or ""
            if ref:
                operation.input_body_class = ref.rsplit("/", 1)[-1]

            # Response body
            resp = op.get("responses", {}).get("200", {}).get("content", {})
            json_resp = resp.get("application/json", {}).get("schema", {})
            resp_ref = json_resp.get("$ref") or ""
            if resp_ref:
                operation.response_class = resp_ref.rsplit("/", 1)[-1]

            # SSE streaming
            if "text/event-stream" in resp:
                operation.is_streaming = True

            # Pagination detection
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
    return Parameter(
        name=name,
        python_name=_snake(name),
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
    return s2.replace("-", "_").lower()


def _op_id_from_path(verb: str, path: str) -> str:
    pieces = [p for p in path.strip("/").split("/") if not p.startswith("{")]
    return f"{verb.lower()}_{'_'.join(pieces)}"
```

- [ ] **Step 5: Run tests — all pass**

Run: `uv run --extra dev pytest tests/test_codegen.py::TestSpecParse -v`
Expected: All 5 tests pass.

- [ ] **Step 6: Commit**

```bash
git add scripts/codegen/__init__.py scripts/codegen/_parse.py scripts/codegen/fixtures/mini_spec.json tests/test_codegen.py
git commit -m "feat: codegen spec parser — openapi.json to Operation objects

Walks openapi.json paths/operations and returns a dict of tag to list
of Operation dataclass instances. Detects pagination (limit + offset or
limit + cursor in query params; response schema with array-of-\$ref
property), streaming (text/event-stream response), input body class
(\$ref on requestBody), response class (\$ref on 200 response). Covers
PoC operations (listAllFacts, addFact) via mini_spec.json golden test."
```

---

## Task 2: Add Jinja2 dev dep + template scaffolding

**Files:**
- Modify: `pyproject.toml`
- Create: `scripts/codegen/templates/*.j2`

- [ ] **Step 1: Add `jinja2` to dev deps**

Edit `pyproject.toml`, find `[project.optional-dependencies].dev`, add:
```toml
    "jinja2>=3.1",
```

Run `uv lock`.

- [ ] **Step 2: Create the resource module template**

Create `scripts/codegen/templates/resource.py.j2`:

```jinja
# Generated by scripts/codegen/generate_resources.py. Do not edit.
# Regenerate via `just regenerate-sdk`.
"""Auto-generated resource classes for the {{ tag_human }} tag."""

from __future__ import annotations

from typing import Any

from sonzai._generated.models import (
{%- for cls in referenced_classes | sort %}
    {{ cls }},
{%- endfor %}
)
from sonzai._pagination import AsyncPage, Page
from sonzai._request_helpers import encode_body


class _{{ class_base }}Base:
    def __init__(self, http: Any) -> None:
        self._http = http


class {{ class_base }}(_{{ class_base }}Base):
{%- for op in operations %}
    {% include op.method_template %}
{% endfor %}


class Async{{ class_base }}(_{{ class_base }}Base):
{%- for op in operations %}
    {% include op.async_method_template %}
{% endfor %}
```

- [ ] **Step 3: Create sync method templates**

Create `scripts/codegen/templates/method_sync.j2`:

```jinja
    def {{ op.method_name }}(
        self,
{%- for pp in op.path_params %}
        {{ pp.python_name }}: {{ pp.type_hint }},
{%- endfor %}
{%- if op.query_params or op.input_body_class %}
        *,
{%- endif %}
{%- for qp in op.query_params %}
        {{ qp.python_name }}: {{ qp.type_hint }}{% if qp.default is not none %} = {{ qp.default | tojson }}{% elif not qp.required %} = None{% endif %},
{%- endfor %}
{%- if op.input_body_class %}
        **body_fields: Any,
{%- endif %}
    ) -> {{ op.response_class or "Any" }}:
        """{{ op.description or "Auto-generated." }}"""
        path = f"{{ op.path }}"
{%- if op.query_params %}
        params: dict[str, Any] = {}
{%- for qp in op.query_params %}
        if {{ qp.python_name }} is not None:
            params["{{ qp.name }}"] = {{ qp.python_name }}
{%- endfor %}
{%- else %}
        params = None
{%- endif %}
{%- if op.input_body_class %}
        body = encode_body({{ op.input_body_class }}, body_fields)
        data = self._http.{{ op.http_method | lower }}(path, params=params, body=body)
{%- elif op.http_method == "GET" or op.http_method == "DELETE" %}
        data = self._http.{{ op.http_method | lower }}(path, params=params)
{%- else %}
        data = self._http.{{ op.http_method | lower }}(path, params=params, body=None)
{%- endif %}
{%- if op.response_class %}
        return {{ op.response_class }}.model_validate(data)
{%- else %}
        return data
{%- endif %}
```

Create `scripts/codegen/templates/method_list_sync.j2`:

```jinja
    def {{ op.method_name }}(
        self,
{%- for pp in op.path_params %}
        {{ pp.python_name }}: {{ pp.type_hint }},
{%- endfor %}
        *,
{%- for qp in op.query_params %}
{%- if qp.name not in ("limit", "offset", "cursor") %}
        {{ qp.python_name }}: {{ qp.type_hint }}{% if qp.default is not none %} = {{ qp.default | tojson }}{% elif not qp.required %} = None{% endif %},
{%- endif %}
{%- endfor %}
        limit: int = 100,
    ) -> Page[{{ op.pagination_item_type }}]:
        """{{ op.description or "Auto-generated paginated list." }}"""
        path = f"{{ op.path }}"
        params: dict[str, Any] = {"limit": limit{% if op.pagination_mode == "offset" %}, "offset": 0{% else %}, "cursor": None{% endif %}}
{%- for qp in op.query_params %}
{%- if qp.name not in ("limit", "offset", "cursor") %}
        if {{ qp.python_name }} is not None:
            params["{{ qp.name }}"] = {{ qp.python_name }}
{%- endif %}
{%- endfor %}
        return Page(
            fetcher=lambda p: self._http.get(path, params=p),
            params=params,
            item_key="{{ op.pagination_item_key }}",
            item_parser={{ op.pagination_item_type }}.model_validate,
            mode="{{ op.pagination_mode }}",
{%- if op.pagination_total_key %}
            total_key="{{ op.pagination_total_key }}",
{%- endif %}
        )
```

Similarly, create `method_async.j2` and `method_list_async.j2` — identical to the sync versions except `def` → `async def`, `Page` → `AsyncPage`, method calls use `await`, and the fetcher lambda is `async`. For brevity I'm not repeating — copy `method_sync.j2` to `method_async.j2`, add `async` keywords, and swap `Page`/`AsyncPage`. Same for the list variant.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml uv.lock scripts/codegen/templates/
git commit -m "feat: codegen Jinja templates for resource method generation

resource.py.j2 emits the per-tag module (sync + async class). Per-method
templates for regular operations and paginated list operations, sync
and async. Input bodies route through encode_body; pagination returns
Page[T]/AsyncPage[T]; responses validated via pydantic model_validate."
```

---

## Task 3: Emit module from template + golden file test

**Files:**
- Create: `scripts/codegen/_emit.py`
- Create: `scripts/codegen/fixtures/expected_memory.py`
- Test: `tests/test_codegen.py`

- [ ] **Step 1: Write the expected golden file**

Create `scripts/codegen/fixtures/expected_memory.py` containing the exact expected output for `memory` tag given `mini_spec.json`. Approximately:

```python
# Generated by scripts/codegen/generate_resources.py. Do not edit.
# Regenerate via `just regenerate-sdk`.
"""Auto-generated resource classes for the Memory tag."""

from __future__ import annotations

from typing import Any

from sonzai._generated.models import (
    AddFactInputBody,
    ListAllFactsResponse,
    StoredFact,
)
from sonzai._pagination import AsyncPage, Page
from sonzai._request_helpers import encode_body


class _MemoryBase:
    def __init__(self, http: Any) -> None:
        self._http = http


class Memory(_MemoryBase):

    def list_all_facts(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
        limit: int = 100,
    ) -> Page[StoredFact]:
        """Auto-generated paginated list."""
        path = f"/api/v1/agents/{agent_id}/facts/all"
        params: dict[str, Any] = {"limit": limit, "offset": 0}
        if user_id is not None:
            params["user_id"] = user_id
        return Page(
            fetcher=lambda p: self._http.get(path, params=p),
            params=params,
            item_key="facts",
            item_parser=StoredFact.model_validate,
            mode="offset",
            total_key="total",
        )


    def add_fact(
        self,
        agent_id: str,
        **body_fields: Any,
    ) -> StoredFact:
        """Auto-generated."""
        path = f"/api/v1/agents/{agent_id}/facts"
        params = None
        body = encode_body(AddFactInputBody, body_fields)
        data = self._http.post(path, params=params, body=body)
        return StoredFact.model_validate(data)


class AsyncMemory(_MemoryBase):

    async def list_all_facts(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
        limit: int = 100,
    ) -> AsyncPage[StoredFact]:
        """Auto-generated paginated list."""
        path = f"/api/v1/agents/{agent_id}/facts/all"
        params: dict[str, Any] = {"limit": limit, "offset": 0}
        if user_id is not None:
            params["user_id"] = user_id
        return AsyncPage(
            fetcher=lambda p: self._http.get(path, params=p),
            params=params,
            item_key="facts",
            item_parser=StoredFact.model_validate,
            mode="offset",
            total_key="total",
        )


    async def add_fact(
        self,
        agent_id: str,
        **body_fields: Any,
    ) -> StoredFact:
        """Auto-generated."""
        path = f"/api/v1/agents/{agent_id}/facts"
        params = None
        body = encode_body(AddFactInputBody, body_fields)
        data = await self._http.post(path, params=params, body=body)
        return StoredFact.model_validate(data)
```

Note: the exact output may differ based on template whitespace. After running the generator, adjust this golden file once to match what the template actually produces — the goal is a stable snapshot.

- [ ] **Step 2: Write failing golden-file test**

Append to `tests/test_codegen.py`:

```python
from scripts.codegen._emit import emit_module


class TestEmit:
    def test_memory_tag_matches_golden(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        output = emit_module("memory", by_tag["memory"])
        expected = (FIXTURES / "expected_memory.py").read_text()
        # normalize trailing whitespace
        assert output.rstrip() == expected.rstrip()
```

- [ ] **Step 3: Run — expect ImportError**

Run: `uv run --extra dev pytest tests/test_codegen.py::TestEmit -v`
Expected: ImportError.

- [ ] **Step 4: Create `scripts/codegen/_emit.py`**

```python
"""Jinja template rendering for resource modules."""

from __future__ import annotations

from pathlib import Path

import jinja2

from ._parse import Operation

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def emit_module(tag: str, operations: list[Operation]) -> str:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )

    # Enrich operations with method template name:
    for op in operations:
        if op.is_paginated:
            op.method_template = "method_list_sync.j2"
            op.async_method_template = "method_list_async.j2"
        else:
            op.method_template = "method_sync.j2"
            op.async_method_template = "method_async.j2"

    # Collect referenced classes (deduped):
    referenced: set[str] = set()
    for op in operations:
        if op.input_body_class:
            referenced.add(op.input_body_class)
        if op.response_class:
            referenced.add(op.response_class)
        if op.pagination_item_type:
            referenced.add(op.pagination_item_type)

    class_base = _to_pascal_case(tag)

    tmpl = env.get_template("resource.py.j2")
    return tmpl.render(
        tag_human=class_base,
        class_base=class_base,
        operations=operations,
        referenced_classes=referenced,
    )


def _to_pascal_case(snake: str) -> str:
    return "".join(part.capitalize() for part in snake.split("_"))
```

- [ ] **Step 5: Iterate: run the test, compare diff, adjust golden or template**

Run: `uv run --extra dev pytest tests/test_codegen.py::TestEmit -v`
Expected: First run likely fails — diff will show whitespace differences. Adjust `expected_memory.py` OR the Jinja template until the test passes. Goal: a clean, readable golden file.

- [ ] **Step 6: Commit**

```bash
git add scripts/codegen/_emit.py scripts/codegen/fixtures/expected_memory.py tests/test_codegen.py
git commit -m "feat: codegen module emitter via Jinja + golden-file test

emit_module(tag, operations) returns the rendered Python source for a
tag. Per-method template is selected by is_paginated. Referenced model
classes deduped for the imports block. Golden-file test against
expected_memory.py prevents silent drift in the generator output shape."
```

---

## Task 4: Entrypoint script + wire into `just regenerate-sdk`

**Files:**
- Create: `scripts/codegen/generate_resources.py`
- Modify: `justfile`

- [ ] **Step 1: Write the entrypoint**

Create `scripts/codegen/generate_resources.py`:

```python
#!/usr/bin/env python3
"""Generate src/sonzai/_generated/resources/<tag>.py from openapi.json.

Usage:
    uv run --extra dev python scripts/codegen/generate_resources.py \
        openapi.json src/sonzai/_generated/resources/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from ._emit import emit_module
from ._parse import parse_spec

INIT_CONTENT = '''"""Auto-generated resource modules.

Do NOT edit files in this directory by hand — they are re-emitted on
every `just regenerate-sdk`.
"""
'''


def main(spec_path: Path, out_dir: Path) -> int:
    spec = json.loads(spec_path.read_text())
    by_tag = parse_spec(spec)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "__init__.py").write_text(INIT_CONTENT)

    for tag, ops in by_tag.items():
        source = emit_module(tag, ops)
        (out_dir / f"{tag}.py").write_text(source)

    print(f"wrote {len(by_tag)} resource modules to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
```

- [ ] **Step 2: Update `justfile::regenerate-sdk`**

Find the `regenerate-sdk` recipe. After the `datamodel-codegen` step and the `__init__.py` write, add:

```just
    @echo "Step 3/4: regenerate resource modules..."
    uv run --extra dev python -m scripts.codegen.generate_resources \
        openapi.json src/sonzai/_generated/resources/
    @uv run --extra dev ruff format src/sonzai/_generated/resources/ 2>/dev/null || true
```

Renumber the old Step 3 (`parity_audit`) to Step 4.

- [ ] **Step 3: Run generator on real spec**

Run: `just regenerate-sdk 2>&1 | tail -5`
Expected: Produces files under `src/sonzai/_generated/resources/` for every tag (memory, agents, knowledge, inventory, etc.).

- [ ] **Step 4: Inspect the output**

Run: `ls src/sonzai/_generated/resources/ && head -40 src/sonzai/_generated/resources/memory.py`
Expected: ~20+ files, `memory.py` shows the Memory and AsyncMemory classes with methods matching the spec's memory tag.

Run: `uv run --extra dev python -c "from sonzai._generated.resources.memory import Memory; print(Memory)"`
Expected: `<class 'sonzai._generated.resources.memory.Memory'>`. If ImportError, the template emitted bad Python — iterate.

- [ ] **Step 5: Commit the generated output + recipe change**

```bash
git add src/sonzai/_generated/resources/ justfile scripts/codegen/generate_resources.py
git commit -m "feat: wire resource generator into regenerate-sdk

\`just regenerate-sdk\` now also emits src/sonzai/_generated/resources/
from openapi.json via the Jinja template pipeline. Nothing in the
public API imports from these generated modules yet — B.3 migrates the
29 hand-written resources to thin subclasses in a later plan."
```

---

## Task 5: PoC subclass — Memory

**Files:**
- Modify: `src/sonzai/resources/memory.py`
- Test: `tests/test_client.py` (verify the path still works)

The real migration of all 29 resources is B.3 (a separate plan). For B.1's PoC, only migrate `memory.py` to confirm the subclass pattern works end-to-end.

- [ ] **Step 1: Back up the existing hand-written `memory.py`**

Copy `src/sonzai/resources/memory.py` → `src/sonzai/resources/memory_legacy.py.bak` (outside git if you prefer; this is a scratch backup). The goal is to compare signatures after migration.

- [ ] **Step 2: Rewrite `src/sonzai/resources/memory.py` as a subclass**

Replace the file contents with:

```python
"""Memory resource — thin convenience layer over the generated class."""

from __future__ import annotations

from typing import Any

from .._generated.resources.memory import AsyncMemory as _GenAsyncMemory
from .._generated.resources.memory import Memory as _GenMemory


class Memory(_GenMemory):
    """Hand-written convenience helpers on top of the generated methods.

    Any method defined in the spec is inherited from the generated
    parent class. Only non-spec helpers belong here.
    """


class AsyncMemory(_GenAsyncMemory):
    """Async mirror of Memory."""
```

- [ ] **Step 3: Run existing memory tests**

Run: `uv run --extra dev pytest tests/test_client.py -v -k memory 2>&1 | tail -20`
Expected: Existing tests may fail because generated method signatures differ from hand-written ones (e.g., body-fields `**body_fields` vs. explicit kwargs). This is the PoC outcome we want to see — a concrete list of signature-divergence items for B.2 to address.

If tests fail, log the failures as a checklist for B.2:
- Each failure surfaces one divergence.
- Adding back the divergent methods as overrides in `memory.py` is an acceptable short-term fix, but the B.2 generator-hardening plan should close the gap.

- [ ] **Step 4: For now, add overrides for signature-divergent methods**

For each failing test's method, copy the legacy signature from the backup and override in the new `Memory` class. Mark each override with a comment:
```python
# TODO(B.2): signature differs from generator (e.g. explicit `content: str`
# kwargs vs. **body_fields). Remove this override once B.2 hardens the
# generator to preserve kwargs names from input body required fields.
def add(self, agent_id: str, *, content: str, fact_type: str, **kwargs: Any) -> StoredFact:
    return super().add_fact(agent_id, content=content, fact_type=fact_type, **kwargs)
```

This is explicitly allowed plan debt — B.2 cleans it up.

- [ ] **Step 5: Run full suite**

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: All pass.

- [ ] **Step 6: Commit**

```bash
git add src/sonzai/resources/memory.py
git commit -m "feat: Memory resource is now a thin subclass of generated class (PoC)

Replaces the ~500-line hand-written Memory + AsyncMemory with a thin
subclass over sonzai._generated.resources.memory. Any signature
divergence between hand-written and generator surfaces as a method
override in this file with a TODO(B.2) marker for the generator
hardening plan to address.

This PROVES the subclass pattern for B.3's full migration."
```

---

## Self-Review Findings

- **Spec output layout** — Task 4 writes to `src/sonzai/_generated/resources/<tag>.py`, matching the spec.
- **Spec customization pattern** — Task 5 demonstrates the subclass pattern on memory.
- **Spec pagination integration** — method_list_sync.j2 returns `Page[T]`; references the item_parser and mode.
- **Spec typed-body integration** — templates use `encode_body(InputBody, ...)` from A.2.
- **Spec streaming integration** — NOT covered in this plan. B.1 is scaffolding; streaming methods will fall into the non-paginated default template and likely generate wrong code. Explicit follow-up task is B.2.
- **Spec drift-detection hooks** — B.4 handles; NOT in this plan.

**Placeholder scan**: one TODO(B.2) comment in Task 5 Step 4 for signature-divergence overrides; intentional handoff to the next plan in the series.

**Type consistency**: `Operation`, `Parameter`, template filenames, emit_module signature consistent across tasks.

**Out of scope for this plan (deferred to B.2/B.3/B.4)**:
- Streaming operation template (SSE endpoints return wrong type today)
- Multipart form data / file upload operations
- Migrating the other 28 resource files (B.3)
- Pre-commit / pre-push hook extensions for `_generated/resources/` (B.4)
- Signature-parity check script (B.4)
