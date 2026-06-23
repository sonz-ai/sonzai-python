"""Pipelines resource for the Sonzai SDK.

Pipelines are tenant-scoped, ordered sequences of named steps that can be
executed to produce structured findings. Backed by the CRUD
``/api/v1/pipelines`` endpoints plus ``/steps`` and ``/run`` actions.

Runs are asynchronous: ``run()`` enqueues a run and returns immediately with a
queued :class:`PipelineRun`. Poll ``get_run()`` (or use the convenience
``run_and_wait()``) until the run reaches a terminal status.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    Pipeline,
    PipelineListResponse,
    PipelineRun,
    PipelineRunListResponse,
)

# Step definitions are passed as a list of ``{"slug", "title"?}`` dicts.
_StepList = list[dict[str, Any]]

# Terminal statuses for an async pipeline run.
_TERMINAL_STATUSES = frozenset({"completed", "failed"})


def _build_body(
    *,
    name: str,
    description: str | None,
    steps: _StepList | None,
) -> dict[str, Any]:
    """Build a create/update write body, omitting None-valued optional fields."""
    body: dict[str, Any] = {"name": name}
    if description is not None:
        body["description"] = description
    if steps is not None:
        body["steps"] = steps
    return body


class Pipelines:
    """Sync pipeline management operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self) -> PipelineListResponse:
        """List all pipelines for the tenant."""
        data = self._http.get("/api/v1/pipelines")
        return PipelineListResponse.model_validate(data)

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        steps: _StepList | None = None,
    ) -> Pipeline:
        """Create a pipeline."""
        body = _build_body(name=name, description=description, steps=steps)
        data = self._http.post("/api/v1/pipelines", json_data=body)
        return Pipeline.model_validate(data)

    def get(self, pipeline_id: str) -> Pipeline:
        """Fetch a single pipeline by ID."""
        data = self._http.get(f"/api/v1/pipelines/{pipeline_id}")
        return Pipeline.model_validate(data)

    def update(
        self,
        pipeline_id: str,
        *,
        name: str,
        description: str | None = None,
        steps: _StepList | None = None,
    ) -> Pipeline:
        """Update a pipeline."""
        body = _build_body(name=name, description=description, steps=steps)
        data = self._http.put(f"/api/v1/pipelines/{pipeline_id}", json_data=body)
        return Pipeline.model_validate(data)

    def delete(self, pipeline_id: str) -> None:
        """Delete a pipeline."""
        self._http.delete(f"/api/v1/pipelines/{pipeline_id}")

    def append_step(
        self,
        pipeline_id: str,
        *,
        slug: str,
        title: str | None = None,
    ) -> Pipeline:
        """Append a step to a pipeline."""
        body: dict[str, Any] = {"slug": slug}
        if title is not None:
            body["title"] = title
        data = self._http.post(
            f"/api/v1/pipelines/{pipeline_id}/steps", json_data=body
        )
        return Pipeline.model_validate(data)

    def run(
        self,
        pipeline_id: str,
        *,
        input: dict[str, Any] | None = None,
    ) -> PipelineRun:
        """Enqueue a pipeline run.

        Returns immediately with a queued :class:`PipelineRun` (``status`` is
        ``"queued"``). Poll :meth:`get_run` to observe progress, or use
        :meth:`run_and_wait` to block until the run completes.
        """
        body: dict[str, Any] = {}
        if input is not None:
            body["input"] = input
        data = self._http.post(
            f"/api/v1/pipelines/{pipeline_id}/run",
            json_data=body,
        )
        return PipelineRun.model_validate(data)

    def get_run(self, pipeline_id: str, run_id: str) -> PipelineRun:
        """Fetch a single pipeline run by ID."""
        data = self._http.get(
            f"/api/v1/pipelines/{pipeline_id}/runs/{run_id}"
        )
        return PipelineRun.model_validate(data)

    def list_runs(self, pipeline_id: str) -> PipelineRunListResponse:
        """List all runs for a pipeline."""
        data = self._http.get(f"/api/v1/pipelines/{pipeline_id}/runs")
        return PipelineRunListResponse.model_validate(data)

    def run_and_wait(
        self,
        pipeline_id: str,
        *,
        input: dict[str, Any] | None = None,
        poll_interval: float = 2.0,
        timeout: float = 1800.0,
    ) -> PipelineRun:
        """Enqueue a run and poll until it reaches a terminal status.

        Raises:
            TimeoutError: if the run does not complete within ``timeout`` seconds.
        """
        run = self.run(pipeline_id, input=input)
        if run.status in _TERMINAL_STATUSES:
            return run
        deadline = time.monotonic() + timeout
        while True:
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"pipeline run {run.run_id} did not complete within "
                    f"{timeout}s (last status: {run.status!r})"
                )
            time.sleep(poll_interval)
            run = self.get_run(pipeline_id, run.run_id)
            if run.status in _TERMINAL_STATUSES:
                return run


