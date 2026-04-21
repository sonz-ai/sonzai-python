"""Support tickets resource for the Sonzai SDK.

The support ticket endpoints are authenticated via the caller's Clerk session
(``bearerClerk`` in the OpenAPI spec). The same :class:`HTTPClient` carries the
bearer token; callers just point it at a session token instead of a project
API key. Every operation is scoped to the caller's active tenant and, for the
close/list paths, to the caller's own user id — the server resolves both from
the bearer token.
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


class SupportTickets:
    """Sync support ticket operations (list, create, get, close, comment)."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(
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

        data = self._http.get("/api/v1/support/tickets", params=params)
        return TicketListResponse.model_validate(data)

    def create(
        self,
        *,
        title: str,
        description: str,
        type: str,
        priority: str | None = None,
    ) -> SupportTicket:
        """Create a support ticket in the caller's tenant.

        ``type`` defaults to ``support`` and ``priority`` to ``medium`` when
        omitted server-side.
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

    def get(self, ticket_id: str) -> TicketDetailResponse:
        """Get a ticket and its comment thread by ID.

        Returns 404 when the ticket belongs to a different tenant.
        """
        data = self._http.get(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}"
        )
        return TicketDetailResponse.model_validate(data)

    def close(self, ticket_id: str) -> SupportTicket:
        """Close a ticket. Only the original creator can close their ticket."""
        data = self._http.post(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/close"
        )
        return SupportTicket.model_validate(data)

    def add_comment(
        self,
        ticket_id: str,
        *,
        content: str,
        is_internal: bool | None = None,
    ) -> SupportTicketComment:
        """Append a user comment to the ticket thread.

        User comments are always external (``is_internal=false``); only staff
        can create internal comments via the admin portal, and the server will
        override the flag accordingly.
        """
        body: dict[str, Any] = {"content": content}
        if is_internal is not None:
            body["is_internal"] = is_internal

        data = self._http.post(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/comments",
            json_data=body,
        )
        return SupportTicketComment.model_validate(data)


class AsyncSupportTickets:
    """Async support ticket operations (list, create, get, close, comment)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(
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

        data = await self._http.get("/api/v1/support/tickets", params=params)
        return TicketListResponse.model_validate(data)

    async def create(
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

    async def get(self, ticket_id: str) -> TicketDetailResponse:
        data = await self._http.get(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}"
        )
        return TicketDetailResponse.model_validate(data)

    async def close(self, ticket_id: str) -> SupportTicket:
        data = await self._http.post(
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/close"
        )
        return SupportTicket.model_validate(data)

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
