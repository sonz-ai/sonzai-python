"""Project notifications resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._generated.models import AcknowledgeProjectNotificationsInputBody
from .._generated.resources.notifications import AsyncNotifications as _GenAsyncNotifications
from .._generated.resources.notifications import Notifications as _GenNotifications
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body
from ..types import AcknowledgeResponse, ProjectNotificationListResponse


class ProjectNotifications(_GenNotifications):
    """Sync project-scoped notification polling operations."""

    def __init__(self, http: HTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    def list(
        self,
        project_id: str,
        *,
        agent_id: str | None = None,
        event_type: str | None = None,
        limit: int | None = None,
    ) -> ProjectNotificationListResponse:
        """List pending notifications for a project."""
        params: dict[str, Any] = {}
        if agent_id:
            params["agent_id"] = agent_id
        if event_type:
            params["event_type"] = event_type
        if limit is not None:
            params["limit"] = limit

        data = self._http.get(
            f"/api/v1/projects/{project_id}/notifications",
            params=params,
        )
        return ProjectNotificationListResponse.model_validate(data)

    def acknowledge(
        self,
        project_id: str,
        notification_ids: list[str],
    ) -> AcknowledgeResponse:
        """Acknowledge specific notifications by ID."""
        body = encode_body(
            AcknowledgeProjectNotificationsInputBody,
            {"notification_ids": notification_ids},
        )
        data = self._http.post(
            f"/api/v1/projects/{project_id}/notifications/acknowledge",
            json_data=body,
        )
        return AcknowledgeResponse.model_validate(data)

    def acknowledge_all(
        self,
        project_id: str,
        *,
        agent_id: str | None = None,
        event_type: str | None = None,
    ) -> AcknowledgeResponse:
        """Acknowledge all pending notifications for a project."""
        params: dict[str, Any] = {}
        if agent_id:
            params["agent_id"] = agent_id
        if event_type:
            params["event_type"] = event_type

        data = self._http.post(
            f"/api/v1/projects/{project_id}/notifications/acknowledge-all",
            params=params,
        )
        return AcknowledgeResponse.model_validate(data)


class AsyncProjectNotifications(_GenAsyncNotifications):
    """Async project-scoped notification polling operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    async def list(
        self,
        project_id: str,
        *,
        agent_id: str | None = None,
        event_type: str | None = None,
        limit: int | None = None,
    ) -> ProjectNotificationListResponse:
        params: dict[str, Any] = {}
        if agent_id:
            params["agent_id"] = agent_id
        if event_type:
            params["event_type"] = event_type
        if limit is not None:
            params["limit"] = limit

        data = await self._http.get(
            f"/api/v1/projects/{project_id}/notifications",
            params=params,
        )
        return ProjectNotificationListResponse.model_validate(data)

    async def acknowledge(
        self,
        project_id: str,
        notification_ids: list[str],
    ) -> AcknowledgeResponse:
        body = encode_body(
            AcknowledgeProjectNotificationsInputBody,
            {"notification_ids": notification_ids},
        )
        data = await self._http.post(
            f"/api/v1/projects/{project_id}/notifications/acknowledge",
            json_data=body,
        )
        return AcknowledgeResponse.model_validate(data)

    async def acknowledge_all(
        self,
        project_id: str,
        *,
        agent_id: str | None = None,
        event_type: str | None = None,
    ) -> AcknowledgeResponse:
        params: dict[str, Any] = {}
        if agent_id:
            params["agent_id"] = agent_id
        if event_type:
            params["event_type"] = event_type

        data = await self._http.post(
            f"/api/v1/projects/{project_id}/notifications/acknowledge-all",
            params=params,
        )
        return AcknowledgeResponse.model_validate(data)
