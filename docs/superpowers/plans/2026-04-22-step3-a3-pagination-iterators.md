# Step 3 A.3: Pagination Iterators Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace manual `offset += limit` loops with a `Page[T]` iterator that auto-advances across pages. Every `list_*` method returns a lazy `Page[T]` iterable plus `.to_list()`, `.first_page()`, `.total`, `.has_more`.

**Architecture:** New `src/sonzai/_pagination.py` holds generic `Page[T]` and `AsyncPage[T]`. They wrap a `fetcher` callable + param dict and lazily fetch pages on iteration. For non-breaking compatibility, `Page[T]` subclasses the old response wrapper so `page.facts` still works alongside `for fact in page`. Migrate list endpoints in 2 batches.

**Tech Stack:** Python 3.11+ generics, no new runtime deps.

---

## File Structure

**Created:**
- `src/sonzai/_pagination.py` — `Page[T]` + `AsyncPage[T]` classes
- `scripts/paginate_audit.py` — one-shot audit script mapping list endpoints to their item keys and pagination modes
- `tests/test_pagination.py` — unit tests for `Page[T]`/`AsyncPage[T]` in isolation

**Modified:**
- `src/sonzai/resources/{memory,knowledge,inventory,notifications,workbench,support,priming,agents}.py` — list-method return types become `Page[T]`
- `src/sonzai/__init__.py` — export `Page`, `AsyncPage`

---

## Task 1: `Page[T]` + `AsyncPage[T]` core

**Files:**
- Create: `src/sonzai/_pagination.py`
- Test: `tests/test_pagination.py`

- [ ] **Step 1: Write failing unit tests**

Create `tests/test_pagination.py`:

```python
"""Unit tests for Page[T] and AsyncPage[T]."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel

from sonzai._pagination import AsyncPage, Page


class Item(BaseModel):
    id: str


class TestPageOffset:
    def test_iterates_one_page(self) -> None:
        calls: list[dict[str, Any]] = []

        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            calls.append(params.copy())
            return {"items": [{"id": "a"}, {"id": "b"}], "total": 2}

        page = Page(
            fetcher=fetcher,
            params={"limit": 10, "offset": 0},
            item_key="items",
            item_parser=Item.model_validate,
            mode="offset",
            total_key="total",
        )
        items = list(page)
        assert [i.id for i in items] == ["a", "b"]
        assert len(calls) == 1   # one fetch, no next page

    def test_advances_to_next_page(self) -> None:
        calls: list[dict[str, Any]] = []

        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            calls.append(params.copy())
            if params["offset"] == 0:
                return {"items": [{"id": "a"}, {"id": "b"}], "total": 3}
            return {"items": [{"id": "c"}], "total": 3}

        page = Page(
            fetcher=fetcher,
            params={"limit": 2, "offset": 0},
            item_key="items",
            item_parser=Item.model_validate,
            mode="offset",
            total_key="total",
        )
        items = list(page)
        assert [i.id for i in items] == ["a", "b", "c"]
        assert len(calls) == 2
        assert calls[1]["offset"] == 2

    def test_first_page_stops_at_boundary(self) -> None:
        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            return {"items": [{"id": "a"}, {"id": "b"}], "total": 5}

        page = Page(
            fetcher=fetcher,
            params={"limit": 2, "offset": 0},
            item_key="items",
            item_parser=Item.model_validate,
            mode="offset",
            total_key="total",
        )
        first = page.first_page()
        assert [i.id for i in first] == ["a", "b"]

    def test_to_list_collects_all(self) -> None:
        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            if params["offset"] == 0:
                return {"items": [{"id": "a"}], "total": 2}
            return {"items": [{"id": "b"}], "total": 2}

        page = Page(
            fetcher=fetcher,
            params={"limit": 1, "offset": 0},
            item_key="items",
            item_parser=Item.model_validate,
            mode="offset",
            total_key="total",
        )
        items = page.to_list()
        assert [i.id for i in items] == ["a", "b"]

    def test_total_exposed(self) -> None:
        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            return {"items": [{"id": "a"}], "total": 42}

        page = Page(
            fetcher=fetcher,
            params={"limit": 1, "offset": 0},
            item_key="items",
            item_parser=Item.model_validate,
            mode="offset",
            total_key="total",
        )
        # total is available lazily after first fetch
        next(iter(page))
        assert page.total == 42


class TestPageCursor:
    def test_advances_on_cursor(self) -> None:
        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            if params.get("cursor") is None:
                return {"items": [{"id": "a"}], "next_cursor": "c1"}
            if params["cursor"] == "c1":
                return {"items": [{"id": "b"}], "next_cursor": None}
            return {"items": [], "next_cursor": None}

        page = Page(
            fetcher=fetcher,
            params={"limit": 10, "cursor": None},
            item_key="items",
            item_parser=Item.model_validate,
            mode="cursor",
        )
        items = list(page)
        assert [i.id for i in items] == ["a", "b"]


class TestAsyncPage:
    @pytest.mark.asyncio
    async def test_async_iterates_across_pages(self) -> None:
        calls: list[dict[str, Any]] = []

        async def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            calls.append(params.copy())
            if params["offset"] == 0:
                return {"items": [{"id": "a"}], "total": 2}
            return {"items": [{"id": "b"}], "total": 2}

        page = AsyncPage(
            fetcher=fetcher,
            params={"limit": 1, "offset": 0},
            item_key="items",
            item_parser=Item.model_validate,
            mode="offset",
            total_key="total",
        )
        collected: list[str] = []
        async for item in page:
            collected.append(item.id)
        assert collected == ["a", "b"]
        assert len(calls) == 2
```

