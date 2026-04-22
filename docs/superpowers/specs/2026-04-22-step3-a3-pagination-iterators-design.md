# Step 3 A.3: Pagination Iterators Design

**Goal:** Replace the manual `offset += 100; loop` pattern users currently write for `list_*` endpoints with a native Python iterator that auto-pages transparently. `for fact in client.memory.list_facts(agent_id="x")` should iterate every fact, not just the first page.

**Architecture:** Introduce a generic `Page[T]` cursor type. Resource list methods return `Page[T]` (which is a lazy iterator over `T` plus `.has_more`, `.next_cursor`, `.total`). Iterating exhausts pages; users who want one page call `.first_page()`. Works for both offset-based and cursor-based endpoints — the paginator detects which by reading the response envelope.

**Tech Stack:** Python 3.11+ `Generic[T]`, no new runtime deps. Uses existing `httpx.Client` and `httpx.AsyncClient` from `_http.py`.

---

## Current pain

```python
# User code today:
all_facts = []
offset = 0
while True:
    page = client.memory.list_all_facts(agent_id="x", limit=100, offset=offset)
    all_facts.extend(page.facts)
    if len(page.facts) < 100:
        break
    offset += 100
```

The SDK forces callers to write pagination loops and get `off-by-one` bugs.

## What users get

```python
# Sync
for fact in client.memory.list_all_facts(agent_id="x"):
    print(fact.content)

# Async
async for fact in aclient.memory.list_all_facts(agent_id="x"):
    print(fact.content)

# Still supports one-page-at-a-time when you want it
page = client.memory.list_all_facts(agent_id="x").first_page()
print(f"Got {len(page)} of {page.total} facts")

# Collect-all helper
facts = client.memory.list_all_facts(agent_id="x").to_list()
```

## Design: `Page[T]` class

In `src/sonzai/_pagination.py` (new):

```python
from typing import Generic, TypeVar, Callable, Iterator, AsyncIterator
from dataclasses import dataclass

T = TypeVar("T")

class Page(Generic[T], Iterator[T]):
    """Lazy, auto-advancing page of T items."""

    def __init__(
        self,
        fetcher: Callable[[dict[str, Any]], dict[str, Any]],
        params: dict[str, Any],
        item_key: str,               # e.g. "facts", "users"
        item_parser: Callable[[dict], T],
        mode: Literal["cursor", "offset"],
        total_key: str | None = None,
    ) -> None: ...

    def __iter__(self) -> Iterator[T]: ...
    def __next__(self) -> T: ...
    def first_page(self) -> list[T]: ...
    def to_list(self) -> list[T]: ...
    @property
    def total(self) -> int | None: ...
    @property
    def has_more(self) -> bool: ...
    @property
    def next_cursor(self) -> str | None: ...

class AsyncPage(Generic[T], AsyncIterator[T]): ...  # async mirror
```

The `Page` fetches one page lazily on first `__next__` call. When exhausted, if `has_more`, it fetches the next page and continues. Cursor-based: passes `next_cursor` as `cursor` param. Offset-based: increments `offset` by `limit`. Auto-detection reads response envelope: if `next_cursor` present → cursor mode; else → offset mode.

## Resource method changes

Every `list_*` method in `src/sonzai/resources/*.py` changes from:

```python
def list_all_facts(self, agent_id: str, *, limit: int = 50, offset: int = 0) -> ListAllFactsResponse:
    data = self._http.get(f"/agents/{agent_id}/facts/all", params={"limit": limit, "offset": offset})
    return ListAllFactsResponse.model_validate(data)
```

to:

```python
def list_all_facts(self, agent_id: str, *, limit: int = 100) -> Page[StoredFact]:
    return Page(
        fetcher=lambda p: self._http.get(f"/agents/{agent_id}/facts/all", params=p),
        params={"limit": limit, "offset": 0},
        item_key="facts",
        item_parser=lambda d: StoredFact.model_validate(d),
        mode="offset",
        total_key="total",
    )
```

`ListAllFactsResponse` as a top-level return type goes away for paged endpoints — users iterate items, not the wrapper. The wrapper is still internally reachable via `.first_page()` semantics but the daily-use API is the iterator.

## List-endpoint inventory

A script (`scripts/paginate_audit.py`) walks `openapi.json` for paths with `limit` + (`offset` or `cursor`) query params and cross-references with `resources/*.py` methods. Output: CSV of (resource_file, method_name, mode, item_key, item_parser, total_key). That's the task list.

Rough scan: ~20 list endpoints across `memory`, `knowledge`, `agents`, `inventory`, `notifications`, `workbench`, `support`, `priming`.

## Backwards compatibility

This IS a breaking API change — return types shift from `ListFooResponse` to `Page[Foo]`. Mitigate with:
- **Iteration**: `for x in page` works on both (Page is iterable; the old Response exposed `.foos` which was also iterable).
- **`.to_list()`** is a net-new-but-simple migration for users who wrote `response.facts`.
- **Document in CHANGELOG** with a migration section.
- Consider shipping this behind a version bump (e.g., 2.0) given the return-type change.

Alternative non-breaking design: `Page` inherits from the old response wrapper. Users doing `resp.facts` keep working; iteration is a new superpower. This doubles the code but makes the migration zero-effort. Recommend this path.

## Testing

For each migrated method:
- Stub 3 pages of responses (cursor or offset) with `respx`.
- Assert `for x in page` visits all items across pages.
- Assert `page.total` matches summed counts.
- Assert `page.first_page()` returns only the first page's items.
- Async mirror.

Plus a new `tests/test_pagination.py` covering `Page[T]` semantics in isolation (fetcher stubs).

## Scope check

One `_pagination.py` module + ~20 resource method signatures + ~40 tests (2 per endpoint — sync+async). Estimate: 1 foundational task (Page class) + 1 audit script + 4 batch tasks (5 endpoints each). Manageable as a single plan.

## Out of scope

- Cursor+offset hybrid pagination (nothing in the spec uses it).
- Backward pagination (`prev_cursor`) — not in API today.
- Filter DSL built on iterators — future.
