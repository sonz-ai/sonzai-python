"""Storefront resource for the Sonzai SDK.

Public agent marketplace: one storefront per tenant, zero-or-more agents
attached. Consumers typically build an admin UI on top of these endpoints.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .._http import AsyncHTTPClient, HTTPClient


class Storefront:
    """Sync storefront operations (tenant-scoped)."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    # --- config ---

    def get(self) -> dict[str, Any]:
        """Get the storefront config for the current tenant."""
        return self._http.get("/api/v1/storefront")

    def update(
        self,
        *,
        slug: str | None = None,
        display_name: str | None = None,
        description: str | None = None,
        hero_image_url: str | None = None,
        theme: str | None = None,
        access_type: str | None = None,
        invite_code: str | None = None,
        contact_email: str | None = None,
        max_visits_per_user: int | None = None,
    ) -> dict[str, Any]:
        """Update storefront config. Only non-None fields are sent."""
        body: dict[str, Any] = {}
        if slug is not None:
            body["slug"] = slug
        if display_name is not None:
            body["display_name"] = display_name
        if description is not None:
            body["description"] = description
        if hero_image_url is not None:
            body["hero_image_url"] = hero_image_url
        if theme is not None:
            body["theme"] = theme
        if access_type is not None:
            body["access_type"] = access_type
        if invite_code is not None:
            body["invite_code"] = invite_code
        if contact_email is not None:
            body["contact_email"] = contact_email
        if max_visits_per_user is not None:
            body["max_visits_per_user"] = max_visits_per_user
        return self._http.put("/api/v1/storefront", json_data=body)

    def publish(self) -> dict[str, Any]:
        """Publish the storefront."""
        return self._http.post("/api/v1/storefront/publish", json_data={})

    def unpublish(self) -> dict[str, Any]:
        """Unpublish the storefront."""
        return self._http.post("/api/v1/storefront/unpublish", json_data={})

    # --- agents on the storefront ---

    def list_agents(self) -> dict[str, Any]:
        """List agents attached to the storefront."""
        return self._http.get("/api/v1/storefront/agents")

    def upsert_agent(
        self,
        agent_id: str,
        *,
        slug: str | None = None,
        display_name: str | None = None,
        description: str | None = None,
        avatar_url: str | None = None,
        featured: bool | None = None,
        max_turns_per_visit: int | None = None,
    ) -> dict[str, Any]:
        """Add or update an agent on the storefront."""
        body: dict[str, Any] = {}
        if slug is not None:
            body["slug"] = slug
        if display_name is not None:
            body["display_name"] = display_name
        if description is not None:
            body["description"] = description
        if avatar_url is not None:
            body["avatar_url"] = avatar_url
        if featured is not None:
            body["featured"] = featured
        if max_turns_per_visit is not None:
            body["max_turns_per_visit"] = max_turns_per_visit
        return self._http.put(
            f"/api/v1/storefront/agents/{quote(agent_id, safe='')}",
            json_data=body,
        )

    def remove_agent(self, agent_id: str) -> dict[str, Any]:
        """Remove an agent from the storefront."""
        return self._http.delete(
            f"/api/v1/storefront/agents/{quote(agent_id, safe='')}"
        )


class AsyncStorefront:
    """Async storefront operations (tenant-scoped)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def get(self) -> dict[str, Any]:
        """Get the storefront config for the current tenant."""
        return await self._http.get("/api/v1/storefront")

    async def update(
        self,
        *,
        slug: str | None = None,
        display_name: str | None = None,
        description: str | None = None,
        hero_image_url: str | None = None,
        theme: str | None = None,
        access_type: str | None = None,
        invite_code: str | None = None,
        contact_email: str | None = None,
        max_visits_per_user: int | None = None,
    ) -> dict[str, Any]:
        """Update storefront config. Only non-None fields are sent."""
        body: dict[str, Any] = {}
        if slug is not None:
            body["slug"] = slug
        if display_name is not None:
            body["display_name"] = display_name
        if description is not None:
            body["description"] = description
        if hero_image_url is not None:
            body["hero_image_url"] = hero_image_url
        if theme is not None:
            body["theme"] = theme
        if access_type is not None:
            body["access_type"] = access_type
        if invite_code is not None:
            body["invite_code"] = invite_code
        if contact_email is not None:
            body["contact_email"] = contact_email
        if max_visits_per_user is not None:
            body["max_visits_per_user"] = max_visits_per_user
        return await self._http.put("/api/v1/storefront", json_data=body)

    async def publish(self) -> dict[str, Any]:
        """Publish the storefront."""
        return await self._http.post("/api/v1/storefront/publish", json_data={})

    async def unpublish(self) -> dict[str, Any]:
        """Unpublish the storefront."""
        return await self._http.post("/api/v1/storefront/unpublish", json_data={})

    async def list_agents(self) -> dict[str, Any]:
        """List agents attached to the storefront."""
        return await self._http.get("/api/v1/storefront/agents")

    async def upsert_agent(
        self,
        agent_id: str,
        *,
        slug: str | None = None,
        display_name: str | None = None,
        description: str | None = None,
        avatar_url: str | None = None,
        featured: bool | None = None,
        max_turns_per_visit: int | None = None,
    ) -> dict[str, Any]:
        """Add or update an agent on the storefront."""
        body: dict[str, Any] = {}
        if slug is not None:
            body["slug"] = slug
        if display_name is not None:
            body["display_name"] = display_name
        if description is not None:
            body["description"] = description
        if avatar_url is not None:
            body["avatar_url"] = avatar_url
        if featured is not None:
            body["featured"] = featured
        if max_turns_per_visit is not None:
            body["max_turns_per_visit"] = max_turns_per_visit
        return await self._http.put(
            f"/api/v1/storefront/agents/{quote(agent_id, safe='')}",
            json_data=body,
        )

    async def remove_agent(self, agent_id: str) -> dict[str, Any]:
        """Remove an agent from the storefront."""
        return await self._http.delete(
            f"/api/v1/storefront/agents/{quote(agent_id, safe='')}"
        )
