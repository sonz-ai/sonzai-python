"""Personality resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import PersonalityResponse, PersonalityUpdateResponse


class Personality:
    """Sync personality operations for an agent."""

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
        body: dict[str, Any] = {"big5": big5}
        if assessment_method is not None:
            body["assessment_method"] = assessment_method
        if total_exchanges is not None:
            body["total_exchanges"] = total_exchanges

        data = self._http.put(
            f"/api/v1/agents/{agent_id}/personality", json_data=body
        )
        return PersonalityUpdateResponse.model_validate(data)


class AsyncPersonality:
    """Async personality operations for an agent."""

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
        body: dict[str, Any] = {"big5": big5}
        if assessment_method is not None:
            body["assessment_method"] = assessment_method
        if total_exchanges is not None:
            body["total_exchanges"] = total_exchanges

        data = await self._http.put(
            f"/api/v1/agents/{agent_id}/personality", json_data=body
        )
        return PersonalityUpdateResponse.model_validate(data)
