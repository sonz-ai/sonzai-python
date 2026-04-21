"""Organization / billing resource.

Wraps all endpoints under ``/org/...`` plus the tenant-facing ``/me``.
These are platform-management endpoints — billing, contracts, ledgers,
vouchers, model pricing. The hand-written SDK historically omitted them
because most SDK users don't need them, but the regeneration audit
flagged them as spec-declared and unbound, so we expose them as typed
dict-returning helpers for completeness.

Response shapes vary by endpoint and the OpenAPI schemas are mostly
free-form objects, so these helpers return raw ``dict[str, Any]``.
Callers who need stronger typing can grab the generated models from
``sonzai._generated.models`` and call ``.from_dict()`` themselves.
"""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient


class _OrgBase:
    def __init__(self, http: Any) -> None:
        self._http = http


class Org(_OrgBase):
    """Sync organization/billing operations."""

    def __init__(self, http: HTTPClient) -> None:
        super().__init__(http)

    # -- Current user context --------------------------------------------------

    def me(self) -> dict[str, Any]:
        """Get the current user + their organizations (``GET /me``)."""
        return self._http.get("/api/v1/me")  # type: ignore[no-any-return]

    # -- Billing / ledger ------------------------------------------------------

    def get_billing(self) -> dict[str, Any]:
        """Get the org billing profile."""
        return self._http.get("/api/v1/org/billing")  # type: ignore[no-any-return]

    def create_billing_checkout(self, **body: Any) -> dict[str, Any]:
        """Create a Stripe checkout session for credit top-up."""
        return self._http.post("/api/v1/org/billing/checkout", json_data=body)  # type: ignore[no-any-return]

    def create_billing_portal(self, **body: Any) -> dict[str, Any]:
        """Create a Stripe billing-portal session."""
        return self._http.post("/api/v1/org/billing/portal", json_data=body)  # type: ignore[no-any-return]

    def get_ledger(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """Get the org billing ledger."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        return self._http.get("/api/v1/org/ledger", params=params or None)  # type: ignore[no-any-return]

    # -- Contracts / service agreements ---------------------------------------

    def get_contract(self) -> dict[str, Any]:
        """Get the org's current enterprise contract."""
        return self._http.get("/api/v1/org/contract")  # type: ignore[no-any-return]

    def subscribe_contract(self, **body: Any) -> dict[str, Any]:
        """Subscribe the tenant to an enterprise contract."""
        return self._http.post("/api/v1/org/contract/subscribe", json_data=body)  # type: ignore[no-any-return]

    def list_service_agreements(self) -> dict[str, Any]:
        """List active service agreements."""
        return self._http.get("/api/v1/org/service-agreements")  # type: ignore[no-any-return]

    def get_service_usage(self) -> dict[str, Any]:
        """Get the org's service usage."""
        return self._http.get("/api/v1/org/service-usage")  # type: ignore[no-any-return]

    def get_usage_summary(self) -> dict[str, Any]:
        """Get the org's usage summary."""
        return self._http.get("/api/v1/org/usage-summary")  # type: ignore[no-any-return]

    # -- Misc ------------------------------------------------------------------

    def get_model_pricing(self) -> dict[str, Any]:
        """Get active model pricing for the tenant."""
        return self._http.get("/api/v1/org/model-pricing")  # type: ignore[no-any-return]

    def list_active_characters(self) -> dict[str, Any]:
        """List active characters for billing purposes."""
        return self._http.get("/api/v1/org/characters")  # type: ignore[no-any-return]

    def get_context_engine_events(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """Context engine event usage (aggregated)."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        return self._http.get("/api/v1/org/events", params=params or None)  # type: ignore[no-any-return]

    def redeem_voucher(self, *, code: str, **extra: Any) -> dict[str, Any]:
        """Redeem a voucher code."""
        body: dict[str, Any] = {"code": code, **extra}
        return self._http.post("/api/v1/org/vouchers/redeem", json_data=body)  # type: ignore[no-any-return]


class AsyncOrg(_OrgBase):
    """Async organization/billing operations (mirror of :class:`Org`)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        super().__init__(http)

    async def me(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/me")  # type: ignore[no-any-return]

    async def get_billing(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/org/billing")  # type: ignore[no-any-return]

    async def create_billing_checkout(self, **body: Any) -> dict[str, Any]:
        return await self._http.post("/api/v1/org/billing/checkout", json_data=body)  # type: ignore[no-any-return]

    async def create_billing_portal(self, **body: Any) -> dict[str, Any]:
        return await self._http.post("/api/v1/org/billing/portal", json_data=body)  # type: ignore[no-any-return]

    async def get_ledger(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        return await self._http.get("/api/v1/org/ledger", params=params or None)  # type: ignore[no-any-return]

    async def get_contract(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/org/contract")  # type: ignore[no-any-return]

    async def subscribe_contract(self, **body: Any) -> dict[str, Any]:
        return await self._http.post("/api/v1/org/contract/subscribe", json_data=body)  # type: ignore[no-any-return]

    async def list_service_agreements(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/org/service-agreements")  # type: ignore[no-any-return]

    async def get_service_usage(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/org/service-usage")  # type: ignore[no-any-return]

    async def get_usage_summary(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/org/usage-summary")  # type: ignore[no-any-return]

    async def get_model_pricing(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/org/model-pricing")  # type: ignore[no-any-return]

    async def list_active_characters(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/org/characters")  # type: ignore[no-any-return]

    async def get_context_engine_events(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        return await self._http.get("/api/v1/org/events", params=params or None)  # type: ignore[no-any-return]

    async def redeem_voucher(self, *, code: str, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"code": code, **extra}
        return await self._http.post("/api/v1/org/vouchers/redeem", json_data=body)  # type: ignore[no-any-return]
