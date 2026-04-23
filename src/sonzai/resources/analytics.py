"""Analytics resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._generated.resources.analytics import Analytics as _GenAnalytics
from .._generated.resources.analytics import AsyncAnalytics as _GenAsyncAnalytics
from .._http import AsyncHTTPClient, HTTPClient


class Analytics(_GenAnalytics):
    """Sync analytics operations."""

    def __init__(self, http: HTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    def get_overview(self) -> dict[str, Any]:
        """Get analytics overview for the current project."""
        data = self._http.get("/api/v1/analytics/overview")
        return data  # type: ignore[return-value]

    def get_realtime(self) -> dict[str, Any]:
        """Get real-time analytics for the current project."""
        data = self._http.get("/api/v1/analytics/realtime")
        return data  # type: ignore[return-value]

    def get_usage(self, *, days: int | None = None) -> dict[str, Any]:
        """Get usage analytics. days: 1–365, default 30."""
        params: dict[str, Any] = {}
        if days is not None:
            params["days"] = days
        data = self._http.get("/api/v1/analytics/usage", params=params if params else None)
        return data  # type: ignore[return-value]

    def get_cost(self, *, days: int | None = None) -> dict[str, Any]:
        """Get cost analytics. days: 1–365, default 30."""
        params: dict[str, Any] = {}
        if days is not None:
            params["days"] = days
        data = self._http.get("/api/v1/analytics/cost", params=params if params else None)
        return data  # type: ignore[return-value]

    def get_cost_breakdown(self, *, days: int | None = None) -> dict[str, Any]:
        """Get cost breakdown by model/agent. days: 1–365, default 30."""
        params: dict[str, Any] = {}
        if days is not None:
            params["days"] = days
        data = self._http.get("/api/v1/analytics/cost/breakdown", params=params if params else None)
        return data  # type: ignore[return-value]


class AsyncAnalytics(_GenAsyncAnalytics):
    """Async analytics operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    async def get_overview(self) -> dict[str, Any]:
        """Get analytics overview for the current project."""
        data = await self._http.get("/api/v1/analytics/overview")
        return data  # type: ignore[return-value]

    async def get_realtime(self) -> dict[str, Any]:
        """Get real-time analytics for the current project."""
        data = await self._http.get("/api/v1/analytics/realtime")
        return data  # type: ignore[return-value]

    async def get_usage(self, *, days: int | None = None) -> dict[str, Any]:
        """Get usage analytics. days: 1–365, default 30."""
        params: dict[str, Any] = {}
        if days is not None:
            params["days"] = days
        data = await self._http.get("/api/v1/analytics/usage", params=params if params else None)
        return data  # type: ignore[return-value]

    async def get_cost(self, *, days: int | None = None) -> dict[str, Any]:
        """Get cost analytics. days: 1–365, default 30."""
        params: dict[str, Any] = {}
        if days is not None:
            params["days"] = days
        data = await self._http.get("/api/v1/analytics/cost", params=params if params else None)
        return data  # type: ignore[return-value]

    async def get_cost_breakdown(self, *, days: int | None = None) -> dict[str, Any]:
        """Get cost breakdown by model/agent. days: 1–365, default 30."""
        params: dict[str, Any] = {}
        if days is not None:
            params["days"] = days
        data = await self._http.get("/api/v1/analytics/cost/breakdown", params=params if params else None)
        return data  # type: ignore[return-value]
