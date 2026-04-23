"""Personality resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._generated.resources.personality import AsyncPersonality as _GenAsyncPersonality
from .._generated.resources.personality import Personality as _GenPersonality
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body
from .._generated.models import BatchGetPersonalitiesInputBody
from ..types import (
    BatchPersonalityResponse,
    PersonalityResponse,
    PersonalityUpdateResponse,
    RecentShiftsResponse,
    SignificantMomentsResponse,
    UserOverlayDetailResponse,
    UserOverlaysListResponse,
)


class Personality(_GenPersonality):
    """Hand-written overrides / convenience helpers on top of generated Personality.

    All hand-written methods remain as overrides preserving the historical SDK
    contract. The subclass inheritance makes future spec additions appear as
    inherited methods automatically.
    """

    # TODO(B.3-followup): __init__ takes HTTPClient (typed); generated _PersonalityBase
    # takes Any. Override kept to preserve typed constructor signature.
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def get(
        self,
        agent_id: str,
        *,
        history_limit: int = 200,
        since: str | None = None,
    ) -> PersonalityResponse:
        """Get personality profile and evolution history."""
        params: dict[str, Any] = {"history_limit": history_limit}
        if since:
            params["since"] = since

        data = self._http.get(
            f"/api/v1/agents/{agent_id}/personality", params=params
        )
        return PersonalityResponse.model_validate(data)

    def update(
        self,
        agent_id: str,
        *,
        big5: dict[str, Any],
        assessment_method: str | None = None,
        total_exchanges: int | None = None,
    ) -> PersonalityUpdateResponse:
        """Update an agent's Big5 personality scores."""
        # NOTE: not routed through encode_body — UpdatePersonalityBody does not include
        # assessment_method or total_exchanges; migrating would silently drop those fields.
        body: dict[str, Any] = {"big5": big5}
        if assessment_method is not None:
            body["assessment_method"] = assessment_method
        if total_exchanges is not None:
            body["total_exchanges"] = total_exchanges

        data = self._http.put(
            f"/api/v1/agents/{agent_id}/personality", json_data=body
        )
        return PersonalityUpdateResponse.model_validate(data)

    def batch_get(self, agent_ids: list[str]) -> BatchPersonalityResponse:
        """Get personality profiles for multiple agents at once."""
        body = encode_body(BatchGetPersonalitiesInputBody, {"agent_ids": agent_ids})
        return BatchPersonalityResponse.model_validate(
            self._http.post("/api/v1/agents/personalities/batch", json_data=body)
        )

    def get_significant_moments(
        self, agent_id: str, *, limit: int | None = None
    ) -> SignificantMomentsResponse:
        """Get significant moments for an agent's personality evolution."""
        params: dict[str, str] = {}
        if limit is not None:
            params["limit"] = str(limit)
        return SignificantMomentsResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/personality/significant-moments", params=params)
        )

    def get_recent_shifts(self, agent_id: str) -> RecentShiftsResponse:
        """Get recent personality shifts for an agent."""
        return RecentShiftsResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/personality/recent-shifts")
        )

    def list_user_overlays(self, agent_id: str) -> UserOverlaysListResponse:
        """List all user-specific personality overlays for an agent."""
        return UserOverlaysListResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/personality/users")
        )

    def get_user_overlay(
        self,
        agent_id: str,
        user_id: str,
        *,
        instance_id: str | None = None,
        since: str | None = None,
    ) -> UserOverlayDetailResponse:
        """Get a specific user's personality overlay for an agent."""
        params: dict[str, str] = {}
        if instance_id is not None:
            params["instance_id"] = instance_id
        if since is not None:
            params["since"] = since
        return UserOverlayDetailResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/personality/users/{user_id}", params=params)
        )


class AsyncPersonality(_GenAsyncPersonality):
    """Async hand-written overrides on top of generated AsyncPersonality."""

    # TODO(B.3-followup): __init__ takes AsyncHTTPClient (typed); generated base
    # takes Any. Override kept to preserve typed constructor signature.
    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def get(
        self,
        agent_id: str,
        *,
        history_limit: int = 200,
        since: str | None = None,
    ) -> PersonalityResponse:
        params: dict[str, Any] = {"history_limit": history_limit}
        if since:
            params["since"] = since

        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/personality", params=params
        )
        return PersonalityResponse.model_validate(data)

    async def update(
        self,
        agent_id: str,
        *,
        big5: dict[str, Any],
        assessment_method: str | None = None,
        total_exchanges: int | None = None,
    ) -> PersonalityUpdateResponse:
        """Update an agent's Big5 personality scores."""
        # NOTE: not routed through encode_body — UpdatePersonalityBody does not include
        # assessment_method or total_exchanges; migrating would silently drop those fields.
        body: dict[str, Any] = {"big5": big5}
        if assessment_method is not None:
            body["assessment_method"] = assessment_method
        if total_exchanges is not None:
            body["total_exchanges"] = total_exchanges

        data = await self._http.put(
            f"/api/v1/agents/{agent_id}/personality", json_data=body
        )
        return PersonalityUpdateResponse.model_validate(data)

    async def batch_get(self, agent_ids: list[str]) -> BatchPersonalityResponse:
        """Get personality profiles for multiple agents at once."""
        body = encode_body(BatchGetPersonalitiesInputBody, {"agent_ids": agent_ids})
        return BatchPersonalityResponse.model_validate(
            await self._http.post("/api/v1/agents/personalities/batch", json_data=body)
        )

    async def get_significant_moments(
        self, agent_id: str, *, limit: int | None = None
    ) -> SignificantMomentsResponse:
        """Get significant moments for an agent's personality evolution."""
        params: dict[str, str] = {}
        if limit is not None:
            params["limit"] = str(limit)
        return SignificantMomentsResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/personality/significant-moments", params=params)
        )

    async def get_recent_shifts(self, agent_id: str) -> RecentShiftsResponse:
        """Get recent personality shifts for an agent."""
        return RecentShiftsResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/personality/recent-shifts")
        )

    async def list_user_overlays(self, agent_id: str) -> UserOverlaysListResponse:
        """List all user-specific personality overlays for an agent."""
        return UserOverlaysListResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/personality/users")
        )

    async def get_user_overlay(
        self,
        agent_id: str,
        user_id: str,
        *,
        instance_id: str | None = None,
        since: str | None = None,
    ) -> UserOverlayDetailResponse:
        """Get a specific user's personality overlay for an agent."""
        params: dict[str, str] = {}
        if instance_id is not None:
            params["instance_id"] = instance_id
        if since is not None:
            params["since"] = since
        return UserOverlayDetailResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/personality/users/{user_id}", params=params)
        )
