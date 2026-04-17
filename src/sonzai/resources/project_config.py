"""Project config resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..post_processing_model import (
    POST_PROCESSING_MODEL_MAP_KEY,
    PostProcessingModelMap,
    decode_post_processing_map,
)
from ..types import ProjectConfigEntry, ProjectConfigListResponse


class ProjectConfig:
    """Sync project configuration operations (key-value store)."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self, project_id: str) -> ProjectConfigListResponse:
        """List all config entries for a project."""
        data = self._http.get(f"/api/v1/projects/{project_id}/config")
        return ProjectConfigListResponse.model_validate(data)

    def get(self, project_id: str, key: str) -> ProjectConfigEntry:
        """Get a config value by key."""
        data = self._http.get(f"/api/v1/projects/{project_id}/config/{key}")
        return ProjectConfigEntry.model_validate(data)

    def set(self, project_id: str, key: str, value: Any) -> dict[str, bool]:
        """Set a config value. Body must be valid JSON."""
        data = self._http.put(
            f"/api/v1/projects/{project_id}/config/{key}",
            json_data=value,
        )
        return data  # type: ignore[return-value]

    def delete(self, project_id: str, key: str) -> None:
        """Delete a config entry."""
        self._http.delete(f"/api/v1/projects/{project_id}/config/{key}")

    # ------------------------------------------------------------------
    # Typed helpers: post-processing model map
    # ------------------------------------------------------------------

    def get_post_processing_model_map(
        self, project_id: str
    ) -> PostProcessingModelMap | None:
        """Read the project-level post-processing model map.

        Returns ``None`` when no map is configured for the project —
        callers can then rely on the account or system-default layer.
        """
        entry = self.get(project_id, POST_PROCESSING_MODEL_MAP_KEY)
        return decode_post_processing_map(entry.value)

    def set_post_processing_model_map(
        self, project_id: str, mapping: PostProcessingModelMap
    ) -> dict[str, bool]:
        """Write the project-level post-processing map (full replace)."""
        return self.set(project_id, POST_PROCESSING_MODEL_MAP_KEY, mapping)

    def delete_post_processing_model_map(self, project_id: str) -> None:
        """Remove the project-level map so the cascade falls through."""
        self.delete(project_id, POST_PROCESSING_MODEL_MAP_KEY)


class AsyncProjectConfig:
    """Async project configuration operations (key-value store)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self, project_id: str) -> ProjectConfigListResponse:
        """List all config entries for a project."""
        data = await self._http.get(f"/api/v1/projects/{project_id}/config")
        return ProjectConfigListResponse.model_validate(data)

    async def get(self, project_id: str, key: str) -> ProjectConfigEntry:
        """Get a config value by key."""
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/config/{key}"
        )
        return ProjectConfigEntry.model_validate(data)

    async def set(
        self, project_id: str, key: str, value: Any
    ) -> dict[str, bool]:
        """Set a config value. Body must be valid JSON."""
        data = await self._http.put(
            f"/api/v1/projects/{project_id}/config/{key}",
            json_data=value,
        )
        return data  # type: ignore[return-value]

    async def delete(self, project_id: str, key: str) -> None:
        """Delete a config entry."""
        await self._http.delete(f"/api/v1/projects/{project_id}/config/{key}")

    # ------------------------------------------------------------------
    # Typed helpers: post-processing model map
    # ------------------------------------------------------------------

    async def get_post_processing_model_map(
        self, project_id: str
    ) -> PostProcessingModelMap | None:
        entry = await self.get(project_id, POST_PROCESSING_MODEL_MAP_KEY)
        return decode_post_processing_map(entry.value)

    async def set_post_processing_model_map(
        self, project_id: str, mapping: PostProcessingModelMap
    ) -> dict[str, bool]:
        return await self.set(
            project_id, POST_PROCESSING_MODEL_MAP_KEY, mapping
        )

    async def delete_post_processing_model_map(
        self, project_id: str
    ) -> None:
        await self.delete(project_id, POST_PROCESSING_MODEL_MAP_KEY)
