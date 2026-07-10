"""Runtime CRM adapter-token resource for the Sonzai SDK."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, cast

from pydantic import BaseModel

from .._http import AsyncHTTPClient, HTTPClient
from .._pagination import AsyncPage, Page
from ..types import CRMEvent, CRMImportItem, CRMImportResult


class Crm:
    """Sync runtime CRM operations available to headless adapter integrations."""

    def __init__(self, http: HTTPClient | None) -> None:
        self._http = http

    def import_contacts(
        self,
        contacts: Sequence[CRMImportItem | Mapping[str, Any]],
        *,
        tenant_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> CRMImportResult:
        """Bulk-upsert CRM contacts by ``external_ref``.

        Targets the deployed app-runtime ``/api/rt/crm/import`` route, not the
        Sonzai platform API. Configure ``runtime_base_url`` on the client and
        authenticate with the runtime adapter token.
        """
        data = self._require_http().post(
            "/api/rt/crm/import",
            json_data={"contacts": [_json_body(item) for item in contacts]},
            headers=_tenant_headers(tenant_id),
            idempotency_key=idempotency_key,
        )
        return CRMImportResult.model_validate(data)

    def events(
        self,
        *,
        cursor: str | None = None,
        limit: int = 100,
        tenant_id: str | None = None,
    ) -> Page[CRMEvent]:
        """Iterate the runtime CRM adapter change feed with cursor pagination."""
        headers = _tenant_headers(tenant_id)
        return Page(
            fetcher=lambda p: self._require_http().get(
                "/api/rt/crm/events", params=p, headers=headers
            ),
            params={"cursor": cursor, "limit": limit},
            item_key="events",
            item_parser=CRMEvent.model_validate,
            mode="cursor",
        )

    def _require_http(self) -> HTTPClient:
        if self._http is None:
            raise ValueError(
                "runtime_base_url must be provided or SONZAI_RUNTIME_BASE_URL must be set "
                "to use client.crm"
            )
        return self._http


class AsyncCrm:
    """Async runtime CRM operations available to headless adapter integrations."""

    def __init__(self, http: AsyncHTTPClient | None) -> None:
        self._http = http

    async def import_contacts(
        self,
        contacts: Sequence[CRMImportItem | Mapping[str, Any]],
        *,
        tenant_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> CRMImportResult:
        """Bulk-upsert CRM contacts by ``external_ref``."""
        data = await self._require_http().post(
            "/api/rt/crm/import",
            json_data={"contacts": [_json_body(item) for item in contacts]},
            headers=_tenant_headers(tenant_id),
            idempotency_key=idempotency_key,
        )
        return CRMImportResult.model_validate(data)

    async def events(
        self,
        *,
        cursor: str | None = None,
        limit: int = 100,
        tenant_id: str | None = None,
    ) -> AsyncPage[CRMEvent]:
        """Iterate the runtime CRM adapter change feed with cursor pagination."""
        headers = _tenant_headers(tenant_id)

        async def fetcher(p: dict[str, Any]) -> dict[str, Any]:
            return cast(
                dict[str, Any],
                await self._require_http().get("/api/rt/crm/events", params=p, headers=headers),
            )

        return AsyncPage(
            fetcher=fetcher,
            params={"cursor": cursor, "limit": limit},
            item_key="events",
            item_parser=CRMEvent.model_validate,
            mode="cursor",
        )

    def _require_http(self) -> AsyncHTTPClient:
        if self._http is None:
            raise ValueError(
                "runtime_base_url must be provided or SONZAI_RUNTIME_BASE_URL must be set "
                "to use client.crm"
            )
        return self._http


def _tenant_headers(tenant_id: str | None) -> dict[str, str] | None:
    if tenant_id is None:
        return None
    return {"X-Sonzai-Tenant-ID": tenant_id}


def _json_body(item: CRMImportItem | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(item, BaseModel):
        return item.model_dump(mode="json", exclude_none=True)
    return {key: value for key, value in item.items() if value is not None}
