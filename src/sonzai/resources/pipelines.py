"""Pipelines resource for the Sonzai SDK.

Pipelines are tenant-scoped, ordered sequences of named steps that can be
executed to produce structured findings. Backed by the CRUD
``/api/v1/pipelines`` endpoints plus ``/steps`` and ``/run`` actions.
"""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import Pipeline, PipelineListResponse, PipelineRun

# Step definitions are passed as a list of ``{"slug", "title"?}`` dicts.
_StepList = list[dict[str, Any]]

# Pipeline runs can take minutes — give them a generous timeout.
_RUN_TIMEOUT_SECONDS = 600.0


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
        """Run a pipeline. May take minutes; uses an extended request timeout."""
        body: dict[str, Any] = {}
        if input is not None:
            body["input"] = input
        data = self._http.post(
            f"/api/v1/pipelines/{pipeline_id}/run",
            json_data=body,
            timeout=_RUN_TIMEOUT_SECONDS,
        )
        return PipelineRun.model_validate(data)


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
        """Run a pipeline. May take minutes; uses an extended request timeout."""
        body: dict[str, Any] = {}
        if input is not None:
            body["input"] = input
        data = await self._http.post(
            f"/api/v1/pipelines/{pipeline_id}/run",
            json_data=body,
            timeout=_RUN_TIMEOUT_SECONDS,
        )
        return PipelineRun.model_validate(data)
