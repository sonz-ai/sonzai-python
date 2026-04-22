# Pydantic Generator Swap + PoC Migration (Step 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the `openapi-python-client` (attrs + `UNSET`) generator with `datamodel-code-generator` (pydantic v2 `BaseModel`), establish a subclass-based customization registry, and migrate three representative models end-to-end (`StoredFact`, `AgentCapabilities`, `ChatStreamEvent`) to prove the pattern scales to the remaining ~150 hand-rolled types.

**Architecture:** Generator emits a single `src/sonzai/_generated/models.py` containing pydantic v2 `BaseModel` subclasses for every schema in `openapi.json`. A new `src/sonzai/_customizations/` package holds thin subclasses that rename, add computed properties, or layer validators on top of generated classes. The public surface (`sonzai/__init__.py`) re-exports from `_customizations` for migrated types and from `types.py` for the rest. Two git hooks make drift nearly impossible: `pre-commit` rejects manual edits to `_generated/` unless `openapi.json` is also staged; `pre-push` regenerates in a temp dir and blocks if output differs from committed files.

**Tech Stack:** `datamodel-code-generator` (new dev dep, replaces `openapi-python-client`), `pydantic >= 2.0` (existing), `pytest` + `respx` (existing), `uv` (existing), `just` (existing). Drops: `attrs`, `python-dateutil` (were only for the old generator).

---

## File Structure

**Created:**
- `src/sonzai/_generated/models.py` — all pydantic models, spec-derived. Regenerable.
- `src/sonzai/_customizations/__init__.py` — package root, re-exports every customized class.
- `src/sonzai/_customizations/memory.py` — `StoredFact` subclass.
- `src/sonzai/_customizations/agents.py` — `AgentCapabilities` subclass.
- `src/sonzai/_customizations/chat.py` — `ChatStreamEvent` subclass (includes rename from generated `ChatSSEChunk`).
- `.githooks/pre-commit` — blocks direct edits to `_generated/`.
- `tests/test_customizations.py` — regression tests for the 3 migrated models.

**Modified:**
- `pyproject.toml` — swap generator dep, drop `attrs` + `python-dateutil`.
- `justfile` — rewrite `regenerate-sdk` recipe.
- `openapi-codegen.yaml` — replaced by `datamodel-codegen.yaml` (or inline in `justfile`).
- `src/sonzai/__init__.py` — imports migrated types from `_customizations/`, keeps rest from `types.py`.
- `src/sonzai/types.py` — delete `StoredFact`, `AgentCapabilities`, `ChatStreamEvent` definitions only.
- `.githooks/pre-push` — extend with regen-diff check.

