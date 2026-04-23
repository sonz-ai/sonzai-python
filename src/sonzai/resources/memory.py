"""Memory resource — thin convenience layer over the generated class.

Any method defined in the spec is inherited from the generated parent
class. Only non-spec helpers and spec-drift overrides belong here.

B.2 CONCERNS SURFACED (all overrides below are marked TODO(B.2)):
  1. Generator emits camelCase variable names in f-strings (e.g. {agentId})
     but method params are snake_case (agent_id). All generated methods raise
     NameError at runtime until this is fixed.
  2. Generator calls self._http.post(..., body=body) but HTTPClient only
     accepts json_data=. Wrong kwarg name breaks all POST/PUT calls.
  3. Generator uses /agents/... path prefix instead of /api/v1/agents/...
     (missing base path prefix).
  4. Method names diverge: generated uses get_memory_tree / search_memories /
     reset_memory / get_memory_timeline; historical SDK contract uses list /
     search / reset / timeline.
  5. search() uses `query` kwarg; generated uses `q`.
  6. list_facts() has `offset` param not present in generated.
  7. create_fact() / update_fact() use explicit kwargs; generated uses
     **body_fields (loses IDE autocomplete and type checking).
  8. seed() method is absent from the generated class entirely.

Until B.2 fixes these, every method requires an override to preserve the
historical SDK contract. The subclass structure is proven below — once the
generator is corrected, overrides can be removed one by one.
"""

from __future__ import annotations

import builtins
from typing import Any
from urllib.parse import quote

_list = builtins.list

from .._generated.resources.memory import AsyncMemory as _GenAsyncMemory
from .._generated.resources.memory import Memory as _GenMemory
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


class Memory(_GenMemory):
    """Hand-written convenience layer on top of the generated Memory class.

    Overrides every method because B.2 generator bugs (camelCase f-string
    vars, wrong HTTP body kwarg, missing /api/v1 path prefix) make all
    generated implementations non-functional at runtime. Each override is
    marked TODO(B.2) and will shrink as the generator is hardened.
    """

    # TODO(B.2): Remove this __init__ override once the generated base class
    # accepts the concrete HTTPClient type (currently typed as Any which is
    # fine, but the historical __init__ is kept for explicitness).
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    # TODO(B.2): Generator names this get_memory_tree; historical contract is list.
    # Also fixes: camelCase {agentId} → {agent_id}, /agents/ → /api/v1/agents/,
    # include_contents default (False → str), limit default (50 → None).
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

    # TODO(B.2): Generator names this search_memories and uses `q` kwarg;
    # historical contract is search(..., query=...). Also fixes path prefix
    # and camelCase variable bug.
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

    # TODO(B.2): Generator names this get_memory_timeline; historical is timeline.
    # Also fixes path prefix and camelCase variable bug.
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

    # TODO(B.2): seed() is absent from the generated class entirely. Generator
    # needs to emit this method from the spec's seed endpoint.
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

        # NOTE: not routed through encode_body — the spec's
        # GenerateSeedMemoriesInputBody under this path maps to a different
        # endpoint variant (generate vs. seed); the actual seed body shape
        # (user_id + memories list) has no matching InputBody class.
        data = self._http.post(
            f"/api/v1/agents/{agent_id}/memory/seed", json_data=body
        )
        return SeedMemoriesResponse.model_validate(data)

    # TODO(B.2): Generated list_facts uses **body_fields (should be explicit
    # kwargs), is missing `offset` param, and has camelCase + path prefix bugs.
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

    # TODO(B.2): Generator names this reset_memory; historical contract is reset.
    # Also fixes camelCase {agentId} and path prefix, and adds fallback for
    # non-dict responses.
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

    # TODO(B.2): Generated create_fact uses **body_fields — loses explicit
    # kwarg names for IDE autocomplete. Also has wrong HTTP body kwarg (body=
    # vs json_data=), camelCase variable bug, and path prefix bug.
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
            f"/api/v1/agents/{agent_id}/memory/facts",
            json_data=encode_body(CreateFactInputBody, body),
        )
        return AtomicFact.model_validate(data)

    # TODO(B.2): Generated update_fact uses **body_fields, wrong HTTP body
    # kwarg (body= vs json_data=), camelCase variable, and path prefix bugs.
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
            f"/api/v1/agents/{agent_id}/memory/facts/{quote(fact_id, safe='')}",
            json_data=encode_body(UpdateFactInputBody, body),
        )
        return AtomicFact.model_validate(data)

    # TODO(B.2): delete_fact signature matches generated but generated has
    # camelCase {agentId}/{factId} and path prefix bugs.
    def delete_fact(self, agent_id: str, fact_id: str) -> None:
        """Delete a fact by ID."""
        self._http.delete(
            f"/api/v1/agents/{agent_id}/memory/facts/{quote(fact_id, safe='')}"
        )

    # TODO(B.2): get_fact_history signature matches generated but generated
    # has camelCase {agentId}/{factId} and path prefix bugs.
    def get_fact_history(self, agent_id: str, fact_id: str) -> FactHistoryResponse:
        """Get the version history for a specific fact."""
        return FactHistoryResponse.model_validate(
            self._http.get(
                f"/api/v1/agents/{agent_id}/memory/fact/{fact_id}/history"
            )
        )

    # TODO(B.2): delete_wisdom_fact signature matches generated but generated
    # has camelCase {agentId}/{factId}, path prefix bugs, and no non-dict
    # response fallback.
    def delete_wisdom_fact(self, agent_id: str, fact_id: str) -> DeleteWisdomResponse:
        """Delete a wisdom fact by ID."""
        data = self._http.delete(
            f"/api/v1/agents/{agent_id}/memory/wisdom/{quote(fact_id, safe='')}"
        )
        if isinstance(data, dict):
            return DeleteWisdomResponse.model_validate(data)
        return DeleteWisdomResponse(success=True, fact_id=fact_id)

    # TODO(B.2): get_wisdom_audit signature matches generated but generated
    # has camelCase {agentId}/{factId} and path prefix bugs.
    def get_wisdom_audit(self, agent_id: str, fact_id: str) -> WisdomAuditResponse:
        """Get the audit trail for a wisdom fact."""
        return WisdomAuditResponse.model_validate(
            self._http.get(
                f"/api/v1/agents/{agent_id}/memory/wisdom/audit/{quote(fact_id, safe='')}"
            )
        )


