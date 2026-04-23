"""Custom states resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._generated.models import (
    CreateCustomStateInputBody,
    UpdateCustomStateInputBody,
    UpsertCustomStateByKeyInputBody,
)
from .._generated.resources.custom_states import AsyncCustomStates as _GenAsyncCustomStates
from .._generated.resources.custom_states import CustomStates as _GenCustomStates
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body
from ..types import CustomState, CustomStateListResponse, DeleteResponse


class CustomStates(_GenCustomStates):
    """Sync custom state operations for an agent."""

    def __init__(self, http: HTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    def list(
        self,
        agent_id: str,
        *,
        scope: str | None = None,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> CustomStateListResponse:
        """List custom states for an agent."""
        params: dict[str, Any] = {}
        if scope is not None:
            params["scope"] = scope
        if user_id is not None:
            params["user_id"] = user_id
        if instance_id is not None:
            params["instance_id"] = instance_id

        data = self._http.get(
            f"/api/v1/agents/{agent_id}/custom-states", params=params
        )
        return CustomStateListResponse.model_validate(data)

    def create(
        self,
        agent_id: str,
        *,
        key: str,
        value: Any,
        scope: str | None = None,
        content_type: str | None = None,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> CustomState:
        """Create a new custom state."""
        raw: dict[str, Any] = {"key": key, "value": value}
        if scope is not None:
            raw["scope"] = scope
        if content_type is not None:
            raw["content_type"] = content_type
        if user_id is not None:
            raw["user_id"] = user_id
        if instance_id is not None:
            raw["instance_id"] = instance_id
        body = encode_body(CreateCustomStateInputBody, raw)

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/custom-states", json_data=body
        )
        return CustomState.model_validate(data)

    def update(
        self,
        agent_id: str,
        state_id: str,
        *,
        value: Any,
        content_type: str | None = None,
    ) -> CustomState:
        """Update a custom state."""
        raw: dict[str, Any] = {"value": value}
        if content_type is not None:
            raw["content_type"] = content_type
        body = encode_body(UpdateCustomStateInputBody, raw)

        data = self._http.put(
            f"/api/v1/agents/{agent_id}/custom-states/{state_id}",
            json_data=body,
        )
        return CustomState.model_validate(data)

    def delete(self, agent_id: str, state_id: str) -> DeleteResponse:
        """Delete a custom state."""
        data = self._http.delete(
            f"/api/v1/agents/{agent_id}/custom-states/{state_id}"
        )
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)

    def upsert(
        self,
        agent_id: str,
        *,
        key: str,
        value: Any,
        scope: str | None = None,
        content_type: str | None = None,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> CustomState:
        """Create or update a custom state by composite key (key + scope + user_id + instance_id)."""
        raw: dict[str, Any] = {"key": key, "value": value}
        if scope is not None:
            raw["scope"] = scope
        if content_type is not None:
            raw["content_type"] = content_type
        if user_id is not None:
            raw["user_id"] = user_id
        if instance_id is not None:
            raw["instance_id"] = instance_id
        body = encode_body(UpsertCustomStateByKeyInputBody, raw)

        data = self._http.put(
            f"/api/v1/agents/{agent_id}/custom-states/by-key", json_data=body
        )
        return CustomState.model_validate(data)

    def get_by_key(
        self,
        agent_id: str,
        *,
        key: str,
        scope: str | None = None,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> CustomState:
        """Get a custom state by its composite key."""
        params: dict[str, Any] = {"key": key}
        if scope is not None:
            params["scope"] = scope
        if user_id is not None:
            params["user_id"] = user_id
        if instance_id is not None:
            params["instance_id"] = instance_id

        data = self._http.get(
            f"/api/v1/agents/{agent_id}/custom-states/by-key", params=params
        )
        return CustomState.model_validate(data)

    def delete_by_key(
        self,
        agent_id: str,
        *,
        key: str,
        scope: str | None = None,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> DeleteResponse:
        """Delete a custom state by its composite key."""
        params: dict[str, Any] = {"key": key}
        if scope is not None:
            params["scope"] = scope
        if user_id is not None:
            params["user_id"] = user_id
        if instance_id is not None:
            params["instance_id"] = instance_id

        data = self._http.delete(
            f"/api/v1/agents/{agent_id}/custom-states/by-key", params=params
        )
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)


class AsyncCustomStates(_GenAsyncCustomStates):
    """Async custom state operations for an agent."""

    def __init__(self, http: AsyncHTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    async def list(
        self,
        agent_id: str,
        *,
        scope: str | None = None,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> CustomStateListResponse:
        """List custom states for an agent."""
        params: dict[str, Any] = {}
        if scope is not None:
            params["scope"] = scope
        if user_id is not None:
            params["user_id"] = user_id
        if instance_id is not None:
            params["instance_id"] = instance_id

        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/custom-states", params=params
        )
        return CustomStateListResponse.model_validate(data)

    async def create(
        self,
        agent_id: str,
        *,
        key: str,
        value: Any,
        scope: str | None = None,
        content_type: str | None = None,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> CustomState:
        """Create a new custom state."""
        raw: dict[str, Any] = {"key": key, "value": value}
        if scope is not None:
            raw["scope"] = scope
        if content_type is not None:
            raw["content_type"] = content_type
        if user_id is not None:
            raw["user_id"] = user_id
        if instance_id is not None:
            raw["instance_id"] = instance_id
        body = encode_body(CreateCustomStateInputBody, raw)

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/custom-states", json_data=body
        )
        return CustomState.model_validate(data)

    async def update(
        self,
        agent_id: str,
        state_id: str,
        *,
        value: Any,
        content_type: str | None = None,
    ) -> CustomState:
        """Update a custom state."""
        raw: dict[str, Any] = {"value": value}
        if content_type is not None:
            raw["content_type"] = content_type
        body = encode_body(UpdateCustomStateInputBody, raw)

        data = await self._http.put(
            f"/api/v1/agents/{agent_id}/custom-states/{state_id}",
            json_data=body,
        )
        return CustomState.model_validate(data)

    async def delete(self, agent_id: str, state_id: str) -> DeleteResponse:
        """Delete a custom state."""
        data = await self._http.delete(
            f"/api/v1/agents/{agent_id}/custom-states/{state_id}"
        )
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)

    async def upsert(
        self,
        agent_id: str,
        *,
        key: str,
        value: Any,
        scope: str | None = None,
        content_type: str | None = None,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> CustomState:
        """Create or update a custom state by composite key (key + scope + user_id + instance_id)."""
        raw: dict[str, Any] = {"key": key, "value": value}
        if scope is not None:
            raw["scope"] = scope
        if content_type is not None:
            raw["content_type"] = content_type
        if user_id is not None:
            raw["user_id"] = user_id
        if instance_id is not None:
            raw["instance_id"] = instance_id
        body = encode_body(UpsertCustomStateByKeyInputBody, raw)

        data = await self._http.put(
            f"/api/v1/agents/{agent_id}/custom-states/by-key", json_data=body
        )
        return CustomState.model_validate(data)

    async def get_by_key(
        self,
        agent_id: str,
        *,
        key: str,
        scope: str | None = None,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> CustomState:
        """Get a custom state by its composite key."""
        params: dict[str, Any] = {"key": key}
        if scope is not None:
            params["scope"] = scope
        if user_id is not None:
            params["user_id"] = user_id
        if instance_id is not None:
            params["instance_id"] = instance_id

        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/custom-states/by-key", params=params
        )
        return CustomState.model_validate(data)

    async def delete_by_key(
        self,
        agent_id: str,
        *,
        key: str,
        scope: str | None = None,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> DeleteResponse:
        """Delete a custom state by its composite key."""
        params: dict[str, Any] = {"key": key}
        if scope is not None:
            params["scope"] = scope
        if user_id is not None:
            params["user_id"] = user_id
        if instance_id is not None:
            params["instance_id"] = instance_id

        data = await self._http.delete(
            f"/api/v1/agents/{agent_id}/custom-states/by-key", params=params
        )
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)
