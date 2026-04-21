"""Storefront resource.

Wraps endpoints under ``/storefront/...``. Returns raw dicts because the
OpenAPI schemas for these endpoints are mostly free-form objects; grab
typed models from ``sonzai._generated.models`` when you need stronger
typing.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .._http import AsyncHTTPClient, HTTPClient


class Storefront:
    """Sync storefront config + published agents."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def get(self) -> dict[str, Any]:
        """Get the storefront config."""
        return self._http.get("/api/v1/storefront")  # type: ignore[no-any-return]

    def update(self, **body: Any) -> dict[str, Any]:
        """Update storefront config."""
        return self._http.put("/api/v1/storefront", json_data=body)  # type: ignore[no-any-return]

    def publish(self, **body: Any) -> dict[str, Any]:
        """Publish the storefront."""
        return self._http.post("/api/v1/storefront/publish", json_data=body)  # type: ignore[no-any-return]

    def unpublish(self, **body: Any) -> dict[str, Any]:
        """Unpublish the storefront."""
        return self._http.post("/api/v1/storefront/unpublish", json_data=body)  # type: ignore[no-any-return]

    def list_agents(self) -> dict[str, Any]:
        """List agents on the storefront."""
        return self._http.get("/api/v1/storefront/agents")  # type: ignore[no-any-return]

    def upsert_agent(self, agent_id: str, **body: Any) -> dict[str, Any]:
        """Add or update an agent on the storefront."""
        return self._http.put(  # type: ignore[no-any-return]
            f"/api/v1/storefront/agents/{quote(agent_id, safe='')}",
            json_data=body,
        )

    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent from the storefront."""
        self._http.delete(f"/api/v1/storefront/agents/{quote(agent_id, safe='')}")


class AsyncStorefront:
    """Async storefront operations (mirror of :class:`Storefront`)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def get(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/storefront")  # type: ignore[no-any-return]

    async def update(self, **body: Any) -> dict[str, Any]:
        return await self._http.put("/api/v1/storefront", json_data=body)  # type: ignore[no-any-return]

    async def publish(self, **body: Any) -> dict[str, Any]:
        return await self._http.post("/api/v1/storefront/publish", json_data=body)  # type: ignore[no-any-return]

    async def unpublish(self, **body: Any) -> dict[str, Any]:
        return await self._http.post("/api/v1/storefront/unpublish", json_data=body)  # type: ignore[no-any-return]

    async def list_agents(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/storefront/agents")  # type: ignore[no-any-return]

    async def upsert_agent(self, agent_id: str, **body: Any) -> dict[str, Any]:
        return await self._http.put(  # type: ignore[no-any-return]
            f"/api/v1/storefront/agents/{quote(agent_id, safe='')}",
            json_data=body,
        )

    async def remove_agent(self, agent_id: str) -> None:
        await self._http.delete(
            f"/api/v1/storefront/agents/{quote(agent_id, safe='')}"
        )
