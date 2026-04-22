"""Storefront resource.

Wraps endpoints under ``/storefront/...``. Returns raw dicts because the
OpenAPI schemas for these endpoints are mostly free-form objects; grab
typed models from ``sonzai._generated.models`` when you need stronger
typing.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .._generated.models import StorefrontUpdateInputBody, StorefrontUpsertAgentInputBody
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body


class Storefront:
    """Sync storefront config + published agents."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def get(self) -> dict[str, Any]:
        """Get the storefront config."""
        return self._http.get("/api/v1/storefront")  # type: ignore[no-any-return]

    def update(
        self,
        *,
        access_type: str | None = None,
        contact_email: str | None = None,
        description: str | None = None,
        display_name: str | None = None,
        hero_image_url: str | None = None,
        invite_code: str | None = None,
        max_visits_per_user: int | None = None,
        slug: str | None = None,
        theme: str | None = None,
    ) -> dict[str, Any]:
        """Update storefront config."""
        raw: dict[str, Any] = {}
        if access_type is not None:
            raw["access_type"] = access_type
        if contact_email is not None:
            raw["contact_email"] = contact_email
        if description is not None:
            raw["description"] = description
        if display_name is not None:
            raw["display_name"] = display_name
        if hero_image_url is not None:
            raw["hero_image_url"] = hero_image_url
        if invite_code is not None:
            raw["invite_code"] = invite_code
        if max_visits_per_user is not None:
            raw["max_visits_per_user"] = max_visits_per_user
        if slug is not None:
            raw["slug"] = slug
        if theme is not None:
            raw["theme"] = theme
        body = encode_body(StorefrontUpdateInputBody, raw)
        return self._http.put("/api/v1/storefront", json_data=body)  # type: ignore[no-any-return]

    def publish(self, **body: Any) -> dict[str, Any]:
        """Publish the storefront."""
        return self._http.post("/api/v1/storefront/publish", json_data=body)  # type: ignore[no-any-return]

    def unpublish(self, **body: Any) -> dict[str, Any]:
        """Unpublish the storefront."""
        return self._http.post("/api/v1/storefront/unpublish", json_data=body)  # type: ignore[no-any-return]

    def list_agents(self) -> dict[str, Any]:
        """List agents on the storefront."""
        return self._http.get("/api/v1/storefront/agents")  # type: ignore[no-any-return]

    def upsert_agent(
        self,
        agent_id: str,
        *,
        avatar_url: str | None = None,
        description: str | None = None,
        display_name: str | None = None,
        featured: bool | None = None,
        max_turns_per_visit: int | None = None,
        slug: str | None = None,
    ) -> dict[str, Any]:
        """Add or update an agent on the storefront."""
        raw: dict[str, Any] = {}
        if avatar_url is not None:
            raw["avatar_url"] = avatar_url
        if description is not None:
            raw["description"] = description
        if display_name is not None:
            raw["display_name"] = display_name
        if featured is not None:
            raw["featured"] = featured
        if max_turns_per_visit is not None:
            raw["max_turns_per_visit"] = max_turns_per_visit
        if slug is not None:
            raw["slug"] = slug
        body = encode_body(StorefrontUpsertAgentInputBody, raw)
        return self._http.put(  # type: ignore[no-any-return]
            f"/api/v1/storefront/agents/{quote(agent_id, safe='')}",
            json_data=body,
        )

    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent from the storefront."""
        self._http.delete(f"/api/v1/storefront/agents/{quote(agent_id, safe='')}")


class AsyncStorefront:
    """Async storefront operations (mirror of :class:`Storefront`)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def get(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/storefront")  # type: ignore[no-any-return]

    async def update(
        self,
        *,
        access_type: str | None = None,
        contact_email: str | None = None,
        description: str | None = None,
        display_name: str | None = None,
        hero_image_url: str | None = None,
        invite_code: str | None = None,
        max_visits_per_user: int | None = None,
        slug: str | None = None,
        theme: str | None = None,
    ) -> dict[str, Any]:
        raw: dict[str, Any] = {}
        if access_type is not None:
            raw["access_type"] = access_type
        if contact_email is not None:
            raw["contact_email"] = contact_email
        if description is not None:
            raw["description"] = description
        if display_name is not None:
            raw["display_name"] = display_name
        if hero_image_url is not None:
            raw["hero_image_url"] = hero_image_url
        if invite_code is not None:
            raw["invite_code"] = invite_code
        if max_visits_per_user is not None:
            raw["max_visits_per_user"] = max_visits_per_user
        if slug is not None:
            raw["slug"] = slug
        if theme is not None:
            raw["theme"] = theme
        body = encode_body(StorefrontUpdateInputBody, raw)
        return await self._http.put("/api/v1/storefront", json_data=body)  # type: ignore[no-any-return]

    async def publish(self, **body: Any) -> dict[str, Any]:
        return await self._http.post("/api/v1/storefront/publish", json_data=body)  # type: ignore[no-any-return]

    async def unpublish(self, **body: Any) -> dict[str, Any]:
        return await self._http.post("/api/v1/storefront/unpublish", json_data=body)  # type: ignore[no-any-return]

    async def list_agents(self) -> dict[str, Any]:
        return await self._http.get("/api/v1/storefront/agents")  # type: ignore[no-any-return]

    async def upsert_agent(
        self,
        agent_id: str,
        *,
        avatar_url: str | None = None,
        description: str | None = None,
        display_name: str | None = None,
        featured: bool | None = None,
        max_turns_per_visit: int | None = None,
        slug: str | None = None,
    ) -> dict[str, Any]:
        raw: dict[str, Any] = {}
        if avatar_url is not None:
            raw["avatar_url"] = avatar_url
        if description is not None:
            raw["description"] = description
        if display_name is not None:
            raw["display_name"] = display_name
        if featured is not None:
            raw["featured"] = featured
        if max_turns_per_visit is not None:
            raw["max_turns_per_visit"] = max_turns_per_visit
        if slug is not None:
            raw["slug"] = slug
        body = encode_body(StorefrontUpsertAgentInputBody, raw)
        return await self._http.put(  # type: ignore[no-any-return]
            f"/api/v1/storefront/agents/{quote(agent_id, safe='')}",
            json_data=body,
        )

    async def remove_agent(self, agent_id: str) -> None:
        await self._http.delete(
            f"/api/v1/storefront/agents/{quote(agent_id, safe='')}"
        )
