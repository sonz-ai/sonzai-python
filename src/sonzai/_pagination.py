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
            new_offset = self._params.get("offset", 0) + len(parsed)
            if len(parsed) < self._params.get("limit", 0):
                self._exhausted = True
            elif self._total is not None and new_offset >= self._total:
                self._exhausted = True
            else:
                self._params["offset"] = new_offset
        elif self._mode == "cursor":
            if not self._next_cursor:
                self._exhausted = True
            else:
                self._params[self._cursor_key] = self._next_cursor

    def first_page(self) -> list[T]:
        """Return only the first page's items without advancing further."""
        if not self._has_fetched_once:
            self._fetch_next_page()
            self._exhausted = True
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
            new_offset = self._params.get("offset", 0) + len(parsed)
            if len(parsed) < self._params.get("limit", 0):
                self._exhausted = True
            elif self._total is not None and new_offset >= self._total:
                self._exhausted = True
            else:
                self._params["offset"] = new_offset
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
