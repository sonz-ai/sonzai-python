"""Projects resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._generated.models import (
    CreateAPIKeyInputBody,
    CreateProjectInputBody,
    UpdateProjectInputBody,
)
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body
from ..types import (
    CreateAPIKeyResponse,
    DeleteProjectResponse,
    Project,
    ProjectAPIKey,
    ProjectAPIKeyList,
    ProjectList,
    RevokeAPIKeyResponse,
)


class Projects:
    """Sync project management operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self, *, limit: int = 50, offset: int = 0) -> ProjectList:
        """List all projects for the current tenant."""
        data = self._http.get("/api/v1/projects", params={"limit": limit, "offset": offset})
        if isinstance(data, list):
            from pydantic import TypeAdapter
            projects = TypeAdapter(list[Project]).validate_python(data)
            return ProjectList(projects=projects)
        return ProjectList.model_validate(data if isinstance(data, dict) else {"projects": data or []})

    def create(self, *, name: str, environment: str | None = None) -> Project:
        """Create a new project."""
        raw: dict[str, Any] = {"name": name}
        if environment is not None:
            raw["environment"] = environment
        body = encode_body(CreateProjectInputBody, raw)
        data = self._http.post("/api/v1/projects", json_data=body)
        return Project.model_validate(data)

    def get(self, project_id: str) -> Project:
        """Get a project by ID."""
        data = self._http.get(f"/api/v1/projects/{project_id}")
        return Project.model_validate(data)

    def update(
        self,
        project_id: str,
        *,
        name: str | None = None,
        game_name: str | None = None,
        environment: str | None = None,
    ) -> Project:
        """Update a project."""
        raw: dict[str, Any] = {}
        if name is not None:
            raw["name"] = name
        if game_name is not None:
            raw["game_name"] = game_name
        if environment is not None:
            raw["environment"] = environment
        body = encode_body(UpdateProjectInputBody, raw)
        data = self._http.put(f"/api/v1/projects/{project_id}", json_data=body)
        return Project.model_validate(data)

    def delete(self, project_id: str) -> DeleteProjectResponse:
        """Delete a project."""
        data = self._http.delete(f"/api/v1/projects/{project_id}")
        return DeleteProjectResponse.model_validate(data)

    # -- API Keys --

    def list_keys(self, project_id: str) -> ProjectAPIKeyList:
        """List API keys for a project."""
        data = self._http.get(f"/api/v1/projects/{project_id}/keys")
        if isinstance(data, list):
            from pydantic import TypeAdapter
            keys = TypeAdapter(list[ProjectAPIKey]).validate_python(data)
            return ProjectAPIKeyList(keys=keys)
        return ProjectAPIKeyList.model_validate(data if isinstance(data, dict) else {"keys": data or []})

    def create_key(
        self,
        project_id: str,
        *,
        name: str | None = None,
        expires_days: int | None = None,
        scopes: list[str] | None = None,
    ) -> CreateAPIKeyResponse:
        """Create a new API key. The plaintext key is only returned once."""
        raw: dict[str, Any] = {}
        if name is not None:
            raw["name"] = name
        if expires_days is not None:
            raw["expires_days"] = expires_days
        if scopes is not None:
            raw["scopes"] = scopes
        body = encode_body(CreateAPIKeyInputBody, raw)
        data = self._http.post(f"/api/v1/projects/{project_id}/keys", json_data=body)
        return CreateAPIKeyResponse.model_validate(data)

    def revoke_key(self, project_id: str, key_id: str) -> RevokeAPIKeyResponse:
        """Revoke (delete) an API key."""
        data = self._http.delete(f"/api/v1/projects/{project_id}/keys/{key_id}")
        return RevokeAPIKeyResponse.model_validate(data)


class AsyncProjects:
    """Async project management operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self, *, limit: int = 50, offset: int = 0) -> ProjectList:
        """List all projects for the current tenant."""
        data = await self._http.get("/api/v1/projects", params={"limit": limit, "offset": offset})
        if isinstance(data, list):
            from pydantic import TypeAdapter
            projects = TypeAdapter(list[Project]).validate_python(data)
            return ProjectList(projects=projects)
        return ProjectList.model_validate(data if isinstance(data, dict) else {"projects": data or []})

    async def create(self, *, name: str, environment: str | None = None) -> Project:
        """Create a new project."""
        raw: dict[str, Any] = {"name": name}
        if environment is not None:
            raw["environment"] = environment
        body = encode_body(CreateProjectInputBody, raw)
        data = await self._http.post("/api/v1/projects", json_data=body)
        return Project.model_validate(data)

    async def get(self, project_id: str) -> Project:
        """Get a project by ID."""
        data = await self._http.get(f"/api/v1/projects/{project_id}")
        return Project.model_validate(data)

    async def update(
        self,
        project_id: str,
        *,
        name: str | None = None,
        game_name: str | None = None,
        environment: str | None = None,
    ) -> Project:
        """Update a project."""
        raw: dict[str, Any] = {}
        if name is not None:
            raw["name"] = name
        if game_name is not None:
            raw["game_name"] = game_name
        if environment is not None:
            raw["environment"] = environment
        body = encode_body(UpdateProjectInputBody, raw)
        data = await self._http.put(f"/api/v1/projects/{project_id}", json_data=body)
        return Project.model_validate(data)

    async def delete(self, project_id: str) -> DeleteProjectResponse:
        """Delete a project."""
        data = await self._http.delete(f"/api/v1/projects/{project_id}")
        return DeleteProjectResponse.model_validate(data)

    # -- API Keys --

    async def list_keys(self, project_id: str) -> ProjectAPIKeyList:
        """List API keys for a project."""
        data = await self._http.get(f"/api/v1/projects/{project_id}/keys")
        if isinstance(data, list):
            from pydantic import TypeAdapter
            keys = TypeAdapter(list[ProjectAPIKey]).validate_python(data)
            return ProjectAPIKeyList(keys=keys)
        return ProjectAPIKeyList.model_validate(data if isinstance(data, dict) else {"keys": data or []})

    async def create_key(
        self,
        project_id: str,
        *,
        name: str | None = None,
        expires_days: int | None = None,
        scopes: list[str] | None = None,
    ) -> CreateAPIKeyResponse:
        """Create a new API key. The plaintext key is only returned once."""
        raw: dict[str, Any] = {}
        if name is not None:
            raw["name"] = name
        if expires_days is not None:
            raw["expires_days"] = expires_days
        if scopes is not None:
            raw["scopes"] = scopes
        body = encode_body(CreateAPIKeyInputBody, raw)
        data = await self._http.post(f"/api/v1/projects/{project_id}/keys", json_data=body)
        return CreateAPIKeyResponse.model_validate(data)

    async def revoke_key(self, project_id: str, key_id: str) -> RevokeAPIKeyResponse:
        """Revoke (delete) an API key."""
        data = await self._http.delete(f"/api/v1/projects/{project_id}/keys/{key_id}")
        return RevokeAPIKeyResponse.model_validate(data)
