"""Org billing resource for the Sonzai SDK.

Enterprise/self-serve billing: Stripe checkout and portal, ledger, usage
summaries, contracts, vouchers. Most GET responses are untyped on the
server side — returned as plain dicts.
"""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient


class OrgBilling:
    """Sync org-level billing operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    # --- profile / usage ---

    def get_billing(self) -> dict[str, Any]:
        """Get the org billing profile (plan, credits, Stripe customer, etc.)."""
        return self._http.get("/api/v1/org/billing")

    def get_usage_summary(self, *, days: int | None = None) -> dict[str, Any]:
        """Get a high-level usage summary."""
        params = {"days": days} if days is not None else None
        return self._http.get("/api/v1/org/usage-summary", params=params)

    def get_service_usage(self, *, days: int | None = None) -> dict[str, Any]:
        """Get detailed per-service usage."""
        params = {"days": days} if days is not None else None
        return self._http.get("/api/v1/org/service-usage", params=params)

    def get_context_engine_events(self, *, days: int | None = None) -> dict[str, Any]:
        """Context-engine event usage for the given lookback window."""
        params = {"days": days} if days is not None else None
        return self._http.get("/api/v1/org/events", params=params)

    def get_ledger(self, *, days: int | None = None) -> dict[str, Any]:
        """Get the org billing ledger."""
        params = {"days": days} if days is not None else None
        return self._http.get("/api/v1/org/ledger", params=params)

    def list_active_characters(self, *, days: int | None = None) -> dict[str, Any]:
        """List active characters for billing purposes."""
        params = {"days": days} if days is not None else None
        return self._http.get("/api/v1/org/characters", params=params)

    def get_model_pricing(self) -> dict[str, Any]:
        """Get active model pricing (per-token rates by provider/model)."""
        return self._http.get("/api/v1/org/model-pricing")

    # --- contracts ---

    def get_contract(self) -> dict[str, Any]:
        """Get the org's enterprise contract (if any)."""
        return self._http.get("/api/v1/org/contract")

    def list_service_agreements(self) -> dict[str, Any]:
        """List active service agreements."""
        return self._http.get("/api/v1/org/service-agreements")

    def subscribe_to_contract(self, *, contract_id: str) -> dict[str, Any]:
        """Subscribe the tenant to an enterprise contract."""
        return self._http.post(
            "/api/v1/org/contract/subscribe",
            json_data={"contractId": contract_id},
        )

    # --- Stripe sessions ---

    def create_checkout(
        self,
        *,
        amount: int,
        currency: str | None = None,
    ) -> dict[str, Any]:
        """Create a Stripe checkout session for a credit top-up.

        Args:
            amount: Amount in smallest currency unit (e.g. cents for USD).
            currency: ISO 4217 currency code; defaults to USD server-side.
        """
        body: dict[str, Any] = {"amount": amount}
        if currency is not None:
            body["currency"] = currency
        return self._http.post("/api/v1/org/billing/checkout", json_data=body)

    def create_portal(self) -> dict[str, Any]:
        """Create a Stripe billing-portal session."""
        return self._http.post("/api/v1/org/billing/portal", json_data={})

    # --- vouchers ---

    def redeem_voucher(self, *, code: str) -> dict[str, Any]:
        """Redeem a voucher code."""
        return self._http.post(
            "/api/v1/org/vouchers/redeem",
            json_data={"code": code},
        )


class AsyncOrgBilling:
    """Async org-level billing operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def get_billing(self) -> dict[str, Any]:
        """Get the org billing profile (plan, credits, Stripe customer, etc.)."""
        return await self._http.get("/api/v1/org/billing")

    async def get_usage_summary(self, *, days: int | None = None) -> dict[str, Any]:
        """Get a high-level usage summary."""
        params = {"days": days} if days is not None else None
        return await self._http.get("/api/v1/org/usage-summary", params=params)

    async def get_service_usage(self, *, days: int | None = None) -> dict[str, Any]:
        """Get detailed per-service usage."""
        params = {"days": days} if days is not None else None
        return await self._http.get("/api/v1/org/service-usage", params=params)

    async def get_context_engine_events(self, *, days: int | None = None) -> dict[str, Any]:
        """Context-engine event usage for the given lookback window."""
        params = {"days": days} if days is not None else None
        return await self._http.get("/api/v1/org/events", params=params)

    async def get_ledger(self, *, days: int | None = None) -> dict[str, Any]:
        """Get the org billing ledger."""
        params = {"days": days} if days is not None else None
        return await self._http.get("/api/v1/org/ledger", params=params)

    async def list_active_characters(self, *, days: int | None = None) -> dict[str, Any]:
        """List active characters for billing purposes."""
        params = {"days": days} if days is not None else None
        return await self._http.get("/api/v1/org/characters", params=params)

    async def get_model_pricing(self) -> dict[str, Any]:
        """Get active model pricing."""
        return await self._http.get("/api/v1/org/model-pricing")

    async def get_contract(self) -> dict[str, Any]:
        """Get the org's enterprise contract (if any)."""
        return await self._http.get("/api/v1/org/contract")

    async def list_service_agreements(self) -> dict[str, Any]:
        """List active service agreements."""
        return await self._http.get("/api/v1/org/service-agreements")

    async def subscribe_to_contract(self, *, contract_id: str) -> dict[str, Any]:
        """Subscribe the tenant to an enterprise contract."""
        return await self._http.post(
            "/api/v1/org/contract/subscribe",
            json_data={"contractId": contract_id},
        )

    async def create_checkout(
        self,
        *,
        amount: int,
        currency: str | None = None,
    ) -> dict[str, Any]:
        """Create a Stripe checkout session for a credit top-up."""
        body: dict[str, Any] = {"amount": amount}
        if currency is not None:
            body["currency"] = currency
        return await self._http.post("/api/v1/org/billing/checkout", json_data=body)

    async def create_portal(self) -> dict[str, Any]:
        """Create a Stripe billing-portal session."""
        return await self._http.post("/api/v1/org/billing/portal", json_data={})

    async def redeem_voucher(self, *, code: str) -> dict[str, Any]:
        """Redeem a voucher code."""
        return await self._http.post(
            "/api/v1/org/vouchers/redeem",
            json_data={"code": code},
        )
