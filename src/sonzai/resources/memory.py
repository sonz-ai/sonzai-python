"""Memory resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import MemoryResponse, MemorySearchResponse, MemoryTimelineResponse


class Memory:
    """Sync memory operations for an agent."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
        instance_id: str | None = None,
        parent_id: str | None = None,
        include_contents: bool = False,
        limit: int = 50,
    ) -> MemoryResponse:
        """Get the memory tree for an agent."""
        params: dict[str, Any] = {"limit": limit}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        if parent_id:
            params["parent_id"] = parent_id
        if include_contents:
            params["include_contents"] = "true"

        data = self._http.get(f"/api/v1/agents/{agent_id}/memory", params=params)
        return MemoryResponse.model_validate(data)

    def search(
        self,
        agent_id: str,
        *,
        query: str,
        instance_id: str | None = None,
        limit: int = 20,
    ) -> MemorySearchResponse:
        """Search agent memories."""
        params: dict[str, Any] = {"q": query, "limit": limit}
        if instance_id:
            params["instance_id"] = instance_id

        data = self._http.get(
            f"/api/v1/agents/{agent_id}/memory/search", params=params
        )
        return MemorySearchResponse.model_validate(data)

    def timeline(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
        instance_id: str | None = None,
        start: str | None = None,
        end: str | None = None,
    ) -> MemoryTimelineResponse:
        """Get memory timeline for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        data = self._http.get(
            f"/api/v1/agents/{agent_id}/memory/timeline", params=params
        )
        return MemoryTimelineResponse.model_validate(data)


class AsyncMemory:
    """Async memory operations for an agent."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
        instance_id: str | None = None,
        parent_id: str | None = None,
        include_contents: bool = False,
        limit: int = 50,
    ) -> MemoryResponse:
        params: dict[str, Any] = {"limit": limit}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        if parent_id:
            params["parent_id"] = parent_id
        if include_contents:
            params["include_contents"] = "true"

        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/memory", params=params
        )
        return MemoryResponse.model_validate(data)

    async def search(
        self,
        agent_id: str,
        *,
        query: str,
        instance_id: str | None = None,
        limit: int = 20,
    ) -> MemorySearchResponse:
        params: dict[str, Any] = {"q": query, "limit": limit}
        if instance_id:
            params["instance_id"] = instance_id

        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/memory/search", params=params
        )
        return MemorySearchResponse.model_validate(data)

    async def timeline(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
        instance_id: str | None = None,
        start: str | None = None,
        end: str | None = None,
    ) -> MemoryTimelineResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/memory/timeline", params=params
        )
        return MemoryTimelineResponse.model_validate(data)
