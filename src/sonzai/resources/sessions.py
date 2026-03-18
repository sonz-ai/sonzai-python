"""Session resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import ChatMessage, SessionResponse


class Sessions:
    """Sync session lifecycle operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def start(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str,
        instance_id: str | None = None,
    ) -> SessionResponse:
        """Start a chat session."""
        body: dict[str, Any] = {
            "user_id": user_id,
            "session_id": session_id,
        }
        if instance_id:
            body["instance_id"] = instance_id

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/sessions/start", json_data=body
        )
        return SessionResponse.model_validate(data)

    def end(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str,
        instance_id: str | None = None,
        total_messages: int = 0,
        duration_seconds: int = 0,
        messages: list[ChatMessage | dict[str, str]] | None = None,
    ) -> SessionResponse:
        """End a chat session."""
        body: dict[str, Any] = {
            "user_id": user_id,
            "session_id": session_id,
            "total_messages": total_messages,
            "duration_seconds": duration_seconds,
        }
        if instance_id:
            body["instance_id"] = instance_id
        if messages:
            body["messages"] = [
                m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
            ]

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/sessions/end", json_data=body
        )
        return SessionResponse.model_validate(data)

    def set_tools(
        self, agent_id: str, session_id: str, tools: list[dict[str, Any]]
    ) -> SessionResponse:
        """Set the tools available for a session."""
        data = self._http.put(
            f"/api/v1/agents/{agent_id}/sessions/{session_id}/tools", json_data=tools
        )
        return SessionResponse.model_validate(data)


class AsyncSessions:
    """Async session lifecycle operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def start(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str,
        instance_id: str | None = None,
    ) -> SessionResponse:
        body: dict[str, Any] = {
            "user_id": user_id,
            "session_id": session_id,
        }
        if instance_id:
            body["instance_id"] = instance_id

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/sessions/start", json_data=body
        )
        return SessionResponse.model_validate(data)

    async def end(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str,
        instance_id: str | None = None,
        total_messages: int = 0,
        duration_seconds: int = 0,
        messages: list[ChatMessage | dict[str, str]] | None = None,
    ) -> SessionResponse:
        body: dict[str, Any] = {
            "user_id": user_id,
            "session_id": session_id,
            "total_messages": total_messages,
            "duration_seconds": duration_seconds,
        }
        if instance_id:
            body["instance_id"] = instance_id
        if messages:
            body["messages"] = [
                m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
            ]

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/sessions/end", json_data=body
        )
        return SessionResponse.model_validate(data)

    async def set_tools(
        self, agent_id: str, session_id: str, tools: list[dict[str, Any]]
    ) -> SessionResponse:
        """Set the tools available for a session."""
        data = await self._http.put(
            f"/api/v1/agents/{agent_id}/sessions/{session_id}/tools", json_data=tools
        )
        return SessionResponse.model_validate(data)
