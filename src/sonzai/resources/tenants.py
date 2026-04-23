"""Tenants resource.

Wraps ``/tenants/...`` read endpoints. Tenant-global KB mutations
(``create_org_node``, ``promote_node_to_org``) live on
:class:`sonzai.resources.knowledge.Knowledge` because the SDK has always
grouped KB work by project — this class only covers the tenant-index /
list-nodes reads.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .._generated.resources.tenants import AsyncTenants as _GenAsyncTenants
from .._generated.resources.tenants import Tenants as _GenTenants
from .._http import AsyncHTTPClient, HTTPClient


class Tenants(_GenTenants):
    """Sync tenant read operations."""

    def __init__(self, http: HTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    def list(self) -> dict[str, Any]:
        """List tenants the caller has access to."""
        return self._http.get("/api/v1/tenants")  # type: ignore[no-any-return]

    def get(self, tenant_id: str) -> dict[str, Any]:
        """Get a tenant by ID."""
        return self._http.get(  # type: ignore[no-any-return]
            f"/api/v1/tenants/{quote(tenant_id, safe='')}"
        )

    def list_org_knowledge_nodes(
        self,
        tenant_id: str,
        *,
        node_type: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """List nodes in the organization-global KB scope for a tenant."""
        params: dict[str, Any] = {}
        if node_type is not None:
            params["node_type"] = node_type
        if limit is not None:
            params["limit"] = limit
        return self._http.get(  # type: ignore[no-any-return]
            f"/api/v1/tenants/{quote(tenant_id, safe='')}/knowledge/org-nodes",
            params=params or None,
        )


class AsyncTenants(_GenAsyncTenants):
    """Async tenant read operations (mirror of :class:`Tenants`)."""

    def __init__(self, http: AsyncHTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    async def list(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/tenants")  # type: ignore[no-any-return]

    async def get(self, tenant_id: str) -> dict[str, Any]:
        return await self._http.get(  # type: ignore[no-any-return]
            f"/api/v1/tenants/{quote(tenant_id, safe='')}"
        )

    async def list_org_knowledge_nodes(
        self,
        tenant_id: str,
        *,
        node_type: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if node_type is not None:
            params["node_type"] = node_type
        if limit is not None:
            params["limit"] = limit
        return await self._http.get(  # type: ignore[no-any-return]
            f"/api/v1/tenants/{quote(tenant_id, safe='')}/knowledge/org-nodes",
            params=params or None,
        )
