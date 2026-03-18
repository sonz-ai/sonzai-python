"""Instance resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import AgentInstance, InstanceListResponse, SessionResponse


class Instances:
    """Sync instance operations for an agent."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self, agent_id: str) -> InstanceListResponse:
        """List all instances for an agent."""
        data = self._http.get(f"/api/v1/agents/{agent_id}/instances")
        return InstanceListResponse.model_validate(data)

    def create(
        self,
        agent_id: str,
        *,
        name: str,
        description: str | None = None,
    ) -> AgentInstance:
        """Create a new agent instance."""
        body: dict[str, Any] = {"name": name}
        if description:
            body["description"] = description

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/instances", json_data=body
        )
        return AgentInstance.model_validate(data)

    def get(self, agent_id: str, instance_id: str) -> AgentInstance:
        """Get a specific instance."""
        data = self._http.get(
            f"/api/v1/agents/{agent_id}/instances/{instance_id}"
        )
        return AgentInstance.model_validate(data)

    def delete(self, agent_id: str, instance_id: str) -> SessionResponse:
        """Delete an instance."""
        data = self._http.delete(
            f"/api/v1/agents/{agent_id}/instances/{instance_id}"
        )
        return SessionResponse.model_validate(data)

    def reset(self, agent_id: str, instance_id: str) -> AgentInstance:
        """Reset an instance (clears all context data)."""
        data = self._http.post(
            f"/api/v1/agents/{agent_id}/instances/{instance_id}/reset"
        )
        return AgentInstance.model_validate(data)

    def update(
        self,
        agent_id: str,
        instance_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        status: str | None = None,
    ) -> AgentInstance:
        """Update an agent instance."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if status is not None:
            body["status"] = status
        data = self._http.patch(
            f"/api/v1/agents/{agent_id}/instances/{instance_id}", json_data=body
        )
        return AgentInstance.model_validate(data)


class AsyncInstances:
    """Async instance operations for an agent."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self, agent_id: str) -> InstanceListResponse:
        data = await self._http.get(f"/api/v1/agents/{agent_id}/instances")
        return InstanceListResponse.model_validate(data)

    async def create(
        self,
        agent_id: str,
        *,
        name: str,
        description: str | None = None,
    ) -> AgentInstance:
        body: dict[str, Any] = {"name": name}
        if description:
            body["description"] = description

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/instances", json_data=body
        )
        return AgentInstance.model_validate(data)

    async def get(self, agent_id: str, instance_id: str) -> AgentInstance:
        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/instances/{instance_id}"
        )
        return AgentInstance.model_validate(data)

    async def delete(self, agent_id: str, instance_id: str) -> SessionResponse:
        data = await self._http.delete(
            f"/api/v1/agents/{agent_id}/instances/{instance_id}"
        )
        return SessionResponse.model_validate(data)

    async def reset(self, agent_id: str, instance_id: str) -> AgentInstance:
        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/instances/{instance_id}/reset"
        )
        return AgentInstance.model_validate(data)

    async def update(
        self,
        agent_id: str,
        instance_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        status: str | None = None,
    ) -> AgentInstance:
        """Update an agent instance."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if status is not None:
            body["status"] = status
        data = await self._http.patch(
            f"/api/v1/agents/{agent_id}/instances/{instance_id}", json_data=body
        )
        return AgentInstance.model_validate(data)
