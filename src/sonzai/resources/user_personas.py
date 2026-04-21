"""User personas resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import DeleteUserPersonaResponse, UserPersonaList, UserPersonaRecord


class UserPersonas:
    """Sync user persona operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self) -> UserPersonaList:
        """List all user personas for the current tenant."""
        data = self._http.get("/api/v1/user-personas")
        if isinstance(data, list):
            from pydantic import TypeAdapter
            personas = TypeAdapter(list[UserPersonaRecord]).validate_python(data)
            return UserPersonaList(personas=personas)
        return UserPersonaList.model_validate(data)

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        style: str | None = None,
    ) -> UserPersonaRecord:
        """Create a new user persona."""
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if style is not None:
            body["style"] = style
        data = self._http.post("/api/v1/user-personas", json_data=body)
        return UserPersonaRecord.model_validate(data)

    def get(self, persona_id: str) -> UserPersonaRecord:
        """Get a user persona by ID."""
        data = self._http.get(f"/api/v1/user-personas/{persona_id}")
        return UserPersonaRecord.model_validate(data)

    def update(
        self,
        persona_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        style: str | None = None,
    ) -> UserPersonaRecord:
        """Update a user persona."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if style is not None:
            body["style"] = style
        data = self._http.put(f"/api/v1/user-personas/{persona_id}", json_data=body)
        return UserPersonaRecord.model_validate(data)

    def delete(self, persona_id: str) -> DeleteUserPersonaResponse:
        """Delete a user persona."""
        data = self._http.delete(f"/api/v1/user-personas/{persona_id}")
        return DeleteUserPersonaResponse.model_validate(data)


class AsyncUserPersonas:
    """Async user persona operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self) -> UserPersonaList:
        """List all user personas for the current tenant."""
        data = await self._http.get("/api/v1/user-personas")
        if isinstance(data, list):
            from pydantic import TypeAdapter
            personas = TypeAdapter(list[UserPersonaRecord]).validate_python(data)
            return UserPersonaList(personas=personas)
        return UserPersonaList.model_validate(data)

    async def create(
        self,
        *,
        name: str,
        description: str | None = None,
        style: str | None = None,
    ) -> UserPersonaRecord:
        """Create a new user persona."""
        body: dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if style is not None:
            body["style"] = style
        data = await self._http.post("/api/v1/user-personas", json_data=body)
        return UserPersonaRecord.model_validate(data)

    async def get(self, persona_id: str) -> UserPersonaRecord:
        """Get a user persona by ID."""
        data = await self._http.get(f"/api/v1/user-personas/{persona_id}")
        return UserPersonaRecord.model_validate(data)

    async def update(
        self,
        persona_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        style: str | None = None,
    ) -> UserPersonaRecord:
        """Update a user persona."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if style is not None:
            body["style"] = style
        data = await self._http.put(f"/api/v1/user-personas/{persona_id}", json_data=body)
        return UserPersonaRecord.model_validate(data)

    async def delete(self, persona_id: str) -> DeleteUserPersonaResponse:
        """Delete a user persona."""
        data = await self._http.delete(f"/api/v1/user-personas/{persona_id}")
        return DeleteUserPersonaResponse.model_validate(data)
