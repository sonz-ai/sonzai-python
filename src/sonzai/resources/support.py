"""Support tickets resource.

Wraps endpoints under ``/support/tickets/...``.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .._http import AsyncHTTPClient, HTTPClient


class Support:
    """Sync support-ticket operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list_tickets(self) -> dict[str, Any]:
        """List the caller's support tickets."""
        return self._http.get("/api/v1/support/tickets")  # type: ignore[no-any-return]

    def create_ticket(self, **body: Any) -> dict[str, Any]:
        """Create a support ticket."""
        return self._http.post("/api/v1/support/tickets", json_data=body)  # type: ignore[no-any-return]

    def get_ticket(self, ticket_id: str) -> dict[str, Any]:
        """Get a support ticket with its comments."""
        return self._http.get(  # type: ignore[no-any-return]
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}"
        )

    def add_comment(self, ticket_id: str, **body: Any) -> dict[str, Any]:
        """Add a comment to a support ticket."""
        return self._http.post(  # type: ignore[no-any-return]
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/comments",
            json_data=body,
        )

    def close_ticket(self, ticket_id: str, **body: Any) -> dict[str, Any]:
        """Close a support ticket (user-initiated)."""
        return self._http.post(  # type: ignore[no-any-return]
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/close",
            json_data=body,
        )


class AsyncSupport:
    """Async support-ticket operations (mirror of :class:`Support`)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list_tickets(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/support/tickets")  # type: ignore[no-any-return]

    async def create_ticket(self, **body: Any) -> dict[str, Any]:
        return await self._http.post("/api/v1/support/tickets", json_data=body)  # type: ignore[no-any-return]

    async def get_ticket(self, ticket_id: str) -> dict[str, Any]:
        return await self._http.get(  # type: ignore[no-any-return]
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}"
        )

    async def add_comment(self, ticket_id: str, **body: Any) -> dict[str, Any]:
        return await self._http.post(  # type: ignore[no-any-return]
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/comments",
            json_data=body,
        )

    async def close_ticket(self, ticket_id: str, **body: Any) -> dict[str, Any]:
        return await self._http.post(  # type: ignore[no-any-return]
            f"/api/v1/support/tickets/{quote(ticket_id, safe='')}/close",
            json_data=body,
        )
