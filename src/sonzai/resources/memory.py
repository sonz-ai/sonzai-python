"""Memory resource for the Sonzai SDK."""

from __future__ import annotations

import builtins
from typing import Any
from urllib.parse import quote

_list = builtins.list

from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body
from .._generated.models import (
    CreateFactInputBody,
    UpdateFactInputBody,
)
from ..types import (
    AtomicFact,
    DeleteWisdomResponse,
    FactHistoryResponse,
    FactListResponse,
    MemoryResetResponse,
    MemoryResponse,
    MemorySearchResponse,
    MemoryTimelineResponse,
    SeedMemoriesResponse,
    WisdomAuditResponse,
)


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
        scope: str | None = None,
        memory_type: str | None = None,
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
        if scope is not None:
            params["scope"] = scope
        if memory_type is not None:
            params["memory_type"] = memory_type

        data = self._http.get(f"/api/v1/agents/{agent_id}/memory", params=params)
        return MemoryResponse.model_validate(data)

    def search(
        self,
        agent_id: str,
        *,
        query: str,
        user_id: str | None = None,
        instance_id: str | None = None,
        mode: str | None = None,
        limit: int = 20,
    ) -> MemorySearchResponse:
        """Search agent memories.

        Passing ``user_id`` opts into semantic (cosine) retrieval over fact
        embeddings. Without it the server falls back to BM25 token search.
        ``mode`` can force ``"bm25"`` or ``"semantic"`` explicitly.
        """
        params: dict[str, Any] = {"q": query, "limit": limit}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        if mode:
            params["mode"] = mode

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

    def seed(
        self,
        agent_id: str,
        *,
        user_id: str,
        memories: _list[dict[str, Any]],
        instance_id: str | None = None,
    ) -> SeedMemoriesResponse:
        """Bulk import initial memories for an agent during setup."""
        body: dict[str, Any] = {
            "user_id": user_id,
            "memories": memories,
        }
        if instance_id is not None:
            body["instance_id"] = instance_id

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/memory/seed", json_data=body
        )
        return SeedMemoriesResponse.model_validate(data)

    def list_facts(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
        fact_type: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> FactListResponse:
        """List atomic facts for an agent, optionally filtered by fact type."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if fact_type:
            params["fact_type"] = fact_type
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        data = self._http.get(
            f"/api/v1/agents/{agent_id}/memory/facts", params=params
        )
        return FactListResponse.model_validate(data)

    def reset(
        self,
        agent_id: str,
        *,
        user_id: str,
        instance_id: str | None = None,
    ) -> MemoryResetResponse:
        """Delete all memory for an agent scoped to a user."""
        params: dict[str, Any] = {"user_id": user_id}
        if instance_id:
            params["instance_id"] = instance_id

        data = self._http.delete(
            f"/api/v1/agents/{agent_id}/memory",
            params=params,
        )
        if isinstance(data, dict):
            return MemoryResetResponse.model_validate(data)
        return MemoryResetResponse(agent_id=agent_id, status="reset")

    def create_fact(
        self,
        agent_id: str,
        *,
        content: str,
        user_id: str | None = None,
        fact_type: str | None = None,
        importance: float | None = None,
        confidence: float | None = None,
        entities: _list[str] | None = None,
        node_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AtomicFact:
        """Create a new fact for an agent. Facts are tagged source_type='manual'."""
        body: dict[str, Any] = {"content": content}
        if user_id is not None:
            body["user_id"] = user_id
        if fact_type is not None:
            body["fact_type"] = fact_type
        if importance is not None:
            body["importance"] = importance
        if confidence is not None:
            body["confidence"] = confidence
        if entities is not None:
            body["entities"] = entities
        if node_id is not None:
            body["node_id"] = node_id
        if metadata is not None:
            body["metadata"] = metadata
        data = self._http.post(
            f"/api/v1/agents/{agent_id}/memory/facts", json_data=encode_body(CreateFactInputBody, body)
        )
        return AtomicFact.model_validate(data)

    def update_fact(
        self,
        agent_id: str,
        fact_id: str,
        *,
        content: str | None = None,
        fact_type: str | None = None,
        importance: float | None = None,
        confidence: float | None = None,
        entities: _list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AtomicFact:
        """Update an existing fact by ID."""
        body: dict[str, Any] = {}
        if content is not None:
            body["content"] = content
        if fact_type is not None:
            body["fact_type"] = fact_type
        if importance is not None:
            body["importance"] = importance
        if confidence is not None:
            body["confidence"] = confidence
        if entities is not None:
            body["entities"] = entities
        if metadata is not None:
            body["metadata"] = metadata
        data = self._http.put(
            f"/api/v1/agents/{agent_id}/memory/facts/{quote(fact_id, safe='')}", json_data=encode_body(UpdateFactInputBody, body)
        )
        return AtomicFact.model_validate(data)

    def delete_fact(self, agent_id: str, fact_id: str) -> None:
        """Delete a fact by ID."""
        self._http.delete(f"/api/v1/agents/{agent_id}/memory/facts/{quote(fact_id, safe='')}")

    def get_fact_history(self, agent_id: str, fact_id: str) -> FactHistoryResponse:
        """Get the version history for a specific fact."""
        return FactHistoryResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/memory/fact/{fact_id}/history")
        )

    def delete_wisdom_fact(self, agent_id: str, fact_id: str) -> DeleteWisdomResponse:
        """Delete a wisdom fact by ID."""
        data = self._http.delete(
            f"/api/v1/agents/{agent_id}/memory/wisdom/{quote(fact_id, safe='')}"
        )
        if isinstance(data, dict):
            return DeleteWisdomResponse.model_validate(data)
        return DeleteWisdomResponse(success=True, fact_id=fact_id)

    def get_wisdom_audit(self, agent_id: str, fact_id: str) -> WisdomAuditResponse:
        """Get the audit trail for a wisdom fact."""
        return WisdomAuditResponse.model_validate(
            self._http.get(
                f"/api/v1/agents/{agent_id}/memory/wisdom/audit/{quote(fact_id, safe='')}"
            )
        )


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
        scope: str | None = None,
        memory_type: str | None = None,
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
        if scope is not None:
            params["scope"] = scope
        if memory_type is not None:
            params["memory_type"] = memory_type

        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/memory", params=params
        )
        return MemoryResponse.model_validate(data)

    async def search(
        self,
        agent_id: str,
        *,
        query: str,
        user_id: str | None = None,
        instance_id: str | None = None,
        mode: str | None = None,
        limit: int = 20,
    ) -> MemorySearchResponse:
        """Search agent memories.

        Passing ``user_id`` opts into semantic (cosine) retrieval over fact
        embeddings. Without it the server falls back to BM25 token search.
        ``mode`` can force ``"bm25"`` or ``"semantic"`` explicitly.
        """
        params: dict[str, Any] = {"q": query, "limit": limit}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        if mode:
            params["mode"] = mode

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

    async def seed(
        self,
        agent_id: str,
        *,
        user_id: str,
        memories: _list[dict[str, Any]],
        instance_id: str | None = None,
    ) -> SeedMemoriesResponse:
        """Bulk import initial memories for an agent during setup."""
        body: dict[str, Any] = {
            "user_id": user_id,
            "memories": memories,
        }
        if instance_id is not None:
            body["instance_id"] = instance_id

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/memory/seed", json_data=body
        )
        return SeedMemoriesResponse.model_validate(data)

    async def list_facts(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
        fact_type: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> FactListResponse:
        """List atomic facts for an agent, optionally filtered by fact type."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if fact_type:
            params["fact_type"] = fact_type
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/memory/facts", params=params
        )
        return FactListResponse.model_validate(data)

    async def reset(
        self,
        agent_id: str,
        *,
        user_id: str,
        instance_id: str | None = None,
    ) -> MemoryResetResponse:
        """Delete all memory for an agent scoped to a user."""
        params: dict[str, Any] = {"user_id": user_id}
        if instance_id:
            params["instance_id"] = instance_id

        data = await self._http.delete(
            f"/api/v1/agents/{agent_id}/memory",
            params=params,
        )
        if isinstance(data, dict):
            return MemoryResetResponse.model_validate(data)
        return MemoryResetResponse(agent_id=agent_id, status="reset")

    async def create_fact(
        self,
        agent_id: str,
        *,
        content: str,
        user_id: str | None = None,
        fact_type: str | None = None,
        importance: float | None = None,
        confidence: float | None = None,
        entities: _list[str] | None = None,
        node_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AtomicFact:
        """Create a new fact for an agent. Facts are tagged source_type='manual'."""
        body: dict[str, Any] = {"content": content}
        if user_id is not None:
            body["user_id"] = user_id
        if fact_type is not None:
            body["fact_type"] = fact_type
        if importance is not None:
            body["importance"] = importance
        if confidence is not None:
            body["confidence"] = confidence
        if entities is not None:
            body["entities"] = entities
        if node_id is not None:
            body["node_id"] = node_id
        if metadata is not None:
            body["metadata"] = metadata
        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/memory/facts", json_data=encode_body(CreateFactInputBody, body)
        )
        return AtomicFact.model_validate(data)

    async def update_fact(
        self,
        agent_id: str,
        fact_id: str,
        *,
        content: str | None = None,
        fact_type: str | None = None,
        importance: float | None = None,
        confidence: float | None = None,
        entities: _list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AtomicFact:
        """Update an existing fact by ID."""
        body: dict[str, Any] = {}
        if content is not None:
            body["content"] = content
        if fact_type is not None:
            body["fact_type"] = fact_type
        if importance is not None:
            body["importance"] = importance
        if confidence is not None:
            body["confidence"] = confidence
        if entities is not None:
            body["entities"] = entities
        if metadata is not None:
            body["metadata"] = metadata
        data = await self._http.put(
            f"/api/v1/agents/{agent_id}/memory/facts/{quote(fact_id, safe='')}", json_data=encode_body(UpdateFactInputBody, body)
        )
        return AtomicFact.model_validate(data)

    async def delete_fact(self, agent_id: str, fact_id: str) -> None:
        """Delete a fact by ID."""
        await self._http.delete(f"/api/v1/agents/{agent_id}/memory/facts/{quote(fact_id, safe='')}")

    async def get_fact_history(self, agent_id: str, fact_id: str) -> FactHistoryResponse:
        """Get the version history for a specific fact."""
        return FactHistoryResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/memory/fact/{fact_id}/history")
        )

    async def delete_wisdom_fact(self, agent_id: str, fact_id: str) -> DeleteWisdomResponse:
        """Delete a wisdom fact by ID."""
        data = await self._http.delete(
            f"/api/v1/agents/{agent_id}/memory/wisdom/{quote(fact_id, safe='')}"
        )
        if isinstance(data, dict):
            return DeleteWisdomResponse.model_validate(data)
        return DeleteWisdomResponse(success=True, fact_id=fact_id)

    async def get_wisdom_audit(self, agent_id: str, fact_id: str) -> WisdomAuditResponse:
        """Get the audit trail for a wisdom fact."""
        return WisdomAuditResponse.model_validate(
            await self._http.get(
                f"/api/v1/agents/{agent_id}/memory/wisdom/audit/{quote(fact_id, safe='')}"
            )
        )
