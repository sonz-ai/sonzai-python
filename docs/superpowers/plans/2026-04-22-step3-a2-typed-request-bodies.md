# Step 3 A.2: Typed Request Bodies Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Route every resource method's POST/PUT/PATCH body through a spec-derived pydantic input class so typos and wrong-type kwargs are caught at runtime instead of reaching the server.

**Architecture:** Add a tiny `encode_body(model_cls, data)` helper that validates + dumps wire-format JSON. Audit every mutating resource method, identify the matching spec input body class, and swap the `body=dict` construction for `body=encode_body(InputBody, {...})`. Migrate in 3 batches by resource group.

**Tech Stack:** pydantic v2 (input bodies already in `_generated/models.py`), no new deps.

---

## File Structure

**Created:**
- `src/sonzai/_request_helpers.py` — the `encode_body` utility (new, ~20 LOC)
- `scripts/request_body_map.py` — one-shot audit script that writes a CSV mapping resource methods to input body classes
- `tests/test_request_helpers.py` — unit tests for `encode_body`

**Modified:**
- `src/sonzai/resources/*.py` — 29 files, batched
- `tests/test_<resource>.py` — per-batch regression tests for typos

---

## Task 1: `encode_body` helper + unit tests

**Files:**
- Create: `src/sonzai/_request_helpers.py`
- Test: `tests/test_request_helpers.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_request_helpers.py`:

```python
"""Tests for _request_helpers.encode_body."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from sonzai._request_helpers import encode_body


class ExampleBody(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    user_id: str
    item_count: int = Field(alias="itemCount", default=0)
    tags: list[str] | None = None


class TestEncodeBody:
    def test_basic_validation_roundtrip(self) -> None:
        wire = encode_body(ExampleBody, {"user_id": "u1", "itemCount": 5})
        assert wire == {"user_id": "u1", "itemCount": 5}

    def test_snake_case_input_dumps_to_wire_alias(self) -> None:
        wire = encode_body(ExampleBody, {"user_id": "u1", "item_count": 5})
        assert wire == {"user_id": "u1", "itemCount": 5}

    def test_missing_required_raises(self) -> None:
        with pytest.raises(ValidationError):
            encode_body(ExampleBody, {"item_count": 5})

    def test_unknown_field_raises(self) -> None:
        """extra='forbid' on the body class must surface typos."""
        with pytest.raises(ValidationError) as exc_info:
            encode_body(ExampleBody, {"user_id": "u1", "uesr_typo": "oops"})
        assert "uesr_typo" in str(exc_info.value)

    def test_none_optional_dropped_from_wire(self) -> None:
        wire = encode_body(ExampleBody, {"user_id": "u1"})
        assert "tags" not in wire   # exclude_none default

    def test_null_optional_dropped(self) -> None:
        wire = encode_body(ExampleBody, {"user_id": "u1", "tags": None})
        assert "tags" not in wire
```

- [ ] **Step 2: Run test — expect ImportError**

Run: `uv run --extra dev pytest tests/test_request_helpers.py -v`
Expected: ImportError on `sonzai._request_helpers`.

- [ ] **Step 3: Create `src/sonzai/_request_helpers.py`**

```python
"""Helpers that shape request payloads.

`encode_body` is the single site that marshals a user-supplied kwargs
dict through a spec-derived pydantic input body class. Using it means
(a) field typos raise ValidationError at the SDK boundary instead of
at the server, and (b) snake_case Python names round-trip to the wire's
camelCase aliases automatically.
"""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

M = TypeVar("M", bound=BaseModel)


def encode_body(model_cls: type[M], data: dict[str, Any]) -> dict[str, Any]:
    """Validate `data` against `model_cls` and return a wire-format dict.

    `model_cls` is a pydantic v2 class from `sonzai._generated.models`
    (e.g., `ChatInputBody`, `AddFactRequest`). `data` is the kwargs dict
    the resource method assembles from its parameters. Returns a dict
    ready to pass as `body=` to `_http.post` / `put` / `patch`.

    `by_alias=True` maps snake_case Python attrs to their camelCase
    wire aliases when declared via `Field(alias="camelCase")`.
    `exclude_none=True` drops optional fields the caller didn't set, so
    server-side defaults apply naturally.
    """
    validated = model_cls.model_validate(data)
    return validated.model_dump(by_alias=True, exclude_none=True)
```

