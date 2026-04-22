# Step 3 A.2: Typed Request Bodies Design

**Goal:** Eliminate loose `dict[str, Any]` / `**kwargs` on resource methods by routing every request body through a spec-derived typed model. A field typo (`uesr_id="x"`) should fail at import time (mypy) or at runtime (pydantic) instead of silently reaching the server and 400-ing with an opaque "unknown field".

**Architecture:** `datamodel-code-generator` already emits every `*InputBody` / request-body schema as a pydantic class in `src/sonzai/_generated/models.py`. Resource methods accept **typed kwargs + `**extra`** — they construct the input body via `SomeInputBody.model_validate({...})` internally, then `.model_dump(by_alias=True, exclude_none=True)` for the wire. Hand-written kwargs signatures remain the public API; the typed body becomes an internal validation gate.

**Tech Stack:** pydantic v2 input bodies (already generated), no new deps. mypy already `strict=true` — typed kwargs get checked at the call site too.

---

## Current pain

```python
# types nothing, typos silent
client.agents.chat(agent_id="x", mesages=[...])  # typo → 400
client.memory.add(user_id="x", contnet="...")    # typo → 400
```

Resource methods today:
```python
def chat(self, agent_id: str, *, messages: list[dict], **kwargs) -> ChatResponse:
    body = {"messages": messages, **kwargs}  # no validation
    return ChatResponse.model_validate(self._http.post(f"/agents/{agent_id}/chat", body=body))
```

## What users get

```python
# Typos caught by mypy + pydantic:
client.agents.chat(agent_id="x", mesages=[])     # mypy error at call site
client.memory.add(user_id="x", contnet="...")    # pydantic ValidationError at runtime
```

Method signatures stay as they are (snake_case typed kwargs) — we're adding an internal gate, not restructuring the public API.

## Implementation pattern

For each resource method, identify the spec's input body class (e.g., `ChatInputBody`, `AddFactRequest`) by:
1. Looking up the `operationId` or path+method in `openapi.json`.
2. Finding the `requestBody.content.application/json.schema.$ref` → `_generated.models.<ClassName>`.

The method body changes from:
```python
body = {"messages": messages, "user_id": user_id, **kwargs}
data = self._http.post(path, body=body)
```
to:
```python
from sonzai._generated.models import ChatInputBody

validated = ChatInputBody.model_validate(
    {"messages": messages, "user_id": user_id, **kwargs}
)
data = self._http.post(path, body=validated.model_dump(by_alias=True, exclude_none=True))
```

The pydantic class enforces:
- Every field exists (unknown keys → `ValidationError`).
- Required fields are provided.
- Types match (e.g., `messages: list[ChatMessage]`).
- Aliases (camelCase wire ↔ snake_case Python) round-trip cleanly.

## Helper module (`src/sonzai/_request_helpers.py`)

A tiny helper to DRY the pattern:
```python
def encode_body(model_cls: type[BaseModel], data: dict) -> dict:
    """Validate data against model_cls and return a wire-format dict."""
    validated = model_cls.model_validate(data)
    return validated.model_dump(by_alias=True, exclude_none=True)
```

Each resource method calls `encode_body(ChatInputBody, {...})`. One-liner replacement across ~200 sites.

## Inventory: which resources need which InputBody

A small audit script (`scripts/request_body_map.py`) walks `resources/*.py` and `openapi.json` to produce a CSV of `(resource_file, method_name, http_verb, path, input_body_class)`. This is the task list for the migration.

Early spot-check: most resources use a handful of input body classes. Some methods (e.g., `GET` queries with no body, `DELETE` without body) skip this migration entirely.

## Migration strategy

Migrate resource-by-resource (29 resource files). Each resource is 1 PR / commit. Inside each resource:
1. Identify every `self._http.post` / `put` / `patch` call with a body.
2. Look up the spec input body class.
3. Replace `body=dict` with `body=encode_body(InputBody, dict)`.
4. Write a regression test demonstrating the typo catches.
5. Commit.

Total: ~29 commits, each small.

## Backwards compatibility

- Method signatures unchanged. Kwargs keep working.
- `**kwargs`-forwarding still works for now (pydantic `extra="forbid"` on input bodies means a typo raises `ValidationError` instead of silently reaching the server — a behavior flip, arguably a net good).
- Existing callers who pass correct fields see no change.

## Testing

For each migrated resource, `tests/test_<resource>.py` adds:
- **Typo test**: `pytest.raises(ValidationError)` when a kwarg name is misspelled.
- **Happy path**: still passes with correct kwargs (regression).

Existing `respx`-mocked tests continue to work since the wire body is unchanged.

## Scope check

This is big — 29 resources × several methods = ~200 call sites. It should be broken into batches (like Step 2 was):

- Batch 1: `agents.py`, `memory.py`, `knowledge.py` (core, most-used)
- Batch 2: `personality.py`, `priming.py`, `inventory.py`, `custom_states.py`
- Batch 3: Everything else (23 resources)

Each batch = 1 PR. The implementation plan should have ~3 batch tasks + 1 audit-script task + 1 helper-module task = 5 top-level tasks, each decomposed to bite-sized steps.

## Out of scope

- Rewriting the method signatures themselves (that's Step 3 B — auto-generate resource methods).
- Typing response bodies — already done in Step 2.
- Query-string / path parameter typing — lower value, defer.
