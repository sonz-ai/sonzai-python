"""MCP Catalog resource for the Sonzai SDK.

The MCP Catalog is a per-project registry of MCP (Model Context Protocol)
server endpoints. Each entry pairs a remote MCP URL with auth config; agents
opt into specific entries via the ``mcpEnabled`` capability (a list of catalog
IDs). At chat time, the platform discovers each entry's tools and registers
them as agent-callable tools for the turn.

Org-admin only on writes (create / update / delete); reads are open within the
project.

The generated ``Mcp`` / ``AsyncMcp`` base classes expose the raw, codegen-named
methods (``list_mcp_catalog``, ``create_mcp_catalog_entry``, …). This
hand-written subclass adds the clean public surface that matches the Go SDK's
``client.MCPCatalog`` (``List`` / ``Get`` / ``Create`` / ``Update`` /
``Delete`` / ``ProbeConfig`` / ``Probe`` / ``ListTools`` / ``ListUsages``) and
the TS SDK's ``client.mcpCatalog`` (``list`` / ``get`` / ``create`` /
``update`` / ``delete`` / ``probeConfig`` / ``probe`` / ``listTools`` /
``listUsages``). Endpoints live under
``/api/v1/projects/{project_id}/mcp/catalog*``.
"""

from __future__ import annotations

from typing import Any

from .._generated.models import (
    ListMCPCatalogOutputBody,
    MCPCatalogCreateBody,
    MCPCatalogEntry,
    MCPCatalogToolsResponse,
    MCPCatalogUpdateBody,
    MCPCatalogUsagesResponse,
    MCPProbeResponseBody,
)
from .._generated.resources.mcp import AsyncMcp as _GenAsyncMcp
from .._generated.resources.mcp import Mcp as _GenMcp
from .._http import AsyncHTTPClient, HTTPClient


def _create_body(
    auth: dict[str, Any],
    name: str,
    transport: str,
    url: str,
    description: str | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "auth": auth,
        "name": name,
        "transport": transport,
        "url": url,
    }
    if description is not None:
        body["description"] = description
    # mode="json" so AnyUrl (the spec types `url`) serialises to a plain
    # string the JSON HTTP layer can encode; by_alias + exclude_none match the
    # encode_body convention used everywhere else.
    return MCPCatalogCreateBody.model_validate(body).model_dump(
        by_alias=True, exclude_none=True, mode="json"
    )


def _update_body(
    auth: dict[str, Any] | None,
    name: str | None,
    transport: str | None,
    url: str | None,
    description: str | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if auth is not None:
        body["auth"] = auth
    if name is not None:
        body["name"] = name
    if transport is not None:
        body["transport"] = transport
    if url is not None:
        body["url"] = url
    if description is not None:
        body["description"] = description
    return MCPCatalogUpdateBody.model_validate(body).model_dump(
        by_alias=True, exclude_none=True, mode="json"
    )


class MCPCatalog(_GenMcp):
    """Sync operations on the per-project MCP catalog.

    Clean aliases over the generated ``Mcp`` base; the raw codegen-named
    methods (``list_mcp_catalog`` etc.) remain available via inheritance.

    Example::

        catalog = client.mcp_catalog.list("proj-1")
        for entry in catalog.entries or []:
            print(entry.name, entry.url, entry.health.status)

        entry = client.mcp_catalog.create(
            "proj-1",
            name="Weather",
            url="https://mcp.example.com/weather",
            transport="streamable-http",
            auth={"kind": "bearer", "bearer_token": "sk-..."},
        )
        client.mcp_catalog.probe("proj-1", entry.id)
    """

    # TODO(B.3-followup): __init__ takes HTTPClient (typed); generated _McpBase
    # takes Any. Override kept to preserve the typed constructor signature.
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self, project_id: str) -> ListMCPCatalogOutputBody:
        """List every catalog entry registered for the project."""
        return self.list_mcp_catalog(project_id)

    def get(self, project_id: str, id: str) -> MCPCatalogEntry:
        """Get a single catalog entry by ID."""
        return self.get_mcp_catalog_entry(project_id, id)

    def create(
        self,
        project_id: str,
        *,
        name: str,
        url: str,
        transport: str,
        auth: dict[str, Any],
        description: str | None = None,
    ) -> MCPCatalogEntry:
        """Register a new MCP server with the project's catalog. Org-admin only."""
        path = f"/api/v1/projects/{project_id}/mcp/catalog"
        body = _create_body(auth, name, transport, url, description)
        data = self._http.post(path, json_data=body)
        return MCPCatalogEntry.model_validate(data)

    def update(
        self,
        project_id: str,
        id: str,
        *,
        name: str | None = None,
        url: str | None = None,
        transport: str | None = None,
        auth: dict[str, Any] | None = None,
        description: str | None = None,
    ) -> MCPCatalogEntry:
        """Patch an existing catalog entry. Org-admin only.

        Auth is updated atomically — pass a fresh ``auth`` object to rotate
        credentials.
        """
        path = f"/api/v1/projects/{project_id}/mcp/catalog/{id}"
        body = _update_body(auth, name, transport, url, description)
        data = self._http.patch(path, json_data=body)
        return MCPCatalogEntry.model_validate(data)

    def delete(self, project_id: str, id: str, *, force: bool | None = None) -> Any:
        """Delete a catalog entry. Org-admin only."""
        return self.delete_mcp_catalog_entry(project_id, id, force=force)

    def probe_config(
        self,
        project_id: str,
        *,
        name: str,
        url: str,
        transport: str,
        auth: dict[str, Any],
        description: str | None = None,
    ) -> MCPProbeResponseBody:
        """Probe an MCP config without persisting it (pre-create "Test connection").

        The response includes latency, tool count, and any auth/transport error
        the platform observed.
        """
        path = f"/api/v1/projects/{project_id}/mcp/catalog/probe"
        body = _create_body(auth, name, transport, url, description)
        data = self._http.post(path, json_data=body)
        return MCPProbeResponseBody.model_validate(data)

    def probe(self, project_id: str, id: str) -> MCPProbeResponseBody:
        """Re-contact an existing entry's MCP server and refresh its tool list + health."""
        return self.probe_mcp_catalog_entry(project_id, id)

    def list_tools(self, project_id: str, id: str) -> MCPCatalogToolsResponse:
        """List the tools advertised by this entry's MCP server (last probed)."""
        return self.list_mcp_catalog_tools(project_id, id)

    def list_usages(self, project_id: str, id: str) -> MCPCatalogUsagesResponse:
        """List every agent ID currently opted into this catalog entry."""
        return self.list_mcp_catalog_usages(project_id, id)


