"""Notification resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._generated.resources.notifications import AsyncNotifications as _GenAsyncNotifications
from .._generated.resources.notifications import Notifications as _GenNotifications
from .._http import AsyncHTTPClient, HTTPClient
from ..types import NotificationListResponse, SessionResponse


class Notifications(_GenNotifications):
    """Hand-written overrides / convenience helpers on top of generated Notifications.

    All hand-written methods remain as overrides preserving the historical SDK
    contract. The subclass inheritance makes future spec additions appear as
    inherited methods automatically.
    """

    # TODO(B.3-followup): __init__ takes HTTPClient (typed); generated _NotificationsBase
    # takes Any. Override kept to preserve typed constructor signature.
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(
        self,
        agent_id: str,
        *,
        status: str | None = None,
        user_id: str | None = None,
        limit: int = 50,
    ) -> NotificationListResponse:
        """List notifications for an agent."""
        params: dict[str, Any] = {"limit": limit}
        if status:
            params["status"] = status
        if user_id:
            params["user_id"] = user_id

        data = self._http.get(
            f"/api/v1/agents/{agent_id}/notifications", params=params
        )
        return NotificationListResponse.model_validate(data)

    def consume(self, agent_id: str, message_id: str) -> SessionResponse:
        """Mark a notification as consumed."""
        data = self._http.post(
            f"/api/v1/agents/{agent_id}/notifications/{message_id}/consume"
        )
        return SessionResponse.model_validate(data)

    def history(
        self,
        agent_id: str,
        *,
        limit: int = 50,
    ) -> NotificationListResponse:
        """List notification history."""
        data = self._http.get(
            f"/api/v1/agents/{agent_id}/notifications/history",
            params={"limit": limit},
        )
        return NotificationListResponse.model_validate(data)


class AsyncNotifications(_GenAsyncNotifications):
    """Async hand-written overrides on top of generated AsyncNotifications."""

    # TODO(B.3-followup): __init__ takes AsyncHTTPClient (typed); generated base
    # takes Any. Override kept to preserve typed constructor signature.
    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        agent_id: str,
        *,
        status: str | None = None,
        user_id: str | None = None,
        limit: int = 50,
    ) -> NotificationListResponse:
        params: dict[str, Any] = {"limit": limit}
        if status:
            params["status"] = status
        if user_id:
            params["user_id"] = user_id

        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/notifications", params=params
        )
        return NotificationListResponse.model_validate(data)

    async def consume(self, agent_id: str, message_id: str) -> SessionResponse:
        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/notifications/{message_id}/consume"
        )
        return SessionResponse.model_validate(data)

    async def history(
        self,
        agent_id: str,
        *,
        limit: int = 50,
    ) -> NotificationListResponse:
        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/notifications/history",
            params={"limit": limit},
        )
        return NotificationListResponse.model_validate(data)
