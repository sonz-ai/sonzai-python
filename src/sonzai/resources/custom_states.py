"""Custom states resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import CustomState, CustomStateListResponse, DeleteResponse


class CustomStates:
    """Sync custom state operations for an agent."""

    def __init__(self, http: HTTPClient) -> None:
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
        body: dict[str, Any] = {"key": key, "value": value}
        if scope is not None:
            body["scope"] = scope
        if content_type is not None:
            body["content_type"] = content_type
        if user_id is not None:
            body["user_id"] = user_id
        if instance_id is not None:
            body["instance_id"] = instance_id

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
        body: dict[str, Any] = {"value": value}
        if content_type is not None:
            body["content_type"] = content_type

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


class AsyncCustomStates:
    """Async custom state operations for an agent."""

    def __init__(self, http: AsyncHTTPClient) -> None:
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
        body: dict[str, Any] = {"key": key, "value": value}
        if scope is not None:
            body["scope"] = scope
        if content_type is not None:
            body["content_type"] = content_type
        if user_id is not None:
            body["user_id"] = user_id
        if instance_id is not None:
            body["instance_id"] = instance_id

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
        body: dict[str, Any] = {"value": value}
        if content_type is not None:
            body["content_type"] = content_type

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