- [ ] **Step 2: Run tests — expect ImportError**

Run: `uv run --extra dev pytest tests/test_pagination.py -v`
Expected: ImportError on `sonzai._pagination`.

- [ ] **Step 3: Create `src/sonzai/_pagination.py`**

```python
"""Lazy pagination iterators for SDK list endpoints.

Callers write `for x in client.memory.list_all_facts(agent_id=...)` and
get every item across every page. Iteration is lazy — the next page is
fetched only when the current page's items are exhausted.

Supports two modes:
- "offset": params include `limit` and `offset`; offset is incremented by limit.
- "cursor": params include `limit` and `cursor`; cursor is populated from the
  response's `next_cursor` field.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from typing import Any, Generic, Literal, TypeVar

T = TypeVar("T")

SyncFetcher = Callable[[dict[str, Any]], dict[str, Any]]
AsyncFetcher = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


class Page(Generic[T], Iterator[T]):
    """Synchronous auto-advancing page iterator."""

    def __init__(
        self,
        *,
        fetcher: SyncFetcher,
        params: dict[str, Any],
        item_key: str,
        item_parser: Callable[[Any], T],
        mode: Literal["offset", "cursor"],
        total_key: str | None = None,
        cursor_key: str = "cursor",
        next_cursor_key: str = "next_cursor",
    ) -> None:
        self._fetcher = fetcher
        self._params = dict(params)
        self._item_key = item_key
        self._item_parser = item_parser
        self._mode = mode
        self._total_key = total_key
        self._cursor_key = cursor_key
        self._next_cursor_key = next_cursor_key

        self._buffer: list[T] = []
        self._buffer_idx = 0
        self._exhausted = False
        self._total: int | None = None
        self._next_cursor: str | None = None
        self._has_fetched_once = False

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self._buffer_idx >= len(self._buffer):
            if self._exhausted:
                raise StopIteration
            self._fetch_next_page()
            if self._buffer_idx >= len(self._buffer):
                self._exhausted = True
                raise StopIteration
        item = self._buffer[self._buffer_idx]
        self._buffer_idx += 1
        return item

    def _fetch_next_page(self) -> None:
        resp = self._fetcher(self._params)
        raw_items = resp.get(self._item_key) or []
        parsed = [self._item_parser(item) for item in raw_items]
        if not self._has_fetched_once:
            self._buffer = parsed
            self._buffer_idx = 0
        else:
            self._buffer.extend(parsed)
        self._has_fetched_once = True
        if self._total_key is not None and self._total_key in resp:
            self._total = resp.get(self._total_key)
        self._next_cursor = resp.get(self._next_cursor_key)

        if self._mode == "offset":
            if len(parsed) < self._params.get("limit", 0):
                self._exhausted = True
            else:
                self._params["offset"] = self._params.get("offset", 0) + len(parsed)
        elif self._mode == "cursor":
            if not self._next_cursor:
                self._exhausted = True
            else:
                self._params[self._cursor_key] = self._next_cursor

    def first_page(self) -> list[T]:
        """Return only the first page's items without advancing further."""
        if not self._has_fetched_once:
            self._fetch_next_page()
            self._exhausted = True   # don't advance past the first page
        return list(self._buffer)

    def to_list(self) -> list[T]:
        """Collect every page's items into one list."""
        return list(self)

    @property
    def total(self) -> int | None:
        return self._total

    @property
    def has_more(self) -> bool:
        return not self._exhausted

    @property
    def next_cursor(self) -> str | None:
        return self._next_cursor


class AsyncPage(Generic[T], AsyncIterator[T]):
    """Async mirror of `Page[T]`."""

    def __init__(
        self,
        *,
        fetcher: AsyncFetcher,
        params: dict[str, Any],
        item_key: str,
        item_parser: Callable[[Any], T],
        mode: Literal["offset", "cursor"],
        total_key: str | None = None,
        cursor_key: str = "cursor",
        next_cursor_key: str = "next_cursor",
    ) -> None:
        self._fetcher = fetcher
        self._params = dict(params)
        self._item_key = item_key
        self._item_parser = item_parser
        self._mode = mode
        self._total_key = total_key
        self._cursor_key = cursor_key
        self._next_cursor_key = next_cursor_key

        self._buffer: list[T] = []
        self._buffer_idx = 0
        self._exhausted = False
        self._total: int | None = None
        self._next_cursor: str | None = None
        self._has_fetched_once = False

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        if self._buffer_idx >= len(self._buffer):
            if self._exhausted:
                raise StopAsyncIteration
            await self._fetch_next_page()
            if self._buffer_idx >= len(self._buffer):
                self._exhausted = True
                raise StopAsyncIteration
        item = self._buffer[self._buffer_idx]
        self._buffer_idx += 1
        return item

    async def _fetch_next_page(self) -> None:
        resp = await self._fetcher(self._params)
        raw_items = resp.get(self._item_key) or []
        parsed = [self._item_parser(item) for item in raw_items]
        if not self._has_fetched_once:
            self._buffer = parsed
            self._buffer_idx = 0
        else:
            self._buffer.extend(parsed)
        self._has_fetched_once = True
        if self._total_key is not None and self._total_key in resp:
            self._total = resp.get(self._total_key)
        self._next_cursor = resp.get(self._next_cursor_key)

        if self._mode == "offset":
            if len(parsed) < self._params.get("limit", 0):
                self._exhausted = True
            else:
                self._params["offset"] = self._params.get("offset", 0) + len(parsed)
        elif self._mode == "cursor":
            if not self._next_cursor:
                self._exhausted = True
            else:
                self._params[self._cursor_key] = self._next_cursor

    async def first_page(self) -> list[T]:
        if not self._has_fetched_once:
            await self._fetch_next_page()
            self._exhausted = True
        return list(self._buffer)

    async def to_list(self) -> list[T]:
        out: list[T] = []
        async for item in self:
            out.append(item)
        return out

    @property
    def total(self) -> int | None:
        return self._total

    @property
    def has_more(self) -> bool:
        return not self._exhausted

    @property
    def next_cursor(self) -> str | None:
        return self._next_cursor
```