class AsyncPipelines:
    """Async pipeline management operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self) -> PipelineListResponse:
        """List all pipelines for the tenant."""
        data = await self._http.get("/api/v1/pipelines")
        return PipelineListResponse.model_validate(data)

    async def create(
        self,
        *,
        name: str,
        description: str | None = None,
        steps: _StepList | None = None,
    ) -> Pipeline:
        """Create a pipeline."""
        body = _build_body(name=name, description=description, steps=steps)
        data = await self._http.post("/api/v1/pipelines", json_data=body)
        return Pipeline.model_validate(data)

    async def get(self, pipeline_id: str) -> Pipeline:
        """Fetch a single pipeline by ID."""
        data = await self._http.get(f"/api/v1/pipelines/{pipeline_id}")
        return Pipeline.model_validate(data)

    async def update(
        self,
        pipeline_id: str,
        *,
        name: str,
        description: str | None = None,
        steps: _StepList | None = None,
    ) -> Pipeline:
        """Update a pipeline."""
        body = _build_body(name=name, description=description, steps=steps)
        data = await self._http.put(
            f"/api/v1/pipelines/{pipeline_id}", json_data=body
        )
        return Pipeline.model_validate(data)

    async def delete(self, pipeline_id: str) -> None:
        """Delete a pipeline."""
        await self._http.delete(f"/api/v1/pipelines/{pipeline_id}")

    async def append_step(
        self,
        pipeline_id: str,
        *,
        slug: str,
        title: str | None = None,
    ) -> Pipeline:
        """Append a step to a pipeline."""
        body: dict[str, Any] = {"slug": slug}
        if title is not None:
            body["title"] = title
        data = await self._http.post(
            f"/api/v1/pipelines/{pipeline_id}/steps", json_data=body
        )
        return Pipeline.model_validate(data)

    async def run(
        self,
        pipeline_id: str,
        *,
        input: dict[str, Any] | None = None,
    ) -> PipelineRun:
        """Enqueue a pipeline run.

        Returns immediately with a queued :class:`PipelineRun` (``status`` is
        ``"queued"``). Poll :meth:`get_run` to observe progress, or use
        :meth:`run_and_wait` to block until the run completes.
        """
        body: dict[str, Any] = {}
        if input is not None:
            body["input"] = input
        data = await self._http.post(
            f"/api/v1/pipelines/{pipeline_id}/run",
            json_data=body,
        )
        return PipelineRun.model_validate(data)

    async def get_run(self, pipeline_id: str, run_id: str) -> PipelineRun:
        """Fetch a single pipeline run by ID."""
        data = await self._http.get(
            f"/api/v1/pipelines/{pipeline_id}/runs/{run_id}"
        )
        return PipelineRun.model_validate(data)

    async def list_runs(self, pipeline_id: str) -> PipelineRunListResponse:
        """List all runs for a pipeline."""
        data = await self._http.get(f"/api/v1/pipelines/{pipeline_id}/runs")
        return PipelineRunListResponse.model_validate(data)

    async def run_and_wait(
        self,
        pipeline_id: str,
        *,
        input: dict[str, Any] | None = None,
        poll_interval: float = 2.0,
        timeout: float = 1800.0,
    ) -> PipelineRun:
        """Enqueue a run and poll until it reaches a terminal status.

        Raises:
            TimeoutError: if the run does not complete within ``timeout`` seconds.
        """
        run = await self.run(pipeline_id, input=input)
        if run.status in _TERMINAL_STATUSES:
            return run
        deadline = time.monotonic() + timeout
        while True:
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"pipeline run {run.run_id} did not complete within "
                    f"{timeout}s (last status: {run.status!r})"
                )
            await asyncio.sleep(poll_interval)
            run = await self.get_run(pipeline_id, run.run_id)
            if run.status in _TERMINAL_STATUSES:
                return run
