"""Session resource for the Sonzai SDK."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from .._generated.models import EndSessionInputBody, StartSessionInputBody
from .._generated.resources.sessions import AsyncSessions as _GenAsyncSessions
from .._generated.resources.sessions import Sessions as _GenSessions
from .._exceptions import SonzaiError
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body
from ..types import ChatMessage, SessionResponse

# Polling tunables for the async session-end path. The server's status
# entry has a 1h TTL so overall_timeout=900s (15m) leaves generous
# headroom for a stalled OnSessionEnd call while still surfacing a clear
# error to the caller when the pipeline is truly wedged.
_SESSION_END_POLL_INITIAL_INTERVAL = 0.5  # seconds
_SESSION_END_POLL_MAX_INTERVAL = 5.0  # seconds
_SESSION_END_POLL_BACKOFF = 1.5
_SESSION_END_OVERALL_TIMEOUT = 900.0


def _next_poll_interval(previous: float) -> float:
    """Exponential backoff capped at _SESSION_END_POLL_MAX_INTERVAL."""
    return min(previous * _SESSION_END_POLL_BACKOFF, _SESSION_END_POLL_MAX_INTERVAL)


class Sessions(_GenSessions):
    """Hand-written overrides / convenience helpers on top of generated Sessions.

    All hand-written methods remain as overrides preserving the historical SDK
    contract. The subclass inheritance makes future spec additions appear as
    inherited methods automatically.
    """

    # TODO(B.3-followup): __init__ takes HTTPClient (typed); generated _SessionsBase
    # takes Any. Override kept to preserve typed constructor signature.
    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def start(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str,
        instance_id: str | None = None,
        user_display_name: str | None = None,
        tool_definitions: list[dict[str, Any]] | None = None,
    ) -> SessionResponse:
        """Start a chat session."""
        raw: dict[str, Any] = {
            "user_id": user_id,
            "session_id": session_id,
        }
        if instance_id:
            raw["instance_id"] = instance_id
        if user_display_name:
            raw["user_display_name"] = user_display_name
        if tool_definitions:
            raw["tool_definitions"] = tool_definitions
        body = encode_body(StartSessionInputBody, raw)

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
        wait: bool = False,
        user_display_name: str | None = None,
        user_timezone: str | None = None,
        poll_timeout: float = _SESSION_END_OVERALL_TIMEOUT,
    ) -> SessionResponse:
        """End a chat session.

        Passing ``wait=True`` runs the CE pipeline synchronously on the
        server — use this in benchmarks and tests that query memory right
        after. When the server is configured with
        ``ENABLE_ASYNC_SESSION_END=true`` it returns 202 with a
        ``processing_id`` instead; this method polls ``/status/{pid}``
        until completion so the caller-visible behaviour stays
        "call returns when the pipeline is done".
        """
        raw: dict[str, Any] = {
            "user_id": user_id,
            "session_id": session_id,
            "total_messages": total_messages,
            "duration_seconds": duration_seconds,
        }
        if instance_id:
            raw["instance_id"] = instance_id
        if messages:
            raw["messages"] = [
                m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
            ]
        if wait:
            raw["wait"] = True
        if user_display_name is not None:
            raw["user_display_name"] = user_display_name
        if user_timezone is not None:
            raw["user_timezone"] = user_timezone
        body = encode_body(EndSessionInputBody, raw)

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/sessions/end", json_data=body
        )
        if isinstance(data, dict) and data.get("processing_id"):
            data = self._poll_processing_status(
                data["processing_id"], overall_timeout=poll_timeout
            )
        return SessionResponse.model_validate(data)

    def _poll_processing_status(
        self, processing_id: str, *, overall_timeout: float
    ) -> dict[str, Any]:
        """Poll the status endpoint until the pipeline reaches a terminal state.

        Raises SonzaiError on timeout or when the server reports
        ``state=failed``. Returns the terminal status payload on success —
        callers treat the overall result as SessionResponse-compatible.
        """
        deadline = time.monotonic() + overall_timeout
        interval = _SESSION_END_POLL_INITIAL_INTERVAL
        last_state: str | None = None
        while True:
            status = self._http.get(
                f"/api/v1/sessions/end/status/{processing_id}"
            )
            if not isinstance(status, dict):
                raise SonzaiError(
                    f"unexpected status payload shape: {type(status)!r}"
                )
            state = status.get("state")
            last_state = state
            if state == "done":
                # Promote to the SessionResponse shape the caller expects.
                return {"success": True, "async": True, **status}
            if state == "failed":
                raise SonzaiError(
                    f"session end failed: {status.get('error', 'unknown')}"
                )
            if time.monotonic() >= deadline:
                raise SonzaiError(
                    f"session end poll timed out after {overall_timeout:.0f}s "
                    f"(last state: {last_state})"
                )
            time.sleep(interval)
            interval = _next_poll_interval(interval)

    def set_tools(
        self, agent_id: str, session_id: str, tools: list[dict[str, Any]]
    ) -> SessionResponse:
        """Set the tools available for a session."""
        data = self._http.put(
            f"/api/v1/agents/{agent_id}/sessions/{session_id}/tools", json_data=tools
        )
        return SessionResponse.model_validate(data)


class AsyncSessions(_GenAsyncSessions):
    """Async hand-written overrides on top of generated AsyncSessions."""

    # TODO(B.3-followup): __init__ takes AsyncHTTPClient (typed); generated base
    # takes Any. Override kept to preserve typed constructor signature.
    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def start(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str,
        instance_id: str | None = None,
        user_display_name: str | None = None,
        tool_definitions: list[dict[str, Any]] | None = None,
    ) -> SessionResponse:
        raw: dict[str, Any] = {
            "user_id": user_id,
            "session_id": session_id,
        }
        if instance_id:
            raw["instance_id"] = instance_id
        if user_display_name:
            raw["user_display_name"] = user_display_name
        if tool_definitions:
            raw["tool_definitions"] = tool_definitions
        body = encode_body(StartSessionInputBody, raw)

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
        wait: bool = False,
        user_display_name: str | None = None,
        user_timezone: str | None = None,
        poll_timeout: float = _SESSION_END_OVERALL_TIMEOUT,
    ) -> SessionResponse:
        """End a session and optionally wait for the CE pipeline.

        By default the server runs fact extraction + summary + side-effects
        asynchronously and responds immediately. Pass ``wait=True`` to run
        the pipeline synchronously — use this in benchmarks and test
        harnesses that query memory or start another session right after.

        When the server is configured with
        ``ENABLE_ASYNC_SESSION_END=true`` it returns 202 with a
        ``processing_id``; this method polls ``/status/{pid}`` until
        the pipeline reaches a terminal state so callers see the same
        blocking-call shape they always did.
        """
        raw: dict[str, Any] = {
            "user_id": user_id,
            "session_id": session_id,
            "total_messages": total_messages,
            "duration_seconds": duration_seconds,
        }
        if instance_id:
            raw["instance_id"] = instance_id
        if messages:
            raw["messages"] = [
                m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
            ]
        if wait:
            raw["wait"] = True
        if user_display_name is not None:
            raw["user_display_name"] = user_display_name
        if user_timezone is not None:
            raw["user_timezone"] = user_timezone
        body = encode_body(EndSessionInputBody, raw)

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/sessions/end", json_data=body
        )
        if isinstance(data, dict) and data.get("processing_id"):
            data = await self._poll_processing_status(
                data["processing_id"], overall_timeout=poll_timeout
            )
        return SessionResponse.model_validate(data)

    async def _poll_processing_status(
        self, processing_id: str, *, overall_timeout: float
    ) -> dict[str, Any]:
        """Async variant of Sessions._poll_processing_status."""
        loop = asyncio.get_event_loop()
        deadline = loop.time() + overall_timeout
        interval = _SESSION_END_POLL_INITIAL_INTERVAL
        last_state: str | None = None
        while True:
            status = await self._http.get(
                f"/api/v1/sessions/end/status/{processing_id}"
            )
            if not isinstance(status, dict):
                raise SonzaiError(
                    f"unexpected status payload shape: {type(status)!r}"
                )
            state = status.get("state")
            last_state = state
            if state == "done":
                return {"success": True, "async": True, **status}
            if state == "failed":
                raise SonzaiError(
                    f"session end failed: {status.get('error', 'unknown')}"
                )
            if loop.time() >= deadline:
                raise SonzaiError(
                    f"session end poll timed out after {overall_timeout:.0f}s "
                    f"(last state: {last_state})"
                )
            await asyncio.sleep(interval)
            interval = _next_poll_interval(interval)

    async def set_tools(
        self, agent_id: str, session_id: str, tools: list[dict[str, Any]]
    ) -> SessionResponse:
        """Set the tools available for a session."""
        data = await self._http.put(
            f"/api/v1/agents/{agent_id}/sessions/{session_id}/tools", json_data=tools
        )
        return SessionResponse.model_validate(data)
