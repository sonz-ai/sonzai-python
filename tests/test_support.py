"""Tests for the Support tickets resource.

Confirms:

- Request shapes match the OpenAPI spec (query params on list, JSON body on
  create/comments, no body on close).
- Responses parse into the typed models (``TicketListResponse``,
  ``SupportTicket``, ``TicketDetailResponse``, ``SupportTicketComment``).
- Optional args are omitted from the wire payload when ``None``.
- Both sync and async clients expose the resource.
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai
from sonzai.resources.support import AsyncSupport, Support


@pytest.fixture
def base_url() -> str:
    return "https://api.test.sonz.ai"


@pytest.fixture
def client(base_url: str):
    c = Sonzai(api_key="test-key", base_url=base_url)
    yield c
    c.close()


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------


class TestSupportSync:
    @respx.mock
    def test_list_no_params(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(f"{base_url}/api/v1/support/tickets").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tickets": [
                        {
                            "ticket_id": "t1",
                            "title": "Cannot log in",
                            "type": "support",
                            "status": "open",
                            "priority": "medium",
                            "created_by_email": "user@example.com",
                            "comment_count": 0,
                            "created_at": "2026-04-21T10:00:00Z",
                            "updated_at": "2026-04-21T10:00:00Z",
                        }
                    ],
                    "total": 1,
                    "has_more": False,
                },
            )
        )

        result = client.support.list_tickets()
        assert route.called
        assert result.total == 1
        assert result.has_more is False
        assert len(result.tickets) == 1
        assert result.tickets[0].ticket_id == "t1"
        assert result.tickets[0].title == "Cannot log in"
        assert route.calls[0].request.url.query == b""

    @respx.mock
    def test_list_with_filters(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(f"{base_url}/api/v1/support/tickets").mock(
            return_value=httpx.Response(
                200,
                json={"tickets": [], "total": 0, "has_more": False},
            )
        )

        client.support.list_tickets(limit=50, offset=10, status="open", type="bug")
        assert route.called
        params = dict(route.calls[0].request.url.params)
        assert params == {
            "limit": "50",
            "offset": "10",
            "status": "open",
            "type": "bug",
        }

    @respx.mock
    def test_create(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/support/tickets").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ticket_id": "t1",
                    "tenant_id": "tenant-a",
                    "created_by": "user-1",
                    "created_by_email": "user@example.com",
                    "title": "Cannot log in",
                    "description": "Keeps rejecting my password",
                    "type": "support",
                    "status": "open",
                    "priority": "medium",
                    "created_at": "2026-04-21T10:00:00Z",
                    "updated_at": "2026-04-21T10:00:00Z",
                },
            )
        )

        ticket = client.support.create_ticket(
            title="Cannot log in",
            description="Keeps rejecting my password",
            type="support",
            priority="medium",
        )
        assert route.called
        assert ticket.ticket_id == "t1"
        assert ticket.title == "Cannot log in"
        assert ticket.type == "support"
        body = json.loads(route.calls[0].request.content)
        assert body == {
            "title": "Cannot log in",
            "description": "Keeps rejecting my password",
            "type": "support",
            "priority": "medium",
        }

    @respx.mock
    def test_create_omits_priority_when_none(
        self, client: Sonzai, base_url: str
    ) -> None:
        route = respx.post(f"{base_url}/api/v1/support/tickets").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ticket_id": "t2",
                    "tenant_id": "tenant-a",
                    "created_by": "u1",
                    "created_by_email": "u@example.com",
                    "title": "T",
                    "description": "D",
                    "type": "support",
                    "status": "open",
                    "priority": "medium",
                    "created_at": "2026-04-21T10:00:00Z",
                    "updated_at": "2026-04-21T10:00:00Z",
                },
            )
        )

        client.support.create_ticket(title="T", description="D", type="support")
        body = json.loads(route.calls[0].request.content)
        assert "priority" not in body

    @respx.mock
    def test_get(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(f"{base_url}/api/v1/support/tickets/t1").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ticket": {
                        "ticket_id": "t1",
                        "tenant_id": "tenant-a",
                        "created_by": "user-1",
                        "created_by_email": "user@example.com",
                        "title": "T",
                        "description": "D",
                        "type": "support",
                        "status": "open",
                        "priority": "medium",
                        "comment_count": 1,
                        "comments": [
                            {
                                "comment_id": "c1",
                                "ticket_id": "t1",
                                "author_id": "user-1",
                                "author_email": "user@example.com",
                                "author_type": "user",
                                "content": "Hello",
                                "is_internal": False,
                                "created_at": "2026-04-21T10:05:00Z",
                            }
                        ],
                        "created_at": "2026-04-21T10:00:00Z",
                        "updated_at": "2026-04-21T10:05:00Z",
                    },
                    "history": [
                        {
                            "history_id": "h1",
                            "ticket_id": "t1",
                            "changed_by": "user-1",
                            "changed_by_email": "user@example.com",
                            "field_changed": "status",
                            "old_value": "",
                            "new_value": "open",
                            "created_at": "2026-04-21T10:00:00Z",
                        }
                    ],
                },
            )
        )

        detail = client.support.get_ticket("t1")
        assert route.called
        assert detail.ticket.ticket_id == "t1"
        assert detail.ticket.comments is not None
        assert detail.ticket.comments[0].comment_id == "c1"
        assert detail.history is not None
        assert detail.history[0].field_changed == "status"

    @respx.mock
    def test_close(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/support/tickets/t1/close").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ticket_id": "t1",
                    "tenant_id": "tenant-a",
                    "created_by": "user-1",
                    "created_by_email": "user@example.com",
                    "title": "T",
                    "description": "D",
                    "type": "support",
                    "status": "closed",
                    "priority": "medium",
                    "created_at": "2026-04-21T10:00:00Z",
                    "updated_at": "2026-04-21T10:30:00Z",
                },
            )
        )

        ticket = client.support.close_ticket("t1")
        assert route.called
        assert ticket.status == "closed"

    @respx.mock
    def test_add_comment(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/support/tickets/t1/comments").mock(
            return_value=httpx.Response(
                200,
                json={
                    "comment_id": "c2",
                    "ticket_id": "t1",
                    "author_id": "user-1",
                    "author_email": "user@example.com",
                    "author_type": "user",
                    "content": "Any update?",
                    "is_internal": False,
                    "created_at": "2026-04-21T11:00:00Z",
                },
            )
        )

        comment = client.support.add_comment("t1", content="Any update?")
        assert route.called
        assert comment.comment_id == "c2"
        assert comment.content == "Any update?"
        assert comment.is_internal is False
        body = json.loads(route.calls[0].request.content)
        assert body == {"content": "Any update?"}

    @respx.mock
    def test_add_comment_passes_is_internal_when_set(
        self, client: Sonzai, base_url: str
    ) -> None:
        route = respx.post(f"{base_url}/api/v1/support/tickets/t1/comments").mock(
            return_value=httpx.Response(
                200,
                json={
                    "comment_id": "c3",
                    "ticket_id": "t1",
                    "author_id": "user-1",
                    "author_email": "user@example.com",
                    "author_type": "user",
                    "content": "Internal note",
                    "is_internal": False,
                    "created_at": "2026-04-21T11:00:00Z",
                },
            )
        )

        client.support.add_comment("t1", content="Internal note", is_internal=True)
        body = json.loads(route.calls[0].request.content)
        assert body == {"content": "Internal note", "is_internal": True}


# ---------------------------------------------------------------------------
# Async parity
# ---------------------------------------------------------------------------


class TestSupportAsync:
    @respx.mock
    async def test_list_async(self, base_url: str) -> None:
        respx.get(f"{base_url}/api/v1/support/tickets").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tickets": [
                        {
                            "ticket_id": "t1",
                            "title": "T",
                            "type": "support",
                            "status": "open",
                            "priority": "medium",
                            "created_by_email": "u@example.com",
                            "comment_count": 0,
                            "created_at": "2026-04-21T10:00:00Z",
                            "updated_at": "2026-04-21T10:00:00Z",
                        }
                    ],
                    "total": 1,
                    "has_more": False,
                },
            )
        )

        client = AsyncSonzai(api_key="test-key", base_url=base_url)
        try:
            result = await client.support.list_tickets()
        finally:
            await client.close()
        assert len(result.tickets) == 1
        assert result.tickets[0].ticket_id == "t1"

    @respx.mock
    async def test_create_async(self, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/support/tickets").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ticket_id": "t1",
                    "tenant_id": "tenant-a",
                    "created_by": "user-1",
                    "created_by_email": "u@example.com",
                    "title": "T",
                    "description": "D",
                    "type": "bug",
                    "status": "open",
                    "priority": "high",
                    "created_at": "2026-04-21T10:00:00Z",
                    "updated_at": "2026-04-21T10:00:00Z",
                },
            )
        )

        client = AsyncSonzai(api_key="test-key", base_url=base_url)
        try:
            ticket = await client.support.create_ticket(
                title="T", description="D", type="bug", priority="high"
            )
        finally:
            await client.close()
        assert ticket.type == "bug"
        assert ticket.priority == "high"
        body = json.loads(route.calls[0].request.content)
        assert body == {
            "title": "T",
            "description": "D",
            "type": "bug",
            "priority": "high",
        }

    @respx.mock
    async def test_get_async(self, base_url: str) -> None:
        respx.get(f"{base_url}/api/v1/support/tickets/t1").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ticket": {
                        "ticket_id": "t1",
                        "tenant_id": "tenant-a",
                        "created_by": "user-1",
                        "created_by_email": "u@example.com",
                        "title": "T",
                        "description": "D",
                        "type": "support",
                        "status": "open",
                        "priority": "medium",
                        "created_at": "2026-04-21T10:00:00Z",
                        "updated_at": "2026-04-21T10:00:00Z",
                    }
                },
            )
        )

        client = AsyncSonzai(api_key="test-key", base_url=base_url)
        try:
            detail = await client.support.get_ticket("t1")
        finally:
            await client.close()
        assert detail.ticket.ticket_id == "t1"
        assert detail.history is None

    @respx.mock
    async def test_close_async(self, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/support/tickets/t1/close").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ticket_id": "t1",
                    "tenant_id": "tenant-a",
                    "created_by": "user-1",
                    "created_by_email": "u@example.com",
                    "title": "T",
                    "description": "D",
                    "type": "support",
                    "status": "closed",
                    "priority": "medium",
                    "created_at": "2026-04-21T10:00:00Z",
                    "updated_at": "2026-04-21T10:30:00Z",
                },
            )
        )

        client = AsyncSonzai(api_key="test-key", base_url=base_url)
        try:
            ticket = await client.support.close_ticket("t1")
        finally:
            await client.close()
        assert ticket.status == "closed"

    @respx.mock
    async def test_add_comment_async(self, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/support/tickets/t1/comments").mock(
            return_value=httpx.Response(
                200,
                json={
                    "comment_id": "c1",
                    "ticket_id": "t1",
                    "author_id": "user-1",
                    "author_email": "u@example.com",
                    "author_type": "user",
                    "content": "Hello",
                    "is_internal": False,
                    "created_at": "2026-04-21T11:00:00Z",
                },
            )
        )

        client = AsyncSonzai(api_key="test-key", base_url=base_url)
        try:
            comment = await client.support.add_comment("t1", content="Hello")
        finally:
            await client.close()
        assert comment.comment_id == "c1"
        body = json.loads(route.calls[0].request.content)
        assert body == {"content": "Hello"}


# ---------------------------------------------------------------------------
# Client wiring
# ---------------------------------------------------------------------------


def test_support_is_wired_on_sync_client() -> None:
    client = Sonzai(api_key="test-key")
    try:
        assert isinstance(client.support, Support)
    finally:
        client.close()


def test_support_is_wired_on_async_client() -> None:
    client = AsyncSonzai(api_key="test-key")
    assert isinstance(client.support, AsyncSupport)
