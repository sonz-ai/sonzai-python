"""Custom agents resource for the Sonzai SDK.

Custom agents are tenant-scoped, declaratively-configured agents (model,
system prompt, tool set, structured findings schema) backed by the CRUD
``/api/v1/custom-agents`` endpoints.
"""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import CustomAgent, CustomAgentListResponse

# Module-level alias for ``list[str]``. The resource classes define a ``list``
# method, which shadows the ``list`` builtin for any parameter annotation
# declared after it at class scope — using this alias keeps ``tools``
# annotations resolving to the builtin regardless of method ordering.
_StrList = list[str]


def _build_body(
    *,
    slug: str,
    name: str,
    model: str,
    system: str,
    description: str | None,
    findings_schema: dict[str, Any] | None,
    tools: _StrList | None,
    disable_tools: bool | None,
    max_tool_rounds: int | None,
) -> dict[str, Any]:
    """Build a create/update write body, omitting None-valued optional fields."""
    body: dict[str, Any] = {
        "slug": slug,
        "name": name,
        "model": model,
        "system": system,
    }
    if description is not None:
        body["description"] = description
    if findings_schema is not None:
        body["findings_schema"] = findings_schema
    if tools is not None:
        body["tools"] = tools
    if disable_tools is not None:
        body["disable_tools"] = disable_tools
    if max_tool_rounds is not None:
        body["max_tool_rounds"] = max_tool_rounds
    return body


class CustomAgents:
    """Sync custom-agent management operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self) -> CustomAgentListResponse:
        """List all custom agents for the tenant."""
        data = self._http.get("/api/v1/custom-agents")
        return CustomAgentListResponse.model_validate(data)

    def create(
        self,
        *,
        slug: str,
        name: str,
        model: str,
        system: str,
        description: str | None = None,
        findings_schema: dict[str, Any] | None = None,
        tools: _StrList | None = None,
        disable_tools: bool | None = None,
        max_tool_rounds: int | None = None,
    ) -> CustomAgent:
        """Create a custom agent."""
        body = _build_body(
            slug=slug,
            name=name,
            model=model,
            system=system,
            description=description,
            findings_schema=findings_schema,
            tools=tools,
            disable_tools=disable_tools,
            max_tool_rounds=max_tool_rounds,
        )
        data = self._http.post("/api/v1/custom-agents", json_data=body)
        return CustomAgent.model_validate(data)

    def get(self, agent_id: str) -> CustomAgent:
        """Fetch a single custom agent by ID."""
        data = self._http.get(f"/api/v1/custom-agents/{agent_id}")
        return CustomAgent.model_validate(data)

    def update(
        self,
        agent_id: str,
        *,
        slug: str,
        name: str,
        model: str,
        system: str,
        description: str | None = None,
        findings_schema: dict[str, Any] | None = None,
        tools: _StrList | None = None,
        disable_tools: bool | None = None,
        max_tool_rounds: int | None = None,
    ) -> CustomAgent:
        """Update a custom agent."""
        body = _build_body(
            slug=slug,
            name=name,
            model=model,
            system=system,
            description=description,
            findings_schema=findings_schema,
            tools=tools,
            disable_tools=disable_tools,
            max_tool_rounds=max_tool_rounds,
        )
        data = self._http.put(f"/api/v1/custom-agents/{agent_id}", json_data=body)
        return CustomAgent.model_validate(data)

    def delete(self, agent_id: str) -> None:
        """Delete a custom agent."""
        self._http.delete(f"/api/v1/custom-agents/{agent_id}")


class AsyncCustomAgents:
    """Async custom-agent management operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self) -> CustomAgentListResponse:
        """List all custom agents for the tenant."""
        data = await self._http.get("/api/v1/custom-agents")
        return CustomAgentListResponse.model_validate(data)

    async def create(
        self,
        *,
        slug: str,
        name: str,
        model: str,
        system: str,
        description: str | None = None,
        findings_schema: dict[str, Any] | None = None,
        tools: _StrList | None = None,
        disable_tools: bool | None = None,
        max_tool_rounds: int | None = None,
    ) -> CustomAgent:
        """Create a custom agent."""
        body = _build_body(
            slug=slug,
            name=name,
            model=model,
            system=system,
            description=description,
            findings_schema=findings_schema,
            tools=tools,
            disable_tools=disable_tools,
            max_tool_rounds=max_tool_rounds,
        )
        data = await self._http.post("/api/v1/custom-agents", json_data=body)
        return CustomAgent.model_validate(data)

    async def get(self, agent_id: str) -> CustomAgent:
        """Fetch a single custom agent by ID."""
        data = await self._http.get(f"/api/v1/custom-agents/{agent_id}")
        return CustomAgent.model_validate(data)

    async def update(
        self,
        agent_id: str,
        *,
        slug: str,
        name: str,
        model: str,
        system: str,
        description: str | None = None,
        findings_schema: dict[str, Any] | None = None,
        tools: _StrList | None = None,
        disable_tools: bool | None = None,
        max_tool_rounds: int | None = None,
    ) -> CustomAgent:
        """Update a custom agent."""
        body = _build_body(
            slug=slug,
            name=name,
            model=model,
            system=system,
            description=description,
            findings_schema=findings_schema,
            tools=tools,
            disable_tools=disable_tools,
            max_tool_rounds=max_tool_rounds,
        )
        data = await self._http.put(
            f"/api/v1/custom-agents/{agent_id}", json_data=body
        )
        return CustomAgent.model_validate(data)

    async def delete(self, agent_id: str) -> None:
        """Delete a custom agent."""
        await self._http.delete(f"/api/v1/custom-agents/{agent_id}")
