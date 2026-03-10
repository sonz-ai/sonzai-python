"""Eval run resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .._http import AsyncHTTPClient, HTTPClient
from ..types import EvalRun, EvalRunListResponse, SessionResponse


class EvalRuns:
    """Sync eval run operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        agent_id: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> EvalRunListResponse:
        """List eval runs."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
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


class AsyncEvalRuns:
    """Async eval run operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        agent_id: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> EvalRunListResponse:
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
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
