"""Schedules resource for the Sonzai SDK.

Recurring per-user schedules. The platform computes ``next_fire_at`` from
the supplied cadence (``{simple: {...}}`` or ``{cron: "..."}``) and honors
any ``active_window`` filter for quiet hours / days-of-week.
"""

from __future__ import annotations

from typing import Any

from .._generated.models import CreateScheduleInputBody, PatchScheduleInputBody
from .._generated.resources.schedules import AsyncSchedules as _GenAsyncSchedules
from .._generated.resources.schedules import Schedules as _GenSchedules
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body
from ..types import (
    DeleteResponse,
    Schedule,
    ScheduleCreateResponse,
    ScheduleListResponse,
    ScheduleUpcomingResponse,
)


def _build_create_body(
    *,
    cadence: dict[str, Any],
    intent: str,
    check_type: str,
    active_window: dict[str, Any] | None,
    inventory_item_id: str | None,
    metadata: dict[str, Any] | None,
    starts_at: str | None,
    ends_at: str | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "cadence": cadence,
        "intent": intent,
        "check_type": check_type,
    }
    if active_window is not None:
        body["active_window"] = active_window
    if inventory_item_id is not None:
        body["inventory_item_id"] = inventory_item_id
    if metadata is not None:
        body["metadata"] = metadata
    if starts_at is not None:
        body["starts_at"] = starts_at
    if ends_at is not None:
        body["ends_at"] = ends_at
    return body


def _build_patch_body(
    *,
    cadence: dict[str, Any] | None,
    active_window: dict[str, Any] | None,
    intent: str | None,
    check_type: str | None,
    metadata: dict[str, Any] | None,
    enabled: bool | None,
    starts_at: str | None,
    ends_at: str | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if cadence is not None:
        body["cadence"] = cadence
    if active_window is not None:
        body["active_window"] = active_window
    if intent is not None:
        body["intent"] = intent
    if check_type is not None:
        body["check_type"] = check_type
    if metadata is not None:
        body["metadata"] = metadata
    if enabled is not None:
        body["enabled"] = enabled
    if starts_at is not None:
        body["starts_at"] = starts_at
    if ends_at is not None:
        body["ends_at"] = ends_at
    return body


class Schedules(_GenSchedules):
    """Hand-written overrides / convenience helpers on top of generated Schedules.

    All hand-written methods remain as overrides preserving the historical SDK
    contract. The subclass inheritance makes future spec additions appear as
    inherited methods automatically.
    """

    # TODO(B.3-followup): __init__ takes HTTPClient (typed); generated _SchedulesBase
    # takes Any. Override kept to preserve typed constructor signature.
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self, agent_id: str, user_id: str) -> ScheduleListResponse:
        """List all schedules for a (agent, user) pair."""
        data = self._http.get(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules"
        )
        return ScheduleListResponse.model_validate(data)

    def create(
        self,
        agent_id: str,
        user_id: str,
        *,
        cadence: dict[str, Any],
        intent: str,
        check_type: str,
        active_window: dict[str, Any] | None = None,
        inventory_item_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        starts_at: str | None = None,
        ends_at: str | None = None,
    ) -> ScheduleCreateResponse:
        """Create a recurring schedule for a user.

        ``cadence`` is ``{"simple": {...}}`` or ``{"cron": "..."}`` with a
        required ``timezone`` field. ``active_window`` is an optional
        quiet-hours/days filter.
        """
        body = encode_body(CreateScheduleInputBody, _build_create_body(
            cadence=cadence,
            intent=intent,
            check_type=check_type,
            active_window=active_window,
            inventory_item_id=inventory_item_id,
            metadata=metadata,
            starts_at=starts_at,
            ends_at=ends_at,
        ))
        data = self._http.post(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules",
            json_data=body,
        )
        return ScheduleCreateResponse.model_validate(data)

    def get(self, agent_id: str, user_id: str, schedule_id: str) -> Schedule:
        """Fetch a single schedule by ID."""
        data = self._http.get(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules/{schedule_id}"
        )
        return Schedule.model_validate(data)

    def update(
        self,
        agent_id: str,
        user_id: str,
        schedule_id: str,
        *,
        cadence: dict[str, Any] | None = None,
        active_window: dict[str, Any] | None = None,
        intent: str | None = None,
        check_type: str | None = None,
        metadata: dict[str, Any] | None = None,
        enabled: bool | None = None,
        starts_at: str | None = None,
        ends_at: str | None = None,
    ) -> Schedule:
        """Partially update a schedule.

        ``next_fire_at`` is recomputed only when ``cadence``, ``active_window``,
        or ``starts_at`` change.
        """
        body = encode_body(PatchScheduleInputBody, _build_patch_body(
            cadence=cadence,
            active_window=active_window,
            intent=intent,
            check_type=check_type,
            metadata=metadata,
            enabled=enabled,
            starts_at=starts_at,
            ends_at=ends_at,
        ))
        data = self._http.patch(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules/{schedule_id}",
            json_data=body,
        )
        return Schedule.model_validate(data)

    def delete(
        self, agent_id: str, user_id: str, schedule_id: str
    ) -> DeleteResponse:
        """Delete a schedule (idempotent — missing IDs return 204)."""
        data = self._http.delete(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules/{schedule_id}"
        )
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)

    def upcoming(
        self,
        agent_id: str,
        user_id: str,
        schedule_id: str,
        *,
        limit: int = 10,
    ) -> ScheduleUpcomingResponse:
        """Preview the next N allowed fire times (does not mutate state)."""
        data = self._http.get(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules/{schedule_id}/upcoming",
            params={"limit": limit},
        )
        return ScheduleUpcomingResponse.model_validate(data)


