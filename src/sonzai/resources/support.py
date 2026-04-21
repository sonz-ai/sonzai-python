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

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    SupportTicket,
    SupportTicketComment,
    TicketDetailResponse,
    TicketListResponse,
)


class Support:
    """Sync support-ticket operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list_tickets(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        status: str | None = None,
        type: str | None = None,
    ) -> TicketListResponse:
        """List the caller's support tickets within their active tenant.

        Args:
            limit: Items per page (server default 20, max 100).
            offset: Pagination offset (server default 0).
            status: Filter by status (``open``, ``in_progress``, ``resolved``,
                ``closed``).
            type: Filter by type (``support``, ``bug``, ``feature_request``,
                ``billing``, ...).
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if status is not None:
            params["status"] = status
        if type is not None:
            params["type"] = type
        data = self._http.get("/api/v1/support/tickets", params=params or None)
        return TicketListResponse.model_validate(data)

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
        body: dict[str, Any] = {
            "title": title,
            "description": description,
            "type": type,
        }
        if priority is not None:
            body["priority"] = priority
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
        body: dict[str, Any] = {"content": content}
        if is_internal is not None:
            body["is_internal"] = is_internal
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


class AsyncSupport:
    """Async support-ticket operations (mirror of :class:`Support`)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list_tickets(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        status: str | None = None,
        type: str | None = None,
    ) -> TicketListResponse:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if status is not None:
            params["status"] = status
        if type is not None:
            params["type"] = type
        data = await self._http.get(
            "/api/v1/support/tickets", params=params or None
        )
        return TicketListResponse.model_validate(data)

    async def create_ticket(
        self,
        *,
        title: str,
        description: str,
        type: str,
        priority: str | None = None,
    ) -> SupportTicket:
        body: dict[str, Any] = {
            "title": title,
            "description": description,
            "type": type,
        }
        if priority is not None:
            body["priority"] = priority
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
        body: dict[str, Any] = {"content": content}
        if is_internal is not None:
            body["is_internal"] = is_internal
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