class AsyncMCPCatalog(_GenAsyncMcp):
    """Async operations on the per-project MCP catalog.

    Mirror of :class:`MCPCatalog`; see that class for usage examples.
    """

    # TODO(B.3-followup): typed constructor; see MCPCatalog.__init__.
    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self, project_id: str) -> ListMCPCatalogOutputBody:
        """List every catalog entry registered for the project."""
        return await self.list_mcp_catalog(project_id)

    async def get(self, project_id: str, id: str) -> MCPCatalogEntry:
        """Get a single catalog entry by ID."""
        return await self.get_mcp_catalog_entry(project_id, id)

    async def create(
        self,
        project_id: str,
        *,
        name: str,
        url: str,
        transport: str,
        auth: dict[str, Any],
        description: str | None = None,
    ) -> MCPCatalogEntry:
        """Register a new MCP server with the project's catalog. Org-admin only."""
        path = f"/api/v1/projects/{project_id}/mcp/catalog"
        body = _create_body(auth, name, transport, url, description)
        data = await self._http.post(path, json_data=body)
        return MCPCatalogEntry.model_validate(data)

    async def update(
        self,
        project_id: str,
        id: str,
        *,
        name: str | None = None,
        url: str | None = None,
        transport: str | None = None,
        auth: dict[str, Any] | None = None,
        description: str | None = None,
    ) -> MCPCatalogEntry:
        """Patch an existing catalog entry. Org-admin only."""
        path = f"/api/v1/projects/{project_id}/mcp/catalog/{id}"
        body = _update_body(auth, name, transport, url, description)
        data = await self._http.patch(path, json_data=body)
        return MCPCatalogEntry.model_validate(data)

    async def delete(
        self, project_id: str, id: str, *, force: bool | None = None
    ) -> Any:
        """Delete a catalog entry. Org-admin only."""
        return await self.delete_mcp_catalog_entry(project_id, id, force=force)

    async def probe_config(
        self,
        project_id: str,
        *,
        name: str,
        url: str,
        transport: str,
        auth: dict[str, Any],
        description: str | None = None,
    ) -> MCPProbeResponseBody:
        """Probe an MCP config without persisting it (pre-create "Test connection")."""
        path = f"/api/v1/projects/{project_id}/mcp/catalog/probe"
        body = _create_body(auth, name, transport, url, description)
        data = await self._http.post(path, json_data=body)
        return MCPProbeResponseBody.model_validate(data)

    async def probe(self, project_id: str, id: str) -> MCPProbeResponseBody:
        """Re-contact an existing entry's MCP server and refresh its tool list + health."""
        return await self.probe_mcp_catalog_entry(project_id, id)

    async def list_tools(self, project_id: str, id: str) -> MCPCatalogToolsResponse:
        """List the tools advertised by this entry's MCP server (last probed)."""
        return await self.list_mcp_catalog_tools(project_id, id)

    async def list_usages(
        self, project_id: str, id: str
    ) -> MCPCatalogUsagesResponse:
        """List every agent ID currently opted into this catalog entry."""
        return await self.list_mcp_catalog_usages(project_id, id)


__all__ = [
    "MCPCatalog",
    "AsyncMCPCatalog",
]
