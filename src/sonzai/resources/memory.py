"""Memory resource — thin convenience layer over the generated class.

Any method defined in the spec is inherited from the generated parent
class unless an override is necessary. Overrides remain for:

  - seed(): Not in spec (spec gap, Bug 8 deferred).
  - list_facts(): Generated is missing `offset` param; spec types limit as
    string but historical contract uses int. Also returns ListFactsResponse
    (generated) vs FactListResponse (historical).
  - create_fact(): Spec marks fact_type required; historical contract treats
    it as optional.

B.2 fixes resolved (overrides removed):
  - list(): generator now produces correct method_name, path, and type.
  - search(): generator now uses `query` kwarg (QUERY_PARAM_OVERRIDES), correct
    path and HTTP method.
  - timeline(): generator now uses `timeline` method_name, correct path.
  - get_fact_history(): generator now produces correct path.
  - get_wisdom_audit(): generator now produces correct path.
  - __init__: base class _MemoryBase accepts Any, no override needed.

B.5 fixes resolved (overrides removed):
  - reset(): generator now returns MemoryResetResponse (RESPONSE_CLASS_OVERRIDES),
    URL-quotes agent_id (Fix 1), and handles DELETE empty-body (Fix 3).
  - update_fact(): generator now URL-quotes fact_id (Fix 1).
  - delete_fact(): generator now URL-quotes fact_id (Fix 1).
  - delete_wisdom_fact(): generator now URL-quotes fact_id (Fix 1) and handles
    DELETE empty-body with sonzai.types.DeleteWisdomResponse (Fix 3 +
    EXTERNAL_CLASS_IMPORTS).
"""

from __future__ import annotations

import builtins
from typing import Any

_list = builtins.list

from .._generated.resources.memory import AsyncMemory as _GenAsyncMemory
from .._generated.resources.memory import Memory as _GenMemory
from .._request_helpers import encode_body
from .._generated.models import (
    AtomicFact,
    CreateFactInputBody,
)
from ..types import (
    FactListResponse,
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

    # TODO: Spec marks fact_type required but historical contract treats it as
    # optional. Also: generated adds instance_id as a query param (not in
    # historical contract).
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

    # TODO: fact_type optional vs required; no instance_id in historical contract.
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
