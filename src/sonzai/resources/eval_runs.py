"""Eval run resource for the Sonzai SDK."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import EvalRun, EvalRunListResponse, SessionResponse, SimulationEvent


class EvalRuns:
    """Sync eval run operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        agent_id: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> EvalRunListResponse:
        """List eval runs."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if agent_id:
            params["agent_id"] = agent_id

        data = self._http.get("/api/v1/eval-runs", params=params)
        return EvalRunListResponse.model_validate(data)

    def get(self, run_id: str) -> EvalRun:
        """Get a specific eval run."""
        data = self._http.get(f"/api/v1/eval-runs/{run_id}")
        return EvalRun.model_validate(data)

    def delete(self, run_id: str) -> SessionResponse:
        """Delete an eval run."""
        data = self._http.delete(f"/api/v1/eval-runs/{run_id}")
        return SessionResponse.model_validate(data)

    def stream_events(
        self,
        run_id: str,
        *,
        from_index: int = 0,
    ) -> Iterator[SimulationEvent]:
        """Stream SSE events from a running eval. Supports reconnection via from_index."""
        for event in self._http.stream_sse(
            "GET",
            f"/api/v1/eval-runs/{run_id}/events?from={from_index}",
        ):
            yield SimulationEvent.model_validate(event)


class AsyncEvalRuns:
    """Async eval run operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        agent_id: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> EvalRunListResponse:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if agent_id:
            params["agent_id"] = agent_id
        data = await self._http.get("/api/v1/eval-runs", params=params)
        return EvalRunListResponse.model_validate(data)

    async def get(self, run_id: str) -> EvalRun:
        data = await self._http.get(f"/api/v1/eval-runs/{run_id}")
        return EvalRun.model_validate(data)

    async def delete(self, run_id: str) -> SessionResponse:
        data = await self._http.delete(f"/api/v1/eval-runs/{run_id}")
        return SessionResponse.model_validate(data)

    async def stream_events(
        self,
        run_id: str,
        *,
        from_index: int = 0,
    ) -> AsyncIterator[SimulationEvent]:
        """Stream SSE events from a running eval. Supports reconnection via from_index."""
        async for event in self._http.stream_sse(
            "GET",
            f"/api/v1/eval-runs/{run_id}/events?from={from_index}",
        ):
            yield SimulationEvent.model_validate(event)
