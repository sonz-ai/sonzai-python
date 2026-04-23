"""Memory resource — thin convenience layer over the generated class.

Any method defined in the spec is inherited from the generated parent
class unless an override is necessary. Overrides remain for:

  - seed(): Not in spec (spec gap, Bug 8 deferred).
  - list_facts(): Generated is missing `offset` param; spec types limit as
    string but historical contract uses int.
  - reset(): Generated returns ResetMemoryResponse (no agent_id/user_id
    fields); historical contract is MemoryResetResponse + fallback for
    non-dict server responses.
  - create_fact(): Generated has fact_type required; historical treats it as
    optional. Also: generated doesn't URL-encode fact path params.
  - update_fact(): URL-encoding of fact_id needed.
  - delete_fact(): URL-encoding of fact_id; return None vs Any.
  - delete_wisdom_fact(): URL-encoding + fallback for non-dict responses.

B.2 fixes resolved (overrides removed):
  - list(): generator now produces correct method_name, path, and type.
  - search(): generator now uses `query` kwarg (QUERY_PARAM_OVERRIDES), correct
    path and HTTP method.
  - timeline(): generator now uses `timeline` method_name, correct path.
  - get_fact_history(): generator now produces correct path.
  - get_wisdom_audit(): generator now produces correct path.
  - __init__: base class _MemoryBase accepts Any, no override needed.
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
    AtomicFact,
    CreateFactInputBody,
    UpdateFactInputBody,
)
from ..types import (
    DeleteWisdomResponse,
    FactListResponse,
    MemoryResetResponse,
    SeedMemoriesResponse,
)


class Memory(_GenMemory):
    """Hand-written convenience layer on top of the generated Memory class.

    Only non-spec helpers and spec-drift overrides belong here. The bulk of
    Memory methods are now inherited from _GenMemory unchanged.
    """

    # TODO(B.2/Bug8): seed() is absent from the generated class entirely — spec
    # gap. The actual seed body (user_id + memories list) has no matching
    # InputBody class in the spec.
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

    # TODO(B.2/Bug6): Generated list_facts is missing `offset` param (spec only
    # has `limit`). Also `limit` is typed as str in spec, int in historical
    # contract. Also returns ListFactsResponse (generated) vs FactListResponse.
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

    # TODO: Generated reset() returns ResetMemoryResponse which lacks agent_id/
    # user_id fields; historical contract is MemoryResetResponse. Also adds
    # fallback for non-dict server responses.
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

    # TODO: Generator doesn't URL-encode fact_id. Also: spec marks fact_type
    # required but historical contract treats it as optional.
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

    # TODO: Generator doesn't URL-encode fact_id in path.
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

    # TODO: Generator doesn't URL-encode fact_id in path.
    def delete_fact(self, agent_id: str, fact_id: str) -> None:
        """Delete a fact by ID."""
        self._http.delete(
            f"/api/v1/agents/{agent_id}/memory/facts/{quote(fact_id, safe='')}"
        )

    # TODO: Generator doesn't URL-encode fact_id; also missing fallback for
    # non-dict responses.
    def delete_wisdom_fact(self, agent_id: str, fact_id: str) -> DeleteWisdomResponse:
        """Delete a wisdom fact by ID."""
        data = self._http.delete(
            f"/api/v1/agents/{agent_id}/memory/wisdom/{quote(fact_id, safe='')}"
        )
        if isinstance(data, dict):
            return DeleteWisdomResponse.model_validate(data)
        return DeleteWisdomResponse(success=True, fact_id=fact_id)


class AsyncMemory(_GenAsyncMemory):
    """Async mirror of Memory — thin convenience layer over generated AsyncMemory.

    Overrides mirror the sync Memory class above. See comments there for reasons.
    """

    # TODO(B.2/Bug8): seed() absent from generated class; spec gap.
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

    # TODO(B.2/Bug6): missing `offset`, limit typed str vs int, different return class.
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

    # TODO: Different return type + fallback for non-dict responses.
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

    # TODO: URL-encoding of fact_id; fact_type treated as optional.
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

    # TODO: URL-encoding of fact_id.
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

    # TODO: URL-encoding of fact_id.
    async def delete_fact(self, agent_id: str, fact_id: str) -> None:
        """Delete a fact by ID."""
        await self._http.delete(
            f"/api/v1/agents/{agent_id}/memory/facts/{quote(fact_id, safe='')}"
        )

    # TODO: URL-encoding + fallback for non-dict responses.
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
