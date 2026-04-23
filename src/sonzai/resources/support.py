"""Support tickets resource.

Wraps endpoints under ``/support/tickets/...``. These are authenticated via
the caller's Clerk session (``bearerClerk`` in the OpenAPI spec); the same
:class:`HTTPClient` carries the bearer token — callers just point it at a
session token instead of a project API key. Every operation is scoped to
the caller's active tenant, and ``list_tickets`` / ``close_ticket`` are
additionally scoped to the caller's own user id, which the server resolves
from the bearer token.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .._generated.models import AddCommentRequest, CreateTicketRequest
from .._generated.resources.support import AsyncSupport as _GenAsyncSupport
from .._generated.resources.support import Support as _GenSupport
from .._http import AsyncHTTPClient, HTTPClient
from .._pagination import AsyncPage, Page
from .._request_helpers import encode_body
from ..types import (
    SupportTicket,
    SupportTicketComment,
    TicketDetailResponse,
    TicketListResponse,
    TicketSummary,
)


class Support(_GenSupport):
    """Hand-written overrides / convenience helpers on top of generated Support.

    All hand-written methods remain as overrides preserving the historical SDK
    contract. The subclass inheritance makes future spec additions appear as
    inherited methods automatically.
    """

    # TODO(B.3-followup): __init__ takes HTTPClient (typed); generated _SupportBase
    # takes Any. Override kept to preserve typed constructor signature.
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list_tickets(
        self,
        *,
        limit: int = 100,
        status: str | None = None,
        type: str | None = None,
    ) -> Page[TicketSummary]:
        """List the caller's support tickets within their active tenant.

        Args:
            limit: Items per page (max 100).
            status: Filter by status (``open``, ``in_progress``, ``resolved``,
                ``closed``).
            type: Filter by type (``support``, ``bug``, ``feature_request``,
                ``billing``, ...).
        """
        params: dict[str, Any] = {"limit": limit, "offset": 0}
        if status is not None:
            params["status"] = status
        if type is not None:
            params["type"] = type
        return Page(
            fetcher=lambda p: self._http.get("/api/v1/support/tickets", params=p),
            params=params,
            item_key="tickets",
            item_parser=TicketSummary.model_validate,
            mode="offset",
            total_key="total",
        )

    def create_ticket(
        self,
        *,
        title: str,
        description: str,
        type: str,
        priority: str | None = None,
    ) -> SupportTicket:
        """Create a support ticket in the caller's tenant.

        ``priority`` defaults to ``medium`` server-side when omitted.
        """
        raw: dict[str, Any] = {
            "title": title,
            "description": description,
            "type": type,
        }
        if priority is not None:
            raw["priority"] = priority
        body = encode_body(CreateTicketRequest, raw)
        data = self._http.post("/api/v1/support/tickets", json_data=body)
        return SupportTicket.model_validate(data)

    def get_ticket(self, ticket_id: str) -> TicketDetailResponse:
        """Get a ticket and its comment thread by ID.

        Returns 404 when the ticket belongs to a different tenant.
        """
        data = self._http.get(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}"
        )
        return TicketDetailResponse.model_validate(data)

    def add_comment(
        self,
        ticket_id: str,
        *,
        content: str,
        is_internal: bool | None = None,
    ) -> SupportTicketComment:
        """Append a user comment to the ticket thread.

        User comments are always external (``is_internal=false``); only staff
        can create internal comments via the admin portal, and the server
        will override the flag accordingly.
        """
        raw: dict[str, Any] = {"content": content}
        if is_internal is not None:
            raw["is_internal"] = is_internal
        body = encode_body(AddCommentRequest, raw)
        data = self._http.post(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/comments",
            json_data=body,
        )
        return SupportTicketComment.model_validate(data)

    def close_ticket(self, ticket_id: str) -> SupportTicket:
        """Close a ticket. Only the original creator can close their ticket."""
        data = self._http.post(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/close"
        )
        return SupportTicket.model_validate(data)


class AsyncSupport(_GenAsyncSupport):
    """Async hand-written overrides on top of generated AsyncSupport."""

    # TODO(B.3-followup): __init__ takes AsyncHTTPClient (typed); generated base
    # takes Any. Override kept to preserve typed constructor signature.
    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list_tickets(
        self,
        *,
        limit: int = 100,
        status: str | None = None,
        type: str | None = None,
    ) -> AsyncPage[TicketSummary]:
        params: dict[str, Any] = {"limit": limit, "offset": 0}
        if status is not None:
            params["status"] = status
        if type is not None:
            params["type"] = type

        async def fetcher(p: dict[str, Any]) -> dict[str, Any]:
            return await self._http.get("/api/v1/support/tickets", params=p)

        return AsyncPage(
            fetcher=fetcher,
            params=params,
            item_key="tickets",
            item_parser=TicketSummary.model_validate,
            mode="offset",
            total_key="total",
        )

    async def create_ticket(
        self,
        *,
        title: str,
        description: str,
        type: str,
        priority: str | None = None,
    ) -> SupportTicket:
        raw: dict[str, Any] = {
            "title": title,
            "description": description,
            "type": type,
        }
        if priority is not None:
            raw["priority"] = priority
        body = encode_body(CreateTicketRequest, raw)
        data = await self._http.post("/api/v1/support/tickets", json_data=body)
        return SupportTicket.model_validate(data)

    async def get_ticket(self, ticket_id: str) -> TicketDetailResponse:
        data = await self._http.get(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}"
        )
        return TicketDetailResponse.model_validate(data)

    async def add_comment(
        self,
        ticket_id: str,
        *,
        content: str,
        is_internal: bool | None = None,
    ) -> SupportTicketComment:
        raw: dict[str, Any] = {"content": content}
        if is_internal is not None:
            raw["is_internal"] = is_internal
        body = encode_body(AddCommentRequest, raw)
        data = await self._http.post(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/comments",
            json_data=body,
        )
        return SupportTicketComment.model_validate(data)

    async def close_ticket(self, ticket_id: str) -> SupportTicket:
        data = await self._http.post(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/close"
        )
        return SupportTicket.model_validate(data)
