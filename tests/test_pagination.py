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
        assert len(calls) == 1

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