class AsyncSchedules(_GenAsyncSchedules):
    """Async hand-written overrides on top of generated AsyncSchedules."""

    # TODO(B.3-followup): __init__ takes AsyncHTTPClient (typed); generated base
    # takes Any. Override kept to preserve typed constructor signature.
    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self, agent_id: str, user_id: str) -> ScheduleListResponse:
        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules"
        )
        return ScheduleListResponse.model_validate(data)

    async def create(
        self,
        agent_id: str,
        user_id: str,
        *,
        cadence: dict[str, Any],
        intent: str,
        check_type: str,
        active_window: dict[str, Any] | None = None,
        inventory_item_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        starts_at: str | None = None,
        ends_at: str | None = None,
    ) -> ScheduleCreateResponse:
        body = encode_body(CreateScheduleInputBody, _build_create_body(
            cadence=cadence,
            intent=intent,
            check_type=check_type,
            active_window=active_window,
            inventory_item_id=inventory_item_id,
            metadata=metadata,
            starts_at=starts_at,
            ends_at=ends_at,
        ))
        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules",
            json_data=body,
        )
        return ScheduleCreateResponse.model_validate(data)

    async def get(
        self, agent_id: str, user_id: str, schedule_id: str
    ) -> Schedule:
        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules/{schedule_id}"
        )
        return Schedule.model_validate(data)

    async def update(
        self,
        agent_id: str,
        user_id: str,
        schedule_id: str,
        *,
        cadence: dict[str, Any] | None = None,
        active_window: dict[str, Any] | None = None,
        intent: str | None = None,
        check_type: str | None = None,
        metadata: dict[str, Any] | None = None,
        enabled: bool | None = None,
        starts_at: str | None = None,
        ends_at: str | None = None,
    ) -> Schedule:
        body = encode_body(PatchScheduleInputBody, _build_patch_body(
            cadence=cadence,
            active_window=active_window,
            intent=intent,
            check_type=check_type,
            metadata=metadata,
            enabled=enabled,
            starts_at=starts_at,
            ends_at=ends_at,
        ))
        data = await self._http.patch(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules/{schedule_id}",
            json_data=body,
        )
        return Schedule.model_validate(data)

    async def delete(
        self, agent_id: str, user_id: str, schedule_id: str
    ) -> DeleteResponse:
        data = await self._http.delete(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules/{schedule_id}"
        )
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)

    async def upcoming(
        self,
        agent_id: str,
        user_id: str,
        schedule_id: str,
        *,
        limit: int = 10,
    ) -> ScheduleUpcomingResponse:
        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/users/{user_id}/schedules/{schedule_id}/upcoming",
            params={"limit": limit},
        )
        return ScheduleUpcomingResponse.model_validate(data)
