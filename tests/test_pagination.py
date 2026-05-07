"""Unit tests for Page[T] and AsyncPage[T]."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel

from sonzai._pagination import AsyncPage, Page


class Item(BaseModel):
    id: str


class TestPageCursor:
    def test_iterates_single_page(self) -> None:
        calls: list[dict[str, Any]] = []

        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            calls.append(params.copy())
            return {"items": [{"id": "a"}, {"id": "b"}], "has_more": False}

        page = Page(
            fetcher=fetcher,
            params={"page_size": 10},
            item_key="items",
            item_parser=Item.model_validate,
        )
        items = list(page)
        assert [i.id for i in items] == ["a", "b"]
        assert len(calls) == 1

    def test_advances_on_cursor(self) -> None:
        calls: list[dict[str, Any]] = []

        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            calls.append(params.copy())
            if params.get("cursor") is None:
                return {
                    "items": [{"id": "a"}],
                    "next_cursor": "c1",
                    "has_more": True,
                }
            if params["cursor"] == "c1":
                return {
                    "items": [{"id": "b"}],
                    "next_cursor": None,
                    "has_more": False,
                }
            return {"items": [], "next_cursor": None, "has_more": False}

        page = Page(
            fetcher=fetcher,
            params={"page_size": 10, "cursor": None},
            item_key="items",
            item_parser=Item.model_validate,
        )
        items = list(page)
        assert [i.id for i in items] == ["a", "b"]
        assert len(calls) == 2
        assert calls[1]["cursor"] == "c1"

    def test_first_page_stops_at_boundary(self) -> None:
        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            return {
                "items": [{"id": "a"}, {"id": "b"}],
                "next_cursor": "c1",
                "has_more": True,
            }

        page = Page(
            fetcher=fetcher,
            params={"page_size": 2},
            item_key="items",
            item_parser=Item.model_validate,
        )
        first = page.first_page()
        assert [i.id for i in first] == ["a", "b"]

    def test_to_list_collects_all(self) -> None:
        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            if params.get("cursor") is None:
                return {
                    "items": [{"id": "a"}],
                    "next_cursor": "c1",
                    "has_more": True,
                }
            return {"items": [{"id": "b"}], "has_more": False}

        page = Page(
            fetcher=fetcher,
            params={"page_size": 1},
            item_key="items",
            item_parser=Item.model_validate,
        )
        items = page.to_list()
        assert [i.id for i in items] == ["a", "b"]

    def test_no_more_pages_when_next_cursor_empty(self) -> None:
        def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            return {"items": [{"id": "a"}], "has_more": False}

        page = Page(
            fetcher=fetcher,
            params={"page_size": 10},
            item_key="items",
            item_parser=Item.model_validate,
        )
        list(page)
        assert page.has_more is False


class TestAsyncPage:
    @pytest.mark.asyncio
    async def test_async_iterates_across_pages(self) -> None:
        calls: list[dict[str, Any]] = []

        async def fetcher(params: dict[str, Any]) -> dict[str, Any]:
            calls.append(params.copy())
            if params.get("cursor") is None:
                return {
                    "items": [{"id": "a"}],
                    "next_cursor": "c1",
                    "has_more": True,
                }
            return {"items": [{"id": "b"}], "has_more": False}

        page = AsyncPage(
            fetcher=fetcher,
            params={"page_size": 1},
            item_key="items",
            item_parser=Item.model_validate,
        )
        collected: list[str] = []
        async for item in page:
            collected.append(item.id)
        assert collected == ["a", "b"]
        assert len(calls) == 2