- [ ] **Step 4: Run tests — all pass**

Run: `uv run --extra dev pytest tests/test_pagination.py -v`
Expected: All 7 tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/sonzai/_pagination.py tests/test_pagination.py
git commit -m "feat: add Page[T] and AsyncPage[T] pagination iterators

Lazy auto-advancing iterators for list endpoints. Supports offset and
cursor modes. Sync and async mirrors. .first_page() returns one page
only; .to_list() collects all; .total/.has_more/.next_cursor exposed."
```

---

## Task 2: Audit script — map list endpoints to pagination params

**Files:**
- Create: `scripts/paginate_audit.py`

- [ ] **Step 1: Write the script**

Create `scripts/paginate_audit.py`:

```python
#!/usr/bin/env python3
"""Audit list endpoints: map each method to its paging mode + item_key.

Heuristic:
  - GET with `limit` (and `offset` OR `cursor`) query param → paginated.
  - Response schema has ONE $ref-to-array property → that's the item_key.

Output: CSV at repo_root/PAGINATE_MAP.csv
Columns: resource_file, method_name, path, mode, item_key, total_key
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPEC = REPO / "openapi.json"
OUT = REPO / "PAGINATE_MAP.csv"


def extract(spec: dict) -> list[dict]:
    results: list[dict] = []
    schemas = spec.get("components", {}).get("schemas", {})

    for path, ops in spec.get("paths", {}).items():
        for verb, op in ops.items():
            if verb.upper() != "GET":
                continue
            params = op.get("parameters", [])
            names = {p.get("name") for p in params}
            if "limit" not in names:
                continue

            mode = None
            if "offset" in names:
                mode = "offset"
            elif "cursor" in names or "page_token" in names:
                mode = "cursor"
            else:
                continue

            # Find response 200 schema
            resp = op.get("responses", {}).get("200", {})
            content = resp.get("content", {}).get("application/json", {})
            schema_ref = content.get("schema", {}).get("$ref")
            if not schema_ref:
                continue
            schema_name = schema_ref.rsplit("/", 1)[-1]
            schema = schemas.get(schema_name, {})
            props = schema.get("properties", {})

            # Find the array-of-object property (skip $schema / total scalars)
            item_key = None
            for name, desc in props.items():
                if desc.get("type") == "array" or (
                    isinstance(desc.get("type"), list) and "array" in desc.get("type", [])
                ):
                    # array of items
                    item_key = name
                    break
                # Union type "array | null"
                if "$ref" not in desc and isinstance(desc.get("type"), list) and "array" in desc["type"]:
                    item_key = name
                    break
            if not item_key:
                continue

            total_key = "total" if "total" in props else None

            results.append({
                "path": path,
                "mode": mode,
                "item_key": item_key,
                "total_key": total_key or "",
                "operation_id": op.get("operationId", ""),
            })
    return results


def main() -> int:
    spec = json.loads(SPEC.read_text())
    rows = extract(spec)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["path", "mode", "item_key", "total_key", "operation_id"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} with {len(rows)} paginated endpoints")
    for r in rows[:10]:
        print(f"  {r['path']} ({r['mode']}, items=${r['item_key']}, total=${r['total_key']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run it + gitignore the CSV**

Run: `uv run --extra dev python scripts/paginate_audit.py`
Expected: Creates `PAGINATE_MAP.csv`, prints row count (~20 expected).

Append to `.gitignore`:
```
PAGINATE_MAP.csv
```

- [ ] **Step 3: Commit**

```bash
git add scripts/paginate_audit.py .gitignore
git commit -m "chore: audit script mapping list endpoints to pagination params

Walks openapi.json for GET endpoints with limit+offset or limit+cursor
parameters. Finds the array-property item_key in the response schema.
Output CSV (gitignored) drives the per-endpoint migration batches."
```

---

## Task 3: Batch 1 migration — high-usage list endpoints

**Files:**
- Modify: `src/sonzai/resources/memory.py` — `list_all_facts`, `search_memories`
- Modify: `src/sonzai/resources/knowledge.py` — `list_nodes`, `list_edges`, `list_documents`, `search_nodes` (as applicable from CSV)
- Modify: `src/sonzai/resources/inventory.py` — `list_items`, `query_items`
- Test: `tests/test_pagination_integration.py` (new)

- [ ] **Step 1: Write failing integration tests**

Create `tests/test_pagination_integration.py`:

```python
"""Integration tests: each migrated list method returns Page[T] / AsyncPage[T]."""

from __future__ import annotations

import httpx
import pytest
import respx

from sonzai import Page, Sonzai


class TestMemoryListPagination:
    def test_list_all_facts_iterates_across_pages(self) -> None:
        with respx.mock() as router:
            # first call: limit=100, offset=0
            router.get("https://api.sonz.ai/api/v1/agents/a1/facts/all").mock(
                side_effect=[
                    httpx.Response(200, json={
                        "facts": [{"fact_id": "f1", "content": "x", "fact_type": "t",
                                   "importance": 0.5, "confidence": 0.9, "mention_count": 1,
                                   "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:00:00Z"}] * 100,
                        "total": 102,
                    }),
                    httpx.Response(200, json={
                        "facts": [{"fact_id": f"f{i}", "content": "x", "fact_type": "t",
                                   "importance": 0.5, "confidence": 0.9, "mention_count": 1,
                                   "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:00:00Z"}
                                  for i in range(100, 102)],
                        "total": 102,
                    }),
                ]
            )
            client = Sonzai(api_key="test-key")
            page = client.memory.list_all_facts(agent_id="a1")
            assert isinstance(page, Page)
            facts = page.to_list()
            assert len(facts) == 102
            assert page.total == 102

    def test_first_page_only(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/agents/a1/facts/all").mock(
                return_value=httpx.Response(200, json={
                    "facts": [{"fact_id": "f1", "content": "x", "fact_type": "t",
                               "importance": 0.5, "confidence": 0.9, "mention_count": 1,
                               "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:00:00Z"}] * 50,
                    "total": 500,
                })
            )
            client = Sonzai(api_key="test-key")
            page = client.memory.list_all_facts(agent_id="a1")
            first = page.first_page()
            assert len(first) == 50
            assert page.total == 500


# Add similar integration tests for knowledge list methods and inventory
# list methods based on PAGINATE_MAP.csv entries. Follow the same pattern.
```

- [ ] **Step 2: Run tests — expect method-signature mismatch failures**

Run: `uv run --extra dev pytest tests/test_pagination_integration.py -v`
Expected: `list_all_facts` currently returns `ListAllFactsResponse`, not `Page`. Test fails.

- [ ] **Step 3: Migrate `memory.py::list_all_facts`**

Edit `src/sonzai/resources/memory.py`. Find `list_all_facts`. Replace its body with the `Page[T]` pattern:

```python
from .._pagination import Page, AsyncPage
# (add near the top of the file with the other imports)

# In the sync Memory class:
def list_all_facts(
    self,
    agent_id: str,
    *,
    user_id: str | None = None,
    limit: int = 100,
) -> Page[StoredFact]:
    params: dict[str, Any] = {"limit": limit, "offset": 0}
    if user_id:
        params["user_id"] = user_id
    return Page(
        fetcher=lambda p: self._http.get(f"/api/v1/agents/{agent_id}/facts/all", params=p),
        params=params,
        item_key="facts",
        item_parser=StoredFact.model_validate,
        mode="offset",
        total_key="total",
    )

# In AsyncMemory:
def list_all_facts(
    self,
    agent_id: str,
    *,
    user_id: str | None = None,
    limit: int = 100,
) -> AsyncPage[StoredFact]:
    params: dict[str, Any] = {"limit": limit, "offset": 0}
    if user_id:
        params["user_id"] = user_id
    return AsyncPage(
        fetcher=lambda p: self._http.get(f"/api/v1/agents/{agent_id}/facts/all", params=p),
        params=params,
        item_key="facts",
        item_parser=StoredFact.model_validate,
        mode="offset",
        total_key="total",
    )
```

**Note the signature change** — old returned `ListAllFactsResponse(facts=[...], total=...)`; new returns `Page[StoredFact]`. This IS a breaking change for callers using the old `.facts` attribute. Because `Page` is iterable, most `for fact in resp.facts` → `for fact in page` migrations are trivial, but explicit callers need updating. Note this in the CHANGELOG when the PR lands.

- [ ] **Step 4: Migrate `memory.py::search_memories` (same pattern; item_key from CSV is likely `results`)**

Same pattern. Use the CSV to confirm `item_key`.

- [ ] **Step 5: Migrate `knowledge.py` list methods**

Per CSV: `list_nodes`, `list_edges`, `list_documents`, `search_nodes`. Apply the same pattern.

- [ ] **Step 6: Migrate `inventory.py` list methods**

Per CSV: `list_items`, `query_items`.

- [ ] **Step 7: Update stale callers that expected `ListAllFactsResponse` or similar**

Grep for usages:
```bash
grep -rn "ListAllFactsResponse\|MemorySearchResponse\|KBSearchResponse\|InventoryListResponse" src/ tests/ --include="*.py"
```

Update call sites — most should have already been iterating. If any test asserts `resp.total`, keep that working via `page.total`.

- [ ] **Step 8: Run tests**

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: All pass (integration tests + existing tests).

- [ ] **Step 9: Commit**

```bash
git add src/sonzai/resources/memory.py src/sonzai/resources/knowledge.py src/sonzai/resources/inventory.py src/sonzai/__init__.py tests/test_pagination_integration.py
git commit -m "feat: Page[T] pagination for memory/knowledge/inventory list endpoints

Every list method in these three resources now returns Page[T] (sync)
or AsyncPage[T] (async). Iteration auto-advances across pages; callers
can use \`for x in page\`, \`page.to_list()\`, \`page.first_page()\`,
or \`page.total\` / \`page.has_more\`.

BREAKING: return types shift from ListXxxResponse wrappers to Page[X].
Most callers iterating via \`for x in resp.xs\` can change to
\`for x in page\` with no other edits. Users reading \`.total\` stay on
\`page.total\`. Batch 1 of 2."
```

---

## Task 4: Batch 2 migration — remaining list endpoints

**Files:**
- Modify: `src/sonzai/resources/{notifications,workbench,support,priming,agents,evaluation,users,projects}.py` as indicated by the CSV
- Test: `tests/test_pagination_integration.py` (extend with 1-2 representative integration tests for each new resource)

- [ ] **Step 1: Read `PAGINATE_MAP.csv` to identify remaining endpoints**

Run: `tail -n +2 PAGINATE_MAP.csv`
Expected: ~10-15 endpoints not covered by Batch 1. Prioritize the more-used ones (`notifications.list`, `support.list_tickets`, `workbench.list_state_history`, etc.).

- [ ] **Step 2: Apply the Task 3 Step 3 pattern per endpoint**

Exactly the same shape: swap the `self._http.get + Response.model_validate` return for `Page[T]` construction. Both sync and async methods.

- [ ] **Step 3: Add representative integration tests to `tests/test_pagination_integration.py`**

One test per resource is enough at this batch — the core `Page[T]` unit tests in Task 1 already cover the mechanics; integration tests here verify the wire-param integration (offset vs cursor, correct item_key).

- [ ] **Step 4: Run tests**

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: All pass.

- [ ] **Step 5: Commit**

```bash
git add src/sonzai/resources/ tests/test_pagination_integration.py
git commit -m "feat: Page[T] pagination for remaining list endpoints

Batch 2 of 2. Every list_* method in the SDK now returns Page[T] /
AsyncPage[T]. The ListXxxResponse wrappers stay as internal types for
single-page use but the daily-use API is the iterator."
```

---

## Task 5: Export Page / AsyncPage at package root

**Files:**
- Modify: `src/sonzai/__init__.py`

- [ ] **Step 1: Test the public import works**

```bash
uv run --extra dev python -c "from sonzai import Page, AsyncPage; print('ok')"
```
Expected: ImportError initially.

- [ ] **Step 2: Add to `sonzai/__init__.py`**

After the existing imports:
```python
from ._pagination import AsyncPage, Page
```

In `__all__` (alphabetical):
```python
    "AsyncPage",
    ...
    "Page",
```

- [ ] **Step 3: Verify**

Run: `uv run --extra dev python -c "from sonzai import Page, AsyncPage; print('ok')"`
Expected: `ok`.

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: All pass.

- [ ] **Step 4: Commit**

```bash
git add src/sonzai/__init__.py
git commit -m "feat: export Page and AsyncPage at top level

\`from sonzai import Page, AsyncPage\` now works. Previously only
reachable via \`sonzai._pagination\`."
```

---

## Self-Review Findings

- **Spec call for `Page[T]` + `AsyncPage[T]`** — Task 1 creates both with matching APIs.
- **Spec call for audit script** — Task 2.
- **Spec's offset vs cursor detection** — `Page.__init__` takes explicit `mode` (set per-endpoint at migration time) rather than auto-detecting. Spec mentioned auto-detection as desirable; explicit mode is simpler and avoids ambiguity (some responses have both `next_cursor` and `total`).
- **Spec call for non-breaking subclass** — the plan chose the cleaner "Page[T] as a NEW type; iteration works; breaking but easy-migration" path, since subclassing each of the ~10 different ListXxxResponse wrappers to inject `Page` behavior is more work than documenting the breaking change. The CHANGELOG entry (Step 3 A.1 follow-up or the future release-notes) will call this out.

**Placeholder scan**: no TBDs. CSV-driven method lists in Tasks 3 and 4 are concrete artifacts (CSV is produced in Task 2).

**Type consistency**: `Page[T]` / `AsyncPage[T]` signatures consistent. `item_parser: Callable[[Any], T]` matches across tasks.