class AsyncMemory(_GenAsyncMemory):
    """Async mirror of Memory — thin convenience layer over generated AsyncMemory.

    All overrides mirror the sync Memory class above. See TODO(B.2) comments
    there for the generator bugs that necessitate each override.
    """

    # TODO(B.2): Same as sync — keep explicit HTTPClient type.
    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    # TODO(B.2): Generator names this get_memory_tree; historical is list.
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

    # TODO(B.2): Generator names this search_memories with `q` kwarg;
    # historical is search(..., query=...).
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

    # TODO(B.2): Generator names this get_memory_timeline; historical is timeline.
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

    # TODO(B.2): seed() absent from generated class; generator must emit it.
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

        # NOTE: not routed through encode_body — see sync `seed()` above.
        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/memory/seed", json_data=body
        )
        return SeedMemoriesResponse.model_validate(data)

    # TODO(B.2): Generated list_facts missing `offset`, uses **body_fields,
    # camelCase variable, and path prefix bugs.
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

    # TODO(B.2): Generator names this reset_memory; historical is reset.
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

    # TODO(B.2): Generated create_fact uses **body_fields, wrong HTTP body
    # kwarg, camelCase variable, and path prefix bugs.
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
            f"/api/v1/agents/{agent_id}/memory/facts",
            json_data=encode_body(CreateFactInputBody, body),
        )
        return AtomicFact.model_validate(data)

    # TODO(B.2): Generated update_fact uses **body_fields, wrong HTTP body
    # kwarg, camelCase variable, and path prefix bugs.
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
            f"/api/v1/agents/{agent_id}/memory/facts/{quote(fact_id, safe='')}",
            json_data=encode_body(UpdateFactInputBody, body),
        )
        return AtomicFact.model_validate(data)

    # TODO(B.2): delete_fact signature matches generated but generated has
    # camelCase {agentId}/{factId} and path prefix bugs.
    async def delete_fact(self, agent_id: str, fact_id: str) -> None:
        """Delete a fact by ID."""
        await self._http.delete(
            f"/api/v1/agents/{agent_id}/memory/facts/{quote(fact_id, safe='')}"
        )

    # TODO(B.2): get_fact_history signature matches generated but generated
    # has camelCase {agentId}/{factId} and path prefix bugs.
    async def get_fact_history(
        self, agent_id: str, fact_id: str
    ) -> FactHistoryResponse:
        """Get the version history for a specific fact."""
        return FactHistoryResponse.model_validate(
            await self._http.get(
                f"/api/v1/agents/{agent_id}/memory/fact/{fact_id}/history"
            )
        )

    # TODO(B.2): delete_wisdom_fact signature matches generated but generated
    # has camelCase {agentId}/{factId}, path prefix bugs, and no non-dict
    # fallback.
    async def delete_wisdom_fact(
        self, agent_id: str, fact_id: str
    ) -> DeleteWisdomResponse:
        """Delete a wisdom fact by ID."""
        data = await self._http.delete(
            f"/api/v1/agents/{agent_id}/memory/wisdom/{quote(fact_id, safe='')}"
        )
        if isinstance(data, dict):
            return DeleteWisdomResponse.model_validate(data)
        return DeleteWisdomResponse(success=True, fact_id=fact_id)

    # TODO(B.2): get_wisdom_audit signature matches generated but generated
    # has camelCase {agentId}/{factId} and path prefix bugs.
    async def get_wisdom_audit(
        self, agent_id: str, fact_id: str
    ) -> WisdomAuditResponse:
        """Get the audit trail for a wisdom fact."""
        return WisdomAuditResponse.model_validate(
            await self._http.get(
                f"/api/v1/agents/{agent_id}/memory/wisdom/audit/{quote(fact_id, safe='')}"
            )
        )
