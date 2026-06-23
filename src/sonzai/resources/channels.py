"""Channels resource for the Sonzai SDK.

Notification channels are tenant-scoped delivery targets (webhook, email,
composio) that fan out platform events. Mirrors the webhooks resource shape
but backed by the CRUD ``/api/v1/channels`` endpoints.
"""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import Channel, ChannelListResponse

# Module-level alias for ``list[str]``. The resource classes define a ``list``
# method, which shadows the ``list`` builtin for any parameter annotation
# declared after it at class scope — using this alias keeps ``events``
# annotations resolving to the builtin regardless of method ordering.
_EventList = list[str]


def _build_body(
    *,
    name: str,
    type: str,
    config: dict[str, Any] | None,
    events: _EventList | None,
    filter: dict[str, Any] | None,
    active: bool | None,
) -> dict[str, Any]:
    """Build a create/update write body, omitting None-valued optional fields."""
    body: dict[str, Any] = {"name": name, "type": type}
    if config is not None:
        body["config"] = config
    if events is not None:
        body["events"] = events
    if filter is not None:
        body["filter"] = filter
    if active is not None:
        body["active"] = active
    return body


class Channels:
    """Sync notification channel management operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self) -> ChannelListResponse:
        """List all notification channels for the tenant."""
        data = self._http.get("/api/v1/channels")
        return ChannelListResponse.model_validate(data)

    def create(
        self,
        *,
        name: str,
        type: str,
        config: dict[str, Any] | None = None,
        events: _EventList | None = None,
        filter: dict[str, Any] | None = None,
        active: bool | None = None,
    ) -> Channel:
        """Create a notification channel."""
        body = _build_body(
            name=name,
            type=type,
            config=config,
            events=events,
            filter=filter,
            active=active,
        )
        data = self._http.post("/api/v1/channels", json_data=body)
        return Channel.model_validate(data)

    def get(self, channel_id: str) -> Channel:
        """Fetch a single notification channel by ID."""
        data = self._http.get(f"/api/v1/channels/{channel_id}")
        return Channel.model_validate(data)

    def update(
        self,
        channel_id: str,
        *,
        name: str,
        type: str,
        config: dict[str, Any] | None = None,
        events: _EventList | None = None,
        filter: dict[str, Any] | None = None,
        active: bool | None = None,
    ) -> Channel:
        """Update a notification channel."""
        body = _build_body(
            name=name,
            type=type,
            config=config,
            events=events,
            filter=filter,
            active=active,
        )
        data = self._http.put(f"/api/v1/channels/{channel_id}", json_data=body)
        return Channel.model_validate(data)

    def delete(self, channel_id: str) -> None:
        """Delete a notification channel."""
        self._http.delete(f"/api/v1/channels/{channel_id}")


class AsyncChannels:
    """Async notification channel management operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self) -> ChannelListResponse:
        """List all notification channels for the tenant."""
        data = await self._http.get("/api/v1/channels")
        return ChannelListResponse.model_validate(data)

    async def create(
        self,
        *,
        name: str,
        type: str,
        config: dict[str, Any] | None = None,
        events: _EventList | None = None,
        filter: dict[str, Any] | None = None,
        active: bool | None = None,
    ) -> Channel:
        """Create a notification channel."""
        body = _build_body(
            name=name,
            type=type,
            config=config,
            events=events,
            filter=filter,
            active=active,
        )
        data = await self._http.post("/api/v1/channels", json_data=body)
        return Channel.model_validate(data)

    async def get(self, channel_id: str) -> Channel:
        """Fetch a single notification channel by ID."""
        data = await self._http.get(f"/api/v1/channels/{channel_id}")
        return Channel.model_validate(data)

    async def update(
        self,
        channel_id: str,
        *,
        name: str,
        type: str,
        config: dict[str, Any] | None = None,
        events: _EventList | None = None,
        filter: dict[str, Any] | None = None,
        active: bool | None = None,
    ) -> Channel:
        """Update a notification channel."""
        body = _build_body(
            name=name,
            type=type,
            config=config,
            events=events,
            filter=filter,
            active=active,
        )
        data = await self._http.put(
            f"/api/v1/channels/{channel_id}", json_data=body
        )
        return Channel.model_validate(data)

    async def delete(self, channel_id: str) -> None:
        """Delete a notification channel."""
        await self._http.delete(f"/api/v1/channels/{channel_id}")
