"""Project config resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
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