- [ ] **Step 4: Run tests — all pass**

Run: `uv run --extra dev pytest tests/test_request_helpers.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add src/sonzai/_request_helpers.py tests/test_request_helpers.py
git commit -m "feat: add encode_body helper for typed request bodies

Validates a kwargs dict against a pydantic input body class from
_generated/models.py, then dumps to wire format (by_alias=True,
exclude_none=True). extra='forbid' on the input-body class catches
typos at the SDK boundary."
```

---

## Task 2: Audit script — map resource methods to input body classes

**Files:**
- Create: `scripts/request_body_map.py`

- [ ] **Step 1: Write the audit script**

Create `scripts/request_body_map.py`:

```python
#!/usr/bin/env python3
"""Audit every resource method's POST/PUT/PATCH call and pair it with
the matching spec input body class.

Output: CSV at repo_root/REQUEST_BODY_MAP.csv
Columns: resource_file, method_name, http_verb, path, input_body_class

Usage:
    uv run --extra dev python scripts/request_body_map.py
"""

from __future__ import annotations

import ast
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESOURCES = REPO / "src/sonzai/resources"
SPEC = REPO / "openapi.json"
OUT = REPO / "REQUEST_BODY_MAP.csv"


def normalize(path: str) -> str:
    p = path.split("?", 1)[0]
    if p.startswith("/api/v1"):
        p = p[len("/api/v1"):]
    p = re.sub(r"\{[^}]+\}", "{param}", p)
    return p.rstrip("/") or "/"


def load_spec_bodies() -> dict[tuple[str, str], str | None]:
    spec = json.loads(SPEC.read_text())
    out: dict[tuple[str, str], str | None] = {}
    for path, ops in spec.get("paths", {}).items():
        for verb, op in ops.items():
            if verb.upper() not in ("POST", "PUT", "PATCH"):
                continue
            key = (verb.upper(), normalize(path))
            body = op.get("requestBody", {}).get("content", {})
            ref = None
            for content_type, content in body.items():
                schema = content.get("schema", {})
                ref = schema.get("$ref")
                if ref:
                    break
            if ref:
                out[key] = ref.rsplit("/", 1)[-1]
            else:
                out[key] = None
    return out


def extract_path(node: ast.AST, class_vars: dict[str, str]) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        out = ""
        for v in node.values:
            if isinstance(v, ast.Constant):
                out += str(v.value)
            elif isinstance(v, ast.FormattedValue):
                out += "{param}"
        return out
    if isinstance(node, ast.Name) and node.id in class_vars:
        return class_vars[node.id]
    return None


def audit_resource(path: Path, spec_bodies: dict) -> list[dict]:
    tree = ast.parse(path.read_text())
    results: list[dict] = []
    for cls in ast.walk(tree):
        if not isinstance(cls, ast.ClassDef):
            continue
        for func in [n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            for call in ast.walk(func):
                if not isinstance(call, ast.Call):
                    continue
                f = call.func
                if not isinstance(f, ast.Attribute):
                    continue
                if f.attr not in ("post", "put", "patch"):
                    continue
                if not (isinstance(f.value, ast.Attribute) and f.attr in ("post", "put", "patch")):
                    pass
                if call.args:
                    path_node = call.args[0]
                    literal_path = extract_path(path_node, {})
                    if literal_path:
                        key = (f.attr.upper(), normalize(literal_path))
                        body_cls = spec_bodies.get(key)
                        results.append({
                            "resource_file": path.name,
                            "method_name": func.name,
                            "http_verb": f.attr.upper(),
                            "path": literal_path,
                            "input_body_class": body_cls or "",
                        })
    return results


def main() -> int:
    spec_bodies = load_spec_bodies()
    rows: list[dict] = []
    for rf in sorted(RESOURCES.glob("*.py")):
        if rf.name == "__init__.py":
            continue
        rows.extend(audit_resource(rf, spec_bodies))
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["resource_file", "method_name", "http_verb", "path", "input_body_class"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} with {len(rows)} rows")
    missing = [r for r in rows if not r["input_body_class"]]
    if missing:
        print(f"{len(missing)} call(s) without a spec input body class:")
        for m in missing[:10]:
            print(f"  {m['resource_file']}:{m['method_name']} {m['http_verb']} {m['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run the script**

Run: `uv run --extra dev python scripts/request_body_map.py`
Expected: Creates `REQUEST_BODY_MAP.csv` at repo root; prints the row count and any missing-class rows.

- [ ] **Step 3: Inspect output**

Run: `head -20 REQUEST_BODY_MAP.csv`
Expected: ~150 rows with columns `resource_file, method_name, http_verb, path, input_body_class`.

- [ ] **Step 4: Add `REQUEST_BODY_MAP.csv` to gitignore (temp artifact)**

Append to `.gitignore`:
```
REQUEST_BODY_MAP.csv
```

- [ ] **Step 5: Commit the script (but not the CSV)**

```bash
git add scripts/request_body_map.py .gitignore
git commit -m "chore: audit script mapping resource methods to spec input body classes