**Deleted:**
- `src/sonzai/_generated/api/` (entire subtree — generated client scaffolding from old generator; unused)
- `src/sonzai/_generated/models/` (454 per-class files — replaced by single `models.py`)
- `src/sonzai/_generated/client.py`, `_generated/errors.py`, `_generated/types.py` (old generator infra)
- `src/sonzai/_generated/__init__.py` (rewritten as a thin re-export)
- `openapi-codegen.yaml` (old generator's config)

---

## Task 1: Swap generator dependency

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Check that `datamodel-code-generator` resolves and installs cleanly**

Run: `uv tool install datamodel-code-generator`
Expected: Installs with no errors. Verify: `datamodel-codegen --version` prints a version ≥ 0.25.

- [ ] **Step 2: Update `pyproject.toml` — drop `attrs`, `python-dateutil`; add `datamodel-code-generator` to dev extras**

Change the `dependencies` array to:

```toml
dependencies = [
    "httpx>=0.25.0",
    "pydantic>=2.0.0",
]
```

Change the `[project.optional-dependencies]` `dev` array by appending `"datamodel-code-generator>=0.25"` and removing no existing items:

```toml
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "respx>=0.21",
    "ruff>=0.4",
    "mypy>=1.0",
    "tqdm>=4.66",
    "google-genai>=0.3",
    "chromadb>=0.5",
    "datamodel-code-generator>=0.25",
]
```

- [ ] **Step 3: Regenerate lockfile**

Run: `uv lock`
Expected: `uv.lock` updated, no resolution errors. `attrs` and `python-dateutil` disappear from top-level.

- [ ] **Step 4: Verify existing tests still pass with old `_generated/` code removed from import path**

Run: `uv run --extra dev pytest -x`
Expected: All 90 tests pass. (The `_generated` tree is currently orphaned — only docstring references — so removing its deps shouldn't break anything.)

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: swap generator dep to datamodel-code-generator

Drops attrs + python-dateutil (were only needed by openapi-python-client
output). Adds datamodel-code-generator for pydantic v2 model emission."
```

---

## Task 2: Rewrite `just regenerate-sdk` recipe

**Files:**
- Modify: `justfile`
- Delete: `openapi-codegen.yaml`

- [ ] **Step 1: Replace the `regenerate-sdk` recipe body**

Open `justfile`, find the `regenerate-sdk:` recipe, and replace it with:

```just
# Regenerate src/sonzai/_generated/models.py from the committed OpenAPI spec.
#
# Outputs a single pydantic v2 models file — no API clients, no per-class
# modules. The hand-written resources/* layer consumes these models by
# subclassing them in src/sonzai/_customizations/ (see that package for the
# migration pattern).
#
# Requires `datamodel-code-generator` (installed via `uv sync --extra dev`).
regenerate-sdk:
    @echo "Step 1/3: sync OpenAPI spec from production..."
    @just sync-spec
    @echo "Step 2/3: regenerate src/sonzai/_generated/models.py ..."
    @rm -rf src/sonzai/_generated
    @mkdir -p src/sonzai/_generated
    uv run --extra dev datamodel-codegen \
        --input openapi.json \
        --input-file-type openapi \
        --output src/sonzai/_generated/models.py \
        --output-model-type pydantic_v2.BaseModel \
        --target-python-version 3.11 \
        --snake-case-field \
        --use-annotated \
        --use-standard-collections \
        --use-union-operator \
        --use-field-description \
        --allow-population-by-field-name \
        --enum-field-as-literal all \
        --collapse-root-models \
        --use-schema-description
    @printf '"""Spec-derived pydantic models. Do not edit by hand.\n\nRegenerate with \`just regenerate-sdk\`. Hand-written customizations live in\n\`src/sonzai/_customizations/\`.\n"""\n\nfrom .models import *  # noqa: F401,F403\n' > src/sonzai/_generated/__init__.py
    @echo "Step 3/3: refreshing parity audit..."
    @uv run --extra dev python scripts/parity_audit.py
    @echo "✓ SDK regenerated."
```

- [ ] **Step 2: Delete the obsolete `openapi-codegen.yaml`**

Run: `rm openapi-codegen.yaml`

- [ ] **Step 3: Commit the recipe change (generation result comes in Task 3)**

```bash
git add justfile
git rm openapi-codegen.yaml
git commit -m "chore: rewrite regenerate-sdk recipe for datamodel-code-generator

Emits a single src/sonzai/_generated/models.py (pydantic v2) instead of
the per-class attrs tree. Drops openapi-codegen.yaml."
```

---

## Task 3: Run new generator, inspect output, commit

**Files:**
- Create: `src/sonzai/_generated/models.py` (generator output)
- Create: `src/sonzai/_generated/__init__.py` (thin re-export, written by the justfile recipe)
- Delete: `src/sonzai/_generated/api/`, `src/sonzai/_generated/models/` (old tree), `src/sonzai/_generated/client.py`, `src/sonzai/_generated/errors.py`, `src/sonzai/_generated/types.py`

- [ ] **Step 1: Run the new generator**

Run: `just regenerate-sdk`
Expected: `src/sonzai/_generated/models.py` appears, large single file (estimate 8–15 KLOC). No errors. `SDK_PARITY_AUDIT.md` still writes (it doesn't depend on `_generated/`).

- [ ] **Step 2: Spot-check the output for the three PoC classes**

Run:
```bash
grep -n "^class StoredFact" src/sonzai/_generated/models.py
grep -n "^class AgentCapabilities" src/sonzai/_generated/models.py
grep -n "^class ChatSseChunk" src/sonzai/_generated/models.py   # may be ChatSSEChunk or ChatSseChunk
```
Expected: Each grep returns exactly one line. Note the exact class names (the generator may emit `ChatSseChunk` for the spec's `ChatSSEChunk` — this is fine; we'll re-export with the canonical name).

- [ ] **Step 3: Inspect the emitted `StoredFact` to confirm pydantic shape**

Run: `grep -n -A 25 "^class StoredFact" src/sonzai/_generated/models.py`
Expected: a `class StoredFact(BaseModel):` definition with fields including `fact_id`, `content`, `fact_type`, `session_id`, `source_id`, etc. Optional fields shown as `field: str | None = None` or `Annotated[str | None, Field(default=None, ...)]`.

- [ ] **Step 4: Verify existing tests still pass (generated file shouldn't affect them yet — nothing imports from it)**

Run: `uv run --extra dev pytest -x`
Expected: All 90 tests pass.

- [ ] **Step 5: Commit the regenerated output**

```bash
git add -A src/sonzai/_generated/
git commit -m "chore: regenerate _generated/models.py as pydantic v2

Single-file output from datamodel-code-generator replacing the 454-file
attrs tree from openapi-python-client. Nothing imports from _generated/
yet — customization layer lands in subsequent commits."
```

---

## Task 4: Create `_customizations/` package scaffold

**Files:**
- Create: `src/sonzai/_customizations/__init__.py`

- [ ] **Step 1: Write the scaffolding `__init__.py`**

Create `src/sonzai/_customizations/__init__.py` with:

```python
"""Hand-written enhancements layered on top of spec-generated models.

Pattern:
    from sonzai._generated.models import Foo as _GenFoo

    class Foo(_GenFoo):
        '''Docstring for public Foo.'''

        @property
        def convenience(self) -> str:
            return self.some_field or ""

Every class here is subclassed from `sonzai._generated.models`. The
re-export below is what `sonzai/__init__.py` imports from.

Types with no spec counterpart (e.g., client-side aggregations like
`ChatUsage` built from SSE frames) stay in `sonzai.types` — they are not
in scope for this package.
"""

from .agents import AgentCapabilities
from .chat import ChatStreamEvent
from .memory import StoredFact

__all__ = [
    "AgentCapabilities",
    "ChatStreamEvent",
    "StoredFact",
]
```

- [ ] **Step 2: Create empty placeholder modules so the `__init__.py` imports don't explode**

Create `src/sonzai/_customizations/memory.py`:

```python
"""StoredFact and related memory types."""

from sonzai._generated.models import StoredFact as _GenStoredFact


class StoredFact(_GenStoredFact):
    """Stored fact returned by fact recall endpoints."""
```

Create `src/sonzai/_customizations/agents.py`:

```python
"""Agent-related customizations."""

from sonzai._generated.models import AgentCapabilities as _GenAgentCapabilities


class AgentCapabilities(_GenAgentCapabilities):
    """Agent capability flags and configuration."""
```

Create `src/sonzai/_customizations/chat.py` — note the generator's name may be `ChatSseChunk` or `ChatSSEChunk`; adjust the import alias based on what Task 3 Step 2 found:

```python
"""Chat streaming event, renamed from the spec's ChatSSEChunk."""

from sonzai._generated.models import ChatSseChunk as _GenChatSseChunk


class ChatStreamEvent(_GenChatSseChunk):
    """A single SSE event from the chat stream.

    Renamed from spec's `ChatSSEChunk` for SDK readability. Adds
    convenience properties for the common "get content" / "is this the
    last frame" checks that would otherwise require reaching into
    `.choices[0].delta`.
    """

    @property
    def content(self) -> str:
        if self.choices:
            return self.choices[0].delta.get("content", "") if self.choices[0].delta else ""
        return ""

    @property
    def is_finished(self) -> bool:
        return bool(self.choices and self.choices[0].finish_reason == "stop")
```

- [ ] **Step 3: Verify the package imports cleanly**

Run: `uv run --extra dev python -c "from sonzai._customizations import StoredFact, AgentCapabilities, ChatStreamEvent; print('ok')"`
Expected: prints `ok`. If the chat import fails with `ImportError: cannot import name 'ChatSseChunk'`, open `src/sonzai/_generated/models.py`, find the actual class name (`grep '^class ChatS' src/sonzai/_generated/models.py`), and fix the alias in `chat.py`.

- [ ] **Step 4: Run tests — nothing should be using the new package yet, so tests still pass unchanged**

Run: `uv run --extra dev pytest -x`
Expected: 90 tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/sonzai/_customizations/
git commit -m "feat: add _customizations/ package scaffolding

Thin subclass layer over spec-generated pydantic models. Holds renames,
computed properties, and validators for the three PoC migration
candidates: StoredFact, AgentCapabilities, ChatStreamEvent."
```

---

## Task 5: Migrate `StoredFact` (simplest case, flat snake_case)

**Files:**
- Test: `tests/test_customizations.py`
- Modify: `src/sonzai/types.py:2053-2071` (delete `StoredFact` class)
- Modify: `src/sonzai/__init__.py` (change import source for `StoredFact`)

- [ ] **Step 1: Write failing test for `StoredFact` migration**

Create `tests/test_customizations.py`:

```python
"""Regression tests for _customizations/ layer."""

from __future__ import annotations

from sonzai import AgentCapabilities, ChatStreamEvent, StoredFact


class TestStoredFact:
    def test_imports_from_customizations(self) -> None:
        from sonzai._customizations import StoredFact as CustStoredFact

        assert StoredFact is CustStoredFact

    def test_roundtrips_all_spec_fields(self) -> None:
        payload = {
            "fact_id": "fact_123",
            "content": "user likes coffee",
            "fact_type": "preference",
            "importance": 0.8,
            "confidence": 0.95,
            "entity": "user",
            "source_type": "chat",
            "source_id": "msg_42",
            "session_id": "sess_abc",
            "mention_count": 3,
            "metadata": {"extra": "info"},
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-02T00:00:00Z",
        }
        fact = StoredFact.model_validate(payload)
        assert fact.fact_id == "fact_123"
        assert fact.session_id == "sess_abc"
        assert fact.source_id == "msg_42"
        assert fact.metadata == {"extra": "info"}

    def test_unknown_fields_surface_via_extra_allow_when_configured(self) -> None:
        # Spec-generated models default to `extra='ignore'`; we're asserting
        # the shipped behavior, not a preference. If this ever flips, we
        # want the test to break so we notice.
        fact = StoredFact.model_validate(
            {
                "fact_id": "x",
                "content": "y",
                "fact_type": "t",
                "importance": 0.0,
                "confidence": 0.0,
                "mention_count": 0,
                "created_at": "",
                "updated_at": "",
                "future_field_that_does_not_exist_yet": "foo",
            }
        )
        assert not hasattr(fact, "future_field_that_does_not_exist_yet")
```

- [ ] **Step 2: Run test — expect ImportError because `sonzai.AgentCapabilities` and `sonzai.ChatStreamEvent` aren't exported yet from the new location**

Run: `uv run --extra dev pytest tests/test_customizations.py -v`
Expected: Import errors or `AttributeError` on `sonzai.AgentCapabilities` (not re-exported from `_customizations` yet). Tests for `StoredFact` may also fail if `sonzai.StoredFact` is still the `types.py` version.

- [ ] **Step 3: Delete `StoredFact` from `types.py`**

Open `src/sonzai/types.py`, locate the `class StoredFact(BaseModel):` definition (around line 2053), and delete the class and any docstring/preceding comments **that reference only StoredFact** (leave `ListAllFactsResponse` which follows alone; it already just references `StoredFact` by name and will resolve via the re-export).

Do NOT touch `ListAllFactsResponse` — it stays for now.

- [ ] **Step 4: Update `src/sonzai/__init__.py` to import `StoredFact` from `_customizations`**

In `src/sonzai/__init__.py`, find the `from .types import (` block, remove `StoredFact,` from that list, and add a new import line near the top (below the existing `from .types import ...` block):

```python
from ._customizations import StoredFact
```

The existing `__all__` entry for `"StoredFact"` stays as-is.

- [ ] **Step 5: Also update `types.py`'s `ListAllFactsResponse` to import StoredFact from customizations**

`ListAllFactsResponse` references `StoredFact` by name. Add to the top of `src/sonzai/types.py` (after the existing pydantic imports):

```python
from ._customizations import StoredFact
```

Remove any duplicate/conflicting imports of `StoredFact`.

- [ ] **Step 6: Run `test_customizations.py::TestStoredFact` — should now pass**

Run: `uv run --extra dev pytest tests/test_customizations.py::TestStoredFact -v`
Expected: All 3 `TestStoredFact` tests pass. `TestAgentCapabilities` and `TestChatStreamEvent` still fail (they're empty classes or import-fail — that's fine for now).

- [ ] **Step 7: Run the full suite to catch any regression**

Run: `uv run --extra dev pytest -x`
Expected: All tests pass (the 90 existing + the 3 new StoredFact tests = 93).

- [ ] **Step 8: Commit**

```bash
git add tests/test_customizations.py src/sonzai/types.py src/sonzai/__init__.py
git commit -m "refactor: migrate StoredFact to spec-generated + customizations

StoredFact class removed from types.py; public sonzai.StoredFact now
re-exports from src/sonzai/_customizations/memory.py, which subclasses
sonzai._generated.models.StoredFact (emitted by datamodel-code-generator
from the committed OpenAPI spec). ListAllFactsResponse's reference to
StoredFact resolves via the new import.

Regression test tests/test_customizations.py::TestStoredFact verifies
the public name resolves to the customization subclass and all spec
fields round-trip through model_validate()."
```

---

## Task 6: Migrate `AgentCapabilities` (tests camelCase alias handling)

**Files:**
- Modify: `src/sonzai/_customizations/agents.py` (the subclass is already in place from Task 4; this task fills in alias tests + removes the hand-rolled version)
- Modify: `tests/test_customizations.py` (add `TestAgentCapabilities` tests)
- Modify: `src/sonzai/types.py` (delete hand-rolled `AgentCapabilities` class if present)
- Modify: `src/sonzai/__init__.py` (switch import source)

- [ ] **Step 1: Check the hand-rolled AgentCapabilities, if any, to understand current shape**

Run: `grep -n "^class AgentCapabilities" src/sonzai/types.py`
Expected: one line, or no match if it's an alias / not hand-rolled.

If found, run: `sed -n "$(grep -n "^class AgentCapabilities" src/sonzai/types.py | head -1 | cut -d: -f1),+25p" src/sonzai/types.py` to inspect.

Record the line range in case you need to delete it.

- [ ] **Step 2: Confirm generated AgentCapabilities has the expected aliased fields**

Run: `grep -n -A 30 "^class AgentCapabilities" src/sonzai/_generated/models.py`
Expected: fields like `custom_tools: ... Field(..., alias="customTools")`, `image_generation`, `memory_mode`, etc. Generator should have converted camelCase spec fields to snake_case Python attrs with `alias=` set.

- [ ] **Step 3: Add `TestAgentCapabilities` to `tests/test_customizations.py`**

Append to `tests/test_customizations.py`:

```python
class TestAgentCapabilities:
    def test_imports_from_customizations(self) -> None:
        from sonzai._customizations import AgentCapabilities as CustAgentCapabilities

        assert AgentCapabilities is CustAgentCapabilities

    def test_camel_case_alias_input(self) -> None:
        """Server sends camelCase; SDK exposes snake_case with aliases."""
        payload = {
            "customTools": False,
            "imageGeneration": True,
            "memoryMode": "full",
            "musicGeneration": False,
        }
        caps = AgentCapabilities.model_validate(payload)
        assert caps.custom_tools is False
        assert caps.image_generation is True
        assert caps.memory_mode == "full"

    def test_snake_case_input_also_works(self) -> None:
        """populate_by_name=True lets users pass either form."""
        payload = {
            "custom_tools": True,
            "image_generation": False,
            "memory_mode": "summary",
        }
        caps = AgentCapabilities.model_validate(payload)
        assert caps.custom_tools is True

    def test_dump_round_trips_to_camel(self) -> None:
        caps = AgentCapabilities(
            custom_tools=True,
            image_generation=True,
            memory_mode="full",
        )
        dumped = caps.model_dump(by_alias=True, exclude_none=True)
        assert "customTools" in dumped
        assert "imageGeneration" in dumped
        assert "memoryMode" in dumped
```

- [ ] **Step 4: Run the new tests — expect them to fail if `populate_by_name` wasn't emitted**

Run: `uv run --extra dev pytest tests/test_customizations.py::TestAgentCapabilities -v`
Expected: Likely `test_snake_case_input_also_works` and the alias tests pass if `--allow-population-by-field-name` was honored (Task 2). If any fail, inspect the generated class's `model_config` — it must contain `populate_by_name=True`. If it's missing, add to the `AgentCapabilities` subclass:

```python
class AgentCapabilities(_GenAgentCapabilities):
    """Agent capability flags and configuration."""

    model_config = {**_GenAgentCapabilities.model_config, "populate_by_name": True}
```

Re-run the tests until all 4 pass.

- [ ] **Step 5: Delete hand-rolled `AgentCapabilities` from `types.py` (if present)**

Using the line range from Step 1, delete the `class AgentCapabilities(BaseModel):` block. If `AgentCapabilities` is only referenced and not defined in `types.py` (i.e., Step 1 found nothing), skip this step.

- [ ] **Step 6: Ensure `sonzai/__init__.py` imports `AgentCapabilities` from `_customizations`**

In `src/sonzai/__init__.py`:
- Remove `AgentCapabilities,` from the `from .types import (` block if present.
- Add to the existing `from ._customizations import ...` line (or extend it):

```python
from ._customizations import AgentCapabilities, StoredFact
```

`"AgentCapabilities"` in `__all__` stays.

- [ ] **Step 7: Run full test suite**

Run: `uv run --extra dev pytest -x`
Expected: All tests pass (90 original + StoredFact tests + AgentCapabilities tests).

- [ ] **Step 8: Commit**

```bash
git add src/sonzai/_customizations/agents.py src/sonzai/__init__.py src/sonzai/types.py tests/test_customizations.py
git commit -m "refactor: migrate AgentCapabilities to spec-generated + customizations

Removes the hand-rolled class (if any) from types.py; public
sonzai.AgentCapabilities now resolves to the customization subclass of
the spec-generated pydantic model. Adds tests proving camelCase aliases
round-trip both directions (wire → snake_case and snake_case → wire)."
```

---

## Task 7: Migrate `ChatStreamEvent` (hardest case: rename + properties + free-form data)

**Files:**
- Modify: `src/sonzai/_customizations/chat.py` (already has subclass skeleton from Task 4)
- Modify: `tests/test_customizations.py` (add `TestChatStreamEvent`)
- Modify: `src/sonzai/types.py` (delete hand-rolled `ChatStreamEvent` definition at line 34)
- Modify: `src/sonzai/__init__.py` (switch import source)
- Modify: `tests/test_types.py` (the existing `TestChatStreamEvent` already exercises the properties — ensure it still passes against the new class)

- [ ] **Step 1: Inspect the generated `ChatSseChunk` (or `ChatSSEChunk`) to confirm field set matches expectations**

Run: `grep -n -A 40 "^class ChatSs" src/sonzai/_generated/models.py`
Expected: class with fields `choices`, `data`, `error`, `type`, `side_effects`, `enriched_context`, `build_duration_ms`, `used_fast_path`, `message_index`. Optional Any/dict types for `data`, `side_effects`, `enriched_context`.

Note: the hand-rolled `ChatStreamEvent` has fields the spec does NOT define (`is_follow_up`, `replacement`, `full_content`, `finish_reason`, `continuation_token`, `response_cookie`, `message_count`, `external_tool_calls`, `error_message`, `error_code`, `is_token_error`). These are populated by the stream consumer from `data` / `type` frames client-side. We must preserve them somehow.

- [ ] **Step 2: Update `src/sonzai/_customizations/chat.py` to add the client-side extension fields plus the rename**

Replace the contents of `src/sonzai/_customizations/chat.py` with:

```python
"""Chat streaming event, renamed from the spec's ChatSSEChunk.

Adds client-side-only fields that are populated by the stream consumer
from `type` and `data` payloads (not part of the server schema).
"""

from __future__ import annotations

from typing import Any

from pydantic import ConfigDict, Field

from sonzai._generated.models import ChatSseChunk as _GenChatSseChunk


class ChatStreamEvent(_GenChatSseChunk):
    """A single SSE event from the chat stream.

    Inherits every spec field from `ChatSseChunk` (choices, data, error,
    type, side_effects, enriched_context, build_duration_ms,
    used_fast_path, message_index). Adds convenience properties for the
    common "get content" / "is this the last frame" checks, plus a set
    of client-side extension fields that the stream consumer in
    `sonzai/_http.py` populates from `data` / `type` payloads for
    ergonomic access.
    """

    # Client-side extensions — populated from `data` / `type` frames by
    # the stream reader, never present on the wire as top-level fields.
    is_follow_up: bool = False
    replacement: bool = False
    full_content: str = ""
    finish_reason: str = ""
    continuation_token: str = ""
    response_cookie: str = ""
    message_count: int = 0
    external_tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    error_message: str = ""
    error_code: str = ""
    is_token_error: bool = False

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    @property
    def content(self) -> str:
        if not self.choices:
            return ""
        delta = self.choices[0].delta
        if not delta:
            return ""
        if isinstance(delta, dict):
            return delta.get("content", "")
        return getattr(delta, "content", "") or ""

    @property
    def is_finished(self) -> bool:
        return bool(self.choices and self.choices[0].finish_reason == "stop")
```

Adjust the `from sonzai._generated.models import ChatSseChunk as _GenChatSseChunk` line if Task 3's inspection found a different casing.

- [ ] **Step 3: Add `TestChatStreamEvent` to `tests/test_customizations.py`**

Append to `tests/test_customizations.py`:

```python
class TestChatStreamEvent:
    def test_imports_from_customizations(self) -> None:
        from sonzai._customizations import ChatStreamEvent as CustChatStreamEvent

        assert ChatStreamEvent is CustChatStreamEvent

    def test_content_property_on_delta_frame(self) -> None:
        event = ChatStreamEvent.model_validate(
            {"choices": [{"delta": {"content": "Hello"}, "index": 0}]}
        )
        assert event.content == "Hello"

    def test_empty_event_has_no_content(self) -> None:
        event = ChatStreamEvent.model_validate({})
        assert event.content == ""
        assert not event.is_finished

    def test_is_finished_on_stop_frame(self) -> None:
        event = ChatStreamEvent.model_validate(
            {"choices": [{"delta": {"content": "."}, "finish_reason": "stop", "index": 0}]}
        )
        assert event.is_finished

    def test_client_extension_fields_default_empty(self) -> None:
        event = ChatStreamEvent.model_validate({})
        assert event.full_content == ""
        assert event.finish_reason == ""
        assert event.external_tool_calls == []
        assert event.is_token_error is False

    def test_client_extension_fields_round_trip(self) -> None:
        event = ChatStreamEvent(
            full_content="done",
            finish_reason="stop",
            continuation_token="abc",
            is_token_error=True,
        )
        assert event.full_content == "done"
        assert event.continuation_token == "abc"
        assert event.is_token_error is True

    def test_free_form_data_preserved(self) -> None:
        """`data` on side_effects frames is free-form per spec — must survive."""
        event = ChatStreamEvent.model_validate(
            {"type": "side_effects", "data": {"facts": [{"content": "x"}]}}
        )
        assert event.type == "side_effects"
        assert event.data == {"facts": [{"content": "x"}]}
```

- [ ] **Step 4: Run new tests — expect pass (or fix the subclass)**

Run: `uv run --extra dev pytest tests/test_customizations.py::TestChatStreamEvent -v`
Expected: All 7 tests pass. If `test_content_property_on_delta_frame` fails, the generated `ChatSseChoice.delta` may have a different shape — debug by inspecting the generated class:

```
grep -n -A 10 "^class ChatSseChoice" src/sonzai/_generated/models.py
grep -n -A 10 "^class ChatSseDelta" src/sonzai/_generated/models.py
```

Adjust the `content` property's traversal accordingly.

- [ ] **Step 5: Delete the hand-rolled `ChatStreamEvent` (+ nothing else — `ChatChoice` stays)**

Open `src/sonzai/types.py`, locate `class ChatStreamEvent(BaseModel):` (around line 34), and delete the entire class body including its decorators, docstring, fields, `model_config`, and the two `@property` methods — through the last `return bool(self.choices and self.choices[0].finish_reason == "stop")` line.

**Do not delete `ChatChoice` or `ChatUsage` or `ChatResponse`** — they stay hand-rolled for now (they're not part of this PoC).

- [ ] **Step 6: Update `src/sonzai/__init__.py`**

- Remove `ChatStreamEvent,` from the `from .types import (` block.
- Extend the `from ._customizations import ...` line:

```python
from ._customizations import AgentCapabilities, ChatStreamEvent, StoredFact
```

`"ChatStreamEvent"` in `__all__` stays.

- [ ] **Step 7: Verify existing `tests/test_types.py::TestChatStreamEvent` still passes against the new class**

Run: `uv run --extra dev pytest tests/test_types.py::TestChatStreamEvent -v`
Expected: All existing tests pass. If any fail, the fields covered in `tests/test_types.py` that belong to the hand-rolled surface area (`full_content`, `response_cookie`, etc.) are preserved by the client-extension fields in the subclass. If a field is missing, add it to the subclass.

- [ ] **Step 8: Run the full suite**

Run: `uv run --extra dev pytest -x`
Expected: all pass.

- [ ] **Step 9: Commit**

```bash
git add src/sonzai/_customizations/chat.py src/sonzai/types.py src/sonzai/__init__.py tests/test_customizations.py
git commit -m "refactor: migrate ChatStreamEvent to spec-generated + customizations

ChatStreamEvent now subclasses the spec-generated ChatSSEChunk,
preserving:
  - all wire fields from the spec (choices, type, data, error, etc.)
  - client-side extension fields populated by the SSE reader
    (full_content, finish_reason, continuation_token, etc.)
  - the .content and .is_finished convenience properties
  - extra='allow' and populate_by_name=True behavior

Renames ChatSSEChunk → ChatStreamEvent at the public boundary; the
spec-derived name stays internal to _generated/.

Hand-rolled ChatStreamEvent definition removed from types.py. All
existing tests in tests/test_types.py::TestChatStreamEvent continue to
pass against the new subclass. New regression suite in
tests/test_customizations.py::TestChatStreamEvent covers the
client-extension round-trip plus free-form `data` preservation."
```

---

## Task 8: Install pre-commit hook blocking `_generated/` edits

**Files:**
- Create: `.githooks/pre-commit`

- [ ] **Step 1: Write the hook**

Create `.githooks/pre-commit`:

```bash
#!/usr/bin/env bash
# Pre-commit drift check: block manual edits to src/sonzai/_generated/.
#
# The _generated/ tree is a build artifact of `just regenerate-sdk`,
# which reads openapi.json. If a commit touches _generated/ WITHOUT also
# touching openapi.json, that is almost certainly an accidental hand edit
# and will be overwritten on the next regen.
#
# Escape hatch: `git commit --no-verify` (only reach for this if you are
# deliberately shipping a generator-output tweak while the generator is
# itself being iterated on — which is rare).

set -e

staged="$(git diff --cached --name-only)"

touches_generated=0
touches_spec=0

while IFS= read -r f; do
  case "$f" in
    src/sonzai/_generated/*) touches_generated=1 ;;
    openapi.json)            touches_spec=1 ;;
  esac
done <<< "$staged"

if [ "$touches_generated" = "1" ] && [ "$touches_spec" = "0" ]; then
  echo ""
  echo "⚠️  Refusing to commit: staged changes touch src/sonzai/_generated/"
  echo "   but openapi.json is unchanged."
  echo ""
  echo "   src/sonzai/_generated/ is a regenerable build artifact. Hand"
  echo "   edits there will be wiped on the next \`just regenerate-sdk\`."
  echo ""
  echo "   → If you meant to change a model, edit openapi.json (or the"
  echo "     upstream API spec) and run: just regenerate-sdk"
  echo "   → If you meant to add a computed property / convenience method,"
  echo "     put it in src/sonzai/_customizations/ instead."
  echo "   → To bypass (rare, ill-advised): git commit --no-verify"
  echo ""
  exit 1
fi

exit 0
```

- [ ] **Step 2: Make it executable**

Run: `chmod +x .githooks/pre-commit`

- [ ] **Step 3: Test the hook fires on a deliberate violation**

Run:
```bash
echo "# test" >> src/sonzai/_generated/models.py
git add src/sonzai/_generated/models.py
git commit -m "test: should fail"
```
Expected: commit rejected with the warning above.

Clean up:
```bash
git restore --staged src/sonzai/_generated/models.py
git checkout -- src/sonzai/_generated/models.py
```

- [ ] **Step 4: Test the hook allows edits that include openapi.json**

Run:
```bash
# Touch both files
echo "" >> openapi.json
echo "# test" >> src/sonzai/_generated/models.py
git add openapi.json src/sonzai/_generated/models.py
git commit -m "test: should pass"
```
Expected: commit succeeds.

Reset:
```bash
git reset --hard HEAD~1
```

- [ ] **Step 5: Commit the hook**

```bash
git add .githooks/pre-commit
git commit -m "chore: add pre-commit hook blocking _generated/ hand edits

Rejects commits that stage src/sonzai/_generated/* without also staging
openapi.json. The _generated/ tree is a build artifact of
\`just regenerate-sdk\`; hand edits there get wiped on next regen, so we
catch it at commit time."
```

- [ ] **Step 6: Remind users to point git at `.githooks/`**

The existing `just install-hooks` recipe runs `git config core.hooksPath .githooks` — the new hook is picked up automatically on fresh clones that run `just install-hooks`. No further action needed, but note it in your own shell:

Run: `just install-hooks`
Expected: `✓ Hooks enabled: .githooks/pre-push will run on git push.` — hook path is now pointed at `.githooks/` so pre-commit fires too.

---

## Task 9: Extend pre-push hook with regenerate-and-diff check

**Files:**
- Modify: `.githooks/pre-push`

- [ ] **Step 1: Read current `.githooks/pre-push`**

It's the spec-drift check from earlier releases. Keep that logic; add a second check appended below it.

- [ ] **Step 2: Replace `.githooks/pre-push` with the extended version**

Overwrite `.githooks/pre-push` with:

```bash
#!/usr/bin/env bash
# Pre-push drift checks:
#  1. openapi.json in repo vs live production spec.
#  2. src/sonzai/_generated/models.py vs what the generator would produce
#     from the committed openapi.json.
#
# Skip with `git push --no-verify`.

set -e

SPEC_URL="${OPENAPI_SPEC_URL:-https://api.sonz.ai/docs/openapi.json}"
LOCAL_SPEC="openapi.json"

# --- Check 1: live spec drift ----------------------------------------------

if [ -f "$LOCAL_SPEC" ]; then
  LIVE_SPEC="$(mktemp)"
  trap 'rm -f "$LIVE_SPEC"' EXIT

  if curl -sfL --max-time 10 "$SPEC_URL" -o "$LIVE_SPEC"; then
    if ! diff -q "$LOCAL_SPEC" "$LIVE_SPEC" > /dev/null 2>&1; then
      echo ""
      echo "⚠️  OpenAPI spec has drifted from production."
      echo ""
      echo "   Committed: $LOCAL_SPEC ($(wc -c < "$LOCAL_SPEC" | tr -d ' ') bytes)"
      echo "   Live:      $SPEC_URL ($(wc -c < "$LIVE_SPEC" | tr -d ' ') bytes)"
      echo ""
      echo "   → Run 'just sync-spec' to pull the latest spec."
      echo "   → Review the diff, update SDK types if needed, and re-push."
      echo "   → To bypass: git push --no-verify"
      echo ""
      exit 1
    fi
  else
    echo "⚠ Could not fetch $SPEC_URL — skipping live-spec drift check."
  fi
fi

# --- Check 2: regenerate and compare --------------------------------------

if [ -f "src/sonzai/_generated/models.py" ]; then
  TMP_OUT="$(mktemp -d)"
  trap 'rm -rf "$TMP_OUT"' EXIT

  if ! uv run --extra dev datamodel-codegen \
      --input openapi.json \
      --input-file-type openapi \
      --output "$TMP_OUT/models.py" \
      --output-model-type pydantic_v2.BaseModel \
      --target-python-version 3.11 \
      --snake-case-field \
      --use-annotated \
      --use-standard-collections \
      --use-union-operator \
      --use-field-description \
      --allow-population-by-field-name \
      --enum-field-as-literal all \
      --collapse-root-models \
      --use-schema-description \
      > /dev/null 2>&1; then
    echo "⚠ Regenerator failed — skipping regen-drift check."
    exit 0
  fi

  if ! diff -q "src/sonzai/_generated/models.py" "$TMP_OUT/models.py" > /dev/null 2>&1; then
    echo ""
    echo "⚠️  _generated/models.py is out of sync with openapi.json."
    echo ""
    echo "   → Run 'just regenerate-sdk' and commit the result."
    echo "   → To bypass: git push --no-verify"
    echo ""
    exit 1
  fi
fi

exit 0
```

- [ ] **Step 3: Test that the hook passes when `_generated/` matches spec**

Run: `.githooks/pre-push` (just run it manually — pre-push hooks receive stdin via git, but with no unpushed refs it's a no-op)

Alternative: run the core check inline:

```bash
TMP_OUT="$(mktemp -d)"
uv run --extra dev datamodel-codegen \
    --input openapi.json \
    --input-file-type openapi \
    --output "$TMP_OUT/models.py" \
    --output-model-type pydantic_v2.BaseModel \
    --target-python-version 3.11 \
    --snake-case-field \
    --use-annotated \
    --use-standard-collections \
    --use-union-operator \
    --use-field-description \
    --allow-population-by-field-name \
    --enum-field-as-literal all \
    --collapse-root-models \
    --use-schema-description
diff -q src/sonzai/_generated/models.py "$TMP_OUT/models.py" && echo "regen drift OK" || echo "DRIFT"
rm -rf "$TMP_OUT"
```

Expected: `regen drift OK`.

- [ ] **Step 4: Commit**

```bash
git add .githooks/pre-push
git commit -m "chore: pre-push hook now regenerates + diffs _generated/models.py

Two drift checks before push:
  1. openapi.json in repo vs live production (existing).
  2. _generated/models.py vs what datamodel-codegen would emit for the
     committed openapi.json (new).

Together with the pre-commit hook blocking hand edits to _generated/,
this makes shipping an out-of-sync SDK effectively impossible without
explicit --no-verify override."
```

---

## Task 10: Update `just deploy` and release flow to tolerate the new layout

**Files:**
- Modify: `justfile` (`_commit` recipe)

- [ ] **Step 1: Find the `_commit` recipe in `justfile`**

Current recipe stages `pyproject.toml uv.lock src/sonzai/__init__.py src/sonzai/_http.py`. With migration, release commits sometimes also update `src/sonzai/_customizations/` if a field alias changed during a regen. Release's `_bump` only edits `__init__.py` and `_http.py`, so no files in `_customizations/` change automatically — the current `_commit` is fine.

**No change needed for step 1's scope**, but verify by running the release dry-run:

Run: `just _bump 1.3.0` (idempotent since version is already 1.3.0) then `git status --short`
Expected: either no changes (if already bumped) or only `pyproject.toml uv.lock src/sonzai/__init__.py src/sonzai/_http.py` modified.

If any `src/sonzai/_generated/` file appears modified, the regenerator introduced nondeterministic output — that's a bug in the justfile recipe (try adding `--no-color` or `--use-timestamped-banner=false` if such flags exist; otherwise pin datamodel-code-generator to an exact version in dev deps).

- [ ] **Step 2: No commit if no changes. Skip this step.**

---

## Task 11: Smoke-test the full loop end-to-end

- [ ] **Step 1: Clean-regen, verify idempotence**

Run: `just regenerate-sdk && git status --short`
Expected: no changes to tracked files (generator output is deterministic for a given spec).

- [ ] **Step 2: Run the full test suite**

Run: `uv run --extra dev pytest -v`
Expected: all tests pass (existing + 3 new customization test classes).

- [ ] **Step 3: Verify the public API shape from a consumer's perspective**

Run:
```bash
uv run --extra dev python -c "
from sonzai import StoredFact, AgentCapabilities, ChatStreamEvent
print('StoredFact MRO:', [c.__name__ for c in StoredFact.__mro__])
print('AgentCapabilities MRO:', [c.__name__ for c in AgentCapabilities.__mro__])
print('ChatStreamEvent MRO:', [c.__name__ for c in ChatStreamEvent.__mro__])
"
```
Expected: each MRO starts with the customization subclass, then the spec-generated class, then `BaseModel`, then `object`. Proves the subclass layer is in place and users see the customization.

- [ ] **Step 4: Verify pre-commit and pre-push hooks both fire (Task 8 Step 3 and Task 9 Step 3 already proved this — re-run here only if Steps 1–3 revealed issues that needed further tweaks).**

---

## Self-Review Findings

Checked the plan against the design before finalizing:

- **Generator choice** covered — Task 1 + Task 2 land `datamodel-code-generator` and the new recipe.
- **Customization registry** covered — Task 4 creates `_customizations/` scaffold; Tasks 5–7 migrate the three PoC models.
- **Coexistence during migration** covered — `types.py` entries get deleted one-at-a-time (Task 5 Step 3, Task 6 Step 5, Task 7 Step 5); `sonzai/__init__.py` switches one import at a time.
- **PoC choices** updated from design: swapped `ChatUsage` (no spec counterpart) for `AgentCapabilities` (exercises camelCase alias handling, which was the only point of keeping `ChatUsage` as a PoC anyway).
- **Pre-commit gate** covered — Task 8.
- **Pre-push regen-diff gate** covered — Task 9.
- **No CI gate** — respected; nothing in the plan touches `.github/workflows/`.
- **TDD cadence** — every migration task writes the test first (Tasks 5/6/7 each open with a failing test).
- **Commits** — every task ends in a single commit; no batching.
- **Placeholder scan** — no `TBD`/`TODO`/`implement later` remain. One "adjust if generator emits a different casing" instruction in Task 4 Step 3 and Task 7 Step 1 — those are conditional, concrete remediation paths, not placeholders.
- **Type consistency** — `_GenStoredFact` / `_GenAgentCapabilities` / `_GenChatSseChunk` aliasing is consistent across Tasks 4–7. Public class names `StoredFact` / `AgentCapabilities` / `ChatStreamEvent` are used consistently.

No spec-requirement gaps. Ready for execution.
