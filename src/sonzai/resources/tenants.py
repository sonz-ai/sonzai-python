"""Tenants resource for the Sonzai SDK."""

from __future__ import annotations

from pydantic import TypeAdapter

from .._http import AsyncHTTPClient, HTTPClient
from ..types import Tenant, TenantList


class Tenants:
    """Sync tenant listing (platform-admin scope)."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self) -> TenantList:
        """List all tenants the caller can see."""
        data = self._http.get("/api/v1/tenants")
        if isinstance(data, list):
            tenants = TypeAdapter(list[Tenant]).validate_python(data)
            return TenantList(tenants=tenants)
        return TenantList.model_validate(data if isinstance(data, dict) else {"tenants": data or []})

    def get(self, tenant_id: str) -> Tenant:
        """Get a tenant by ID."""
        data = self._http.get(f"/api/v1/tenants/{tenant_id}")
        return Tenant.model_validate(data)


class AsyncTenants:
    """Async tenant listing (platform-admin scope)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self) -> TenantList:
        """List all tenants the caller can see."""
        data = await self._http.get("/api/v1/tenants")
        if isinstance(data, list):
            tenants = TypeAdapter(list[Tenant]).validate_python(data)
            return TenantList(tenants=tenants)
        return TenantList.model_validate(data if isinstance(data, dict) else {"tenants": data or []})

    async def get(self, tenant_id: str) -> Tenant:
        """Get a tenant by ID."""
        data = await self._http.get(f"/api/v1/tenants/{tenant_id}")
        return Tenant.model_validate(data)