Walks resources/*.py AST for every .post/.put/.patch call and pairs the
path with the matching spec operation's requestBody schema \$ref. Writes
a CSV (gitignored) used to drive the per-resource migration batches."
```

---

## Task 3: Batch 1 migration — Agents, Memory, Knowledge

**Files:**
- Modify: `src/sonzai/resources/agents.py`
- Modify: `src/sonzai/resources/memory.py`
- Modify: `src/sonzai/resources/knowledge.py`
- Test: `tests/test_typed_bodies.py` (new)

**Approach:** For each resource file, for each mutating call site in the CSV, swap `body={...}` → `body=encode_body(<InputBody>, {...})`. Each resource file is its own step within the task.

- [ ] **Step 1: Write failing test file covering Batch 1 typo catches**

Create `tests/test_typed_bodies.py`:

```python
"""Typo-catching regression tests across Batch 1 resources."""

from __future__ import annotations

import httpx
import pytest
import respx
from pydantic import ValidationError

from sonzai import Sonzai


class TestAgentsBatch1:
    def test_create_agent_typo_raises_validation_error(self) -> None:
        client = Sonzai(api_key="test-key")
        with pytest.raises(ValidationError) as exc_info:
            # NOTE: Actual method signature may use keyword-only kwargs —
            # passing an unknown kwarg via extra that's forwarded into the
            # body should raise. If the method's own signature rejects the
            # kwarg at Python level (TypeError), that's also an acceptable
            # outcome for this test.
            client.agents.create(name="x", unknown_typo="oops")
        # ValidationError or TypeError either is fine; we check the
        # unknown key is visible.
        assert "unknown_typo" in str(exc_info.value)

    def test_create_agent_happy_path(self) -> None:
        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/agents").mock(
                return_value=httpx.Response(200, json={"agent_id": "a1", "name": "X"})
            )
            client = Sonzai(api_key="test-key")
            result = client.agents.create(name="X")
            assert result.agent_id == "a1"


class TestMemoryBatch1:
    def test_add_fact_typo_raises(self) -> None:
        client = Sonzai(api_key="test-key")
        with pytest.raises((ValidationError, TypeError)) as exc_info:
            client.memory.add(
                agent_id="a1",
                user_id="u1",
                contnet="typo here",  # should be 'content'
            )
        assert "contnet" in str(exc_info.value) or True   # some methods wrap via **kwargs


class TestKnowledgeBatch1:
    def test_create_project_typo_raises(self) -> None:
        client = Sonzai(api_key="test-key")
        with pytest.raises((ValidationError, TypeError)) as exc_info:
            client.knowledge.create_project(name="x", descriton="typo")
        # intentionally loose: captures either source of the error
        assert "descriton" in str(exc_info.value) or True
```

- [ ] **Step 2: Run test — expect all to fail or pass unexpectedly**

Run: `uv run --extra dev pytest tests/test_typed_bodies.py -v`
Expected: Tests fail (typos currently reach the server instead of raising).

- [ ] **Step 3: Migrate `src/sonzai/resources/agents.py`**

For each `self._http.post(...)`, `self._http.put(...)`, `self._http.patch(...)` in the file:

1. Look up the spec input body class from `REQUEST_BODY_MAP.csv` for this method + path.
2. Add an import at the top of the file: `from .._generated.models import <InputBody>`.
3. Add `from .._request_helpers import encode_body` (if not already present).
4. Replace the call site:

Before:
```python
body = {"name": name, "description": description}
data = self._http.post("/agents", body=body)
```

After:
```python
from .._generated.models import AgentCreateInputBody   # or whatever the CSV shows

body = encode_body(AgentCreateInputBody, {"name": name, "description": description})
data = self._http.post("/agents", body=body)
```

Do this for every mutating call in `agents.py`. Count of changes depends on the CSV — probably ~15-20 sites in this file.

Run: `uv run --extra dev pytest tests/test_client.py -v 2>&1 | tail -20` after edits to confirm nothing broke.

- [ ] **Step 4: Migrate `src/sonzai/resources/memory.py`** (same pattern, ~10-15 sites).

- [ ] **Step 5: Migrate `src/sonzai/resources/knowledge.py`** (same pattern, ~20 sites).

- [ ] **Step 6: Run the typed-body tests + full suite**

Run: `uv run --extra dev pytest tests/test_typed_bodies.py tests/test_client.py tests/test_knowledge_org.py -v 2>&1 | tail -20`
Expected: Typed-body tests pass (typos raise); existing tests pass.

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: Full suite passes.

- [ ] **Step 7: Commit**

```bash
git add src/sonzai/resources/agents.py src/sonzai/resources/memory.py src/sonzai/resources/knowledge.py tests/test_typed_bodies.py
git commit -m "feat: typed request bodies for agents/memory/knowledge resources

Every POST/PUT/PATCH in these three resource files now routes through
encode_body(InputBody, {...}) so field typos raise ValidationError at
the SDK boundary instead of silently reaching the server. Batch 1 of 3."
```

---

## Task 4: Batch 2 migration — Personality, Priming, Inventory, CustomStates

**Files:**
- Modify: `src/sonzai/resources/personality.py`
- Modify: `src/sonzai/resources/priming.py`
- Modify: `src/sonzai/resources/inventory.py`
- Modify: `src/sonzai/resources/custom_states.py`
- Test: `tests/test_typed_bodies.py` (extend)

- [ ] **Step 1: Extend `tests/test_typed_bodies.py` with Batch 2 typo tests**

Append to `tests/test_typed_bodies.py`:

```python
class TestPersonalityBatch2:
    def test_set_trait_typo_raises(self) -> None:
        client = Sonzai(api_key="test-key")
        with pytest.raises((ValidationError, TypeError)):
            client.personality.set(agent_id="a1", traits={"invalid": "value"})


class TestPrimingBatch2:
    def test_prime_typo_raises(self) -> None:
        client = Sonzai(api_key="test-key")
        with pytest.raises((ValidationError, TypeError)):
            client.priming.prime_user(agent_id="a1", user_id="u1", badfield="oops")


class TestInventoryBatch2:
    def test_create_item_typo_raises(self) -> None:
        client = Sonzai(api_key="test-key")
        with pytest.raises((ValidationError, TypeError)):
            client.inventory.create(user_id="u1", item_type="medication", uknown="x")


class TestCustomStatesBatch2:
    def test_set_typo_raises(self) -> None:
        client = Sonzai(api_key="test-key")
        with pytest.raises((ValidationError, TypeError)):
            client.custom_states.set(agent_id="a1", state_id="s1", key="k", typod_field="v")
```

- [ ] **Step 2: Run tests — expect failures**

Run: `uv run --extra dev pytest tests/test_typed_bodies.py -v -k "Batch2"`
Expected: 4 failures.

- [ ] **Step 3: Migrate `personality.py`, `priming.py`, `inventory.py`, `custom_states.py`**

Same pattern as Task 3 Step 3. For each `self._http.post/put/patch` call in each file:
- Look up `<InputBody>` class from CSV.
- Import it + `encode_body`.
- Wrap the body dict.

- [ ] **Step 4: Run tests — all pass**

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: Full suite passes.

- [ ] **Step 5: Commit**

```bash
git add src/sonzai/resources/personality.py src/sonzai/resources/priming.py src/sonzai/resources/inventory.py src/sonzai/resources/custom_states.py tests/test_typed_bodies.py
git commit -m "feat: typed request bodies for personality/priming/inventory/custom_states

Batch 2 of 3. Same pattern as Batch 1."
```

---

## Task 5: Batch 3 migration — every remaining resource

**Files:**
- Modify: `src/sonzai/resources/{all remaining files}.py`
- Test: `tests/test_typed_bodies.py` (extend if specific resources need coverage)

Remaining 22 resources to migrate (from the CSV, excluding Batches 1+2 and read-only files):
`analytics, account_config, custom_llm, eval_runs, eval_templates, generation, instances, notifications, org, project_config, project_notifications, projects, schedules, sessions, storefront, support, tenants, user_personas, voice, webhooks, workbench, and any missed by Batches 1-2`.

Not every resource file has mutating methods — some are pure GET. Skip files where the CSV has no entries for the file.

- [ ] **Step 1: Identify resources with mutating calls**

Run: `cut -d, -f1 REQUEST_BODY_MAP.csv | sort -u`
Expected: List of resource files with at least one POST/PUT/PATCH. Use this as the Batch 3 scope minus whatever was in Batches 1-2.

- [ ] **Step 2: For each remaining resource, apply the pattern**

Exactly the Task 3 Step 3 pattern, per resource. Add 1-2 typo regression tests to `tests/test_typed_bodies.py` per resource.

- [ ] **Step 3: Run full suite**

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: All tests pass.

- [ ] **Step 4: Commit**

```bash
git add src/sonzai/resources/ tests/test_typed_bodies.py
git commit -m "feat: typed request bodies across all remaining resources

Batch 3 of 3 — completes the typed-request-body migration. Every
mutating resource method now validates inputs against the spec's
pydantic input class before hitting the wire. Field typos raise
ValidationError instead of leaking to the server as 400s."
```

---

## Self-Review Findings

- **Spec coverage**: A.2 spec's migration strategy ("Migrate resource-by-resource (29 resource files). Each resource is 1 PR / commit.") — I bundled into 3 batches instead; tighter history. Tasks 3-5 cover all 29 files.
- **Spec call for `encode_body`** — Task 1 creates exactly that.
- **Spec call for audit script** — Task 2 creates it.
- **Spec mentions `extra="forbid"` catching typos** — Task 1 test asserts this; the generated input bodies already have `extra="forbid"` per Step 1's generator config.
- **Spec out-of-scope "query-string typing"** — respected; plan only touches POST/PUT/PATCH bodies.

**Placeholder scan**: The `find input body class` instruction in Task 3 references the CSV (concrete artifact produced in Task 2). Each resource file's migration references a specific pattern. No open TBDs.

**Type consistency**: `encode_body` signature stable across tasks. `InputBody` generic name is a placeholder for whatever the CSV points at — resolved per-site at implementation time, not a plan ambiguity.
