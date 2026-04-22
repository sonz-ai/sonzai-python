# Step 3 B: Auto-Generated Resource Methods Design

**Goal:** Eliminate the ~29 hand-written resource files (`src/sonzai/resources/*.py`) that collectively duplicate information already in `openapi.json`. Every list-paths-types-methods mapping the SDK knows about is derivable from the spec. Replace ~8,000 lines of hand-written boilerplate with a generator pass, dropping the per-endpoint human touch down to a thin convenience layer (~400 LOC).

**Architecture:** Custom code generator consumes `openapi.json` and emits `src/sonzai/_generated/resources/*.py` — one file per OpenAPI tag, each with sync + async classes. The hand-written `src/sonzai/resources/<area>.py` files become thin subclasses that ONLY carry convenience helpers (pagination iterators from A.3, streaming classifiers from A.4, business-logic helpers that don't belong in a generator). Drift between spec and SDK becomes structurally impossible.

**Tech Stack:** Jinja2 templates (already a transitive dep), `datamodel-code-generator`'s parser for path+operation extraction, pydantic v2 for input/output binding (from A.2). No runtime deps change.

---

## The scope problem

This is the most ambitious Step 3 sub-project. It interacts with everything:
- A.1 (typed errors) — raise sites stay centralized in `_http.py`, unchanged
- A.2 (typed request bodies) — generated methods use the same `encode_body(InputBody, ...)` pattern
- A.3 (pagination) — generated methods for list endpoints return `Page[T]` directly
- A.4 (typed streaming) — generated methods for streaming endpoints return the union type
- A.5 (retry) — transparent; retry is at the HTTP layer

**Sequencing**: A.1–A.5 should land first. Then B generates methods that already rely on those pieces being in place. Otherwise B would have to carry placeholder scaffolding and get retrofitted.

## Why not openapi-python-client

We evicted `openapi-python-client` in Step 1 because its output was attrs + UNSET sentinels — a DX nightmare for models. Its HTTP client layer is tied to the same attrs-based types. Bringing it back just for methods would re-introduce the style mismatch.

Alternatives:
- **Stainless / Fern** (commercial) — best quality output, used by OpenAI/Anthropic. Not-in-house; incurs vendor dependency for a core piece of infra. Option if "unlimited resources" really means "pay for it".
- **Custom Jinja template** — smallest moving part, zero vendor risk, generates exactly what we want. The template is ~500 lines. Recommended.
- **Speakeasy** (commercial) — similar tradeoffs to Stainless.

Recommendation: custom Jinja template, committed under `scripts/codegen/` with its own tests.

## Generator design

### Input

`openapi.json` (already synced, already driving `_generated/models.py`). Grouping by the `tags` field of each operation gives one output file per logical area (agents, memory, knowledge, etc.), matching the existing `resources/*.py` layout.

### Output

`src/sonzai/_generated/resources/<tag>.py`, one per tag. Each contains:

```python
# Generated — do not edit. Regenerate with `just regenerate-sdk`.
from __future__ import annotations

from typing import Any
from sonzai._generated.models import (
    ChatInputBody, ChatResponse, StoredFact, ...
)
from sonzai._pagination import Page, AsyncPage
from sonzai._request_helpers import encode_body

class _MemoryBase:
    """Shared HTTP plumbing. Subclassed by sync + async."""
    def __init__(self, http: Any) -> None:
        self._http = http

class Memory(_MemoryBase):
    def list_all_facts(
        self, agent_id: str, *, limit: int = 100,
    ) -> Page[StoredFact]:
        return Page(
            fetcher=lambda p: self._http.get(f"/agents/{agent_id}/facts/all", params=p),
            params={"limit": limit, "offset": 0},
            item_key="facts",
            item_parser=StoredFact.model_validate,
            mode="offset",
            total_key="total",
        )

    def add_fact(
        self, agent_id: str, *, content: str, fact_type: str, **extra: Any,
    ) -> StoredFact:
        body = encode_body(AddFactInputBody, {"content": content, "fact_type": fact_type, **extra})
        data = self._http.post(f"/agents/{agent_id}/facts", body=body)
        return StoredFact.model_validate(data)

    # ... one method per operation under the "memory" tag

class AsyncMemory(_MemoryBase):
    # async mirror; same methods with `async def` + `await`
```

### Extension pattern

Hand-written `src/sonzai/resources/memory.py` becomes a thin subclass:

```python
from sonzai._generated.resources.memory import Memory as _GenMemory, AsyncMemory as _GenAsyncMemory

class Memory(_GenMemory):
    """Hand-written convenience helpers layered on top of generated methods.

    Generated methods cover 100% of spec endpoints. This subclass only
    adds convenience that the spec doesn't encode.
    """

    def forget_user(self, agent_id: str, user_id: str) -> None:
        """Convenience: delete every fact tied to a user. Calls the generated
        list + delete_fact methods internally; no separate API endpoint."""
        for fact in self.list_all_facts(agent_id=agent_id, user_id=user_id):
            self.delete_fact(agent_id=agent_id, fact_id=fact.fact_id)

class AsyncMemory(_GenAsyncMemory):
    async def forget_user(self, agent_id: str, user_id: str) -> None: ...
```

`sonzai/_client.py` wires `Memory` and `AsyncMemory` from the customization path, not the generated path — so users importing `Sonzai.memory` get the subclass.

### Method signatures

Parsed from the operation's parameters + requestBody schema:
- Path params → positional-or-keyword arguments (`agent_id: str`)
- Query params → keyword-only arguments with defaults (`limit: int = 100`)
- Request body → flattened into keyword-only kwargs (`content: str, fact_type: str, ...`) using the spec's required vs optional fields
- Response type → model class from `_generated.models`
- Streaming endpoints (detected via `content-type: text/event-stream` or convention) return `Iterator[ChatStreamEvent]`

### Pagination detection

An operation is "paged" if it has a `limit` (or `pageSize`) query param AND the response body has an iterable key (`facts`, `items`, `results`). Detection heuristic: response schema has one `$ref` array-of-T property matching a known plural-of-singular mapping. Otherwise falls back to returning the raw response wrapper.

### Streaming detection

If the operation's responses include a `text/event-stream` content type, the generated method returns `Iterator[ChatStreamEvent]` (sync) or `AsyncIterator[ChatStreamEvent]` (async) and routes through `_http.stream_sse(...)` with the classifier from A.4.

### Regenerate flow

`just regenerate-sdk` extends to:
1. `just sync-spec` (existing)
2. `datamodel-codegen --output src/sonzai/_generated/models.py ...` (existing)
3. **NEW:** `python scripts/codegen/generate_resources.py openapi.json src/sonzai/_generated/resources/` — runs the Jinja templates.
4. Ruff format the output.
5. Parity audit (existing).

## Migration

29 resources × 2 classes (sync + async) × average 6 methods = ~350 methods. Manual migration would take weeks; this is the whole point of generating.

**Strategy**: 
1. Build the generator and validate on 3 tags (`memory`, `inventory`, `agents`) — the PoC.
2. Generate all tags into `_generated/resources/`.
3. Per existing `resources/*.py`: delete the method bodies, keep the class as a subclass of the generated class, retaining only convenience methods that don't map to a spec operation.
4. For each deleted method, assert the generated method has the same signature + return type. If not, investigate — either generator template needs tweaking or the hand-written signature was drifting from spec.
5. Tests that hit specific method signatures (most do) may need updating if signatures shifted.

## Drift detection

Extend the existing pre-push hook: if `_generated/resources/*.py` isn't regenerable from committed `openapi.json`, block push. Matches the pattern for `_generated/models.py`.

Pre-commit hook already blocks manual edits to `_generated/`; extends to the new `resources/` subdir automatically.

## Backwards compat

Method signatures SHOULD match existing hand-written ones. Auditable via a script that compares hand-written AST signatures against generated ones. Any divergence is either:
- Spec is wrong (file server-side bug, fix spec first)
- Hand-written signature is wrong (has been silently non-spec-compliant — rare but possible)
- Generator template is too literal (e.g., exposing every optional query param as a kwarg; users got by with `**kwargs`)

Each divergence is a manual reconciliation. Early PoC (3 tags) will surface the common patterns and inform the template.

## Testing

- **Generator unit tests** — `tests/test_codegen.py`: feed a canonical mini-spec into the generator, assert the output matches a golden file.
- **Generated code correctness** — all existing `tests/test_*.py` remain green when run against the generated resources. If any fail, the generator's output is wrong.
- **Signature parity** — `scripts/check_signature_parity.py` runs in the pre-push hook; asserts every generated method signature matches what's expected given the spec.

## Scope check

This is **at least 4 distinct implementation plans**:

1. **B.1**: Generator scaffold — Jinja templates, operation parser, one tag PoC (`memory`). 1 plan.
2. **B.2**: Generator hardening — handle all spec patterns (nested refs, discriminated request bodies, form-encoded, multipart upload, streaming, pagination detection). 1 plan.
3. **B.3**: Migrate all 29 resources to subclass-pattern. 1 plan, probably ~5 batches.
4. **B.4**: Hook integration + drift detection. 1 plan.

Each depends on the previous. DO NOT treat this as one plan. Each sub-plan needs its own brainstorm + design pass before coding.

## Risks

- **Method signature divergence** — spec might have gaps or sloppy definitions that generate ugly kwargs. Mitigation: PoC on 3 tags before committing to the generator approach.
- **File-upload endpoints** — OpenAPI `multipart/form-data` is the hardest to generate. Audit beforehand; there are ~3-5 such endpoints (knowledge uploads, avatar).
- **Streaming generators** — SSE parsing is client-side logic; the generator needs to emit `yield from self._http.stream_sse(...)` cleanly. Doable, just tricky.
- **Users who patch resource methods** — any monkey-patches to `Sonzai.memory.add_fact` point at the hand-written class. After migration, that still works (subclass inherits), but the patch site may have shifted methods. Low probability; document.

## Out of scope

- Generating the client constructor (`Sonzai(...)`) — that's hand-written wiring, not endpoint-derivable.
- Generating types.py's client-only classes (ChatUsage, etc.) — they have no spec counterpart.
- Websocket handling (voice streaming) — out of spec scope for the generator; stays hand-written.
- TypeScript / Go ports — those are distinct projects (would-be Step 4).
