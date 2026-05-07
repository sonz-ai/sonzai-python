"""Hand-written Session/AsyncSession handles for the real-time turn loop.

A ``Session`` bundles the identity tuple ``(agent_id, user_id, session_id,
instance_id)`` plus session-level ``provider``/``model`` defaults so the
caller doesn't have to repeat them on every method:

    session = client.agents.sessions.start(
        agent_id="...",
        user_id="...",
        session_id="...",
        provider="gemini",
        model="gemini-3.1-flash-lite-preview",
        tool_definitions=[...],
    )
    ctx = session.context(query=user_message)
    result = session.turn(
        messages=[...],
        fetch_next_context={"query": next_user_message},
    )
    session.end()

Methods are thin wrappers over the underlying ``Sessions`` resource and
the platform's ``GET /context`` and ``POST /turn`` endpoints. Per-call
``provider``/``model`` arguments override the session defaults; if
neither is supplied, the server-side resolver picks a default model.

Backward compat: ``success`` is exposed as a property mirroring the
``StartSessionOutputBody`` returned by the server, so existing
``client.agents.sessions.start(...).success`` callers keep working
without code changes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from sonzai._generated.models import TurnRequestBody, TurnResponseBody, TurnStatusOutputBody
from sonzai._request_helpers import encode_body

if TYPE_CHECKING:
    from sonzai.resources.sessions import AsyncSessions, Sessions
    from sonzai.types import ChatMessage, SessionResponse


class _SessionBase:
    """Shared init / state for sync + async session handles."""

    def __init__(
        self,
        *,
        agent_id: str,
        user_id: str,
        session_id: str,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        user_display_name: str | None = None,
        user_timezone: str | None = None,
        start_response: SessionResponse | None = None,
    ) -> None:
        self.agent_id = agent_id
        self.user_id = user_id
        self.session_id = session_id
        self.instance_id = instance_id
        self.provider = provider
        self.model = model
        self.user_display_name = user_display_name
        self.user_timezone = user_timezone
        # Cached server response from /sessions/start so callers that
        # used the pre-handle return shape (e.g. `.success`) still work.
        self._start_response = start_response

    @property
    def success(self) -> bool:
        """Mirror of the ``/sessions/start`` response body — kept so
        callers doing ``result = sessions.start(...); result.success``
        continue to work after we changed the return type to Session.
        """
        if self._start_response is None:
            return True
        return bool(getattr(self._start_response, "success", False))

    def _resolve_provider_model(
        self, provider: str | None, model: str | None
    ) -> tuple[str | None, str | None]:
        """Per-call provider/model wins over session defaults; ``None``
        falls through to the server-side resolver."""
        return (
            provider if provider is not None else self.provider,
            model if model is not None else self.model,
        )


class Session(_SessionBase):
    """Synchronous session handle.

    Created by :meth:`sonzai.resources.sessions.Sessions.start`. Wraps the
    sync ``Sessions`` resource for the real-time loop methods.
    """

    def __init__(
        self,
        sessions: Sessions,
        *,
        agent_id: str,
        user_id: str,
        session_id: str,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        user_display_name: str | None = None,
        user_timezone: str | None = None,
        start_response: SessionResponse | None = None,
    ) -> None:
        super().__init__(
            agent_id=agent_id,
            user_id=user_id,
            session_id=session_id,
            instance_id=instance_id,
            provider=provider,
            model=model,
            user_display_name=user_display_name,
            user_timezone=user_timezone,
            start_response=start_response,
        )
        self._sessions = sessions
        self._http = sessions._http

    def context(
        self,
        *,
        query: str | None = None,
        language: str | None = None,
        timezone: str | None = None,
    ) -> Any:
        """Fetch the enriched agent context for this session.

        Thin wrapper over ``GET /api/v1/agents/{agentId}/context``.
        Returns the raw JSON payload (matches the generated
        ``Context.get_context`` shape — server response is intentionally
        free-form so client renderers stay forward-compatible).
        """
        params: dict[str, Any] = {
            "userId": self.user_id,
            "sessionId": self.session_id,
        }
        if self.instance_id is not None:
            params["instanceId"] = self.instance_id
        if query is not None:
            params["query"] = query
        if language is not None:
            params["language"] = language
        if timezone is not None:
            params["timezone"] = timezone
        path = f"/api/v1/agents/{quote(self.agent_id, safe='')}/context"
        return self._http.get(path, params=params)

    def turn(
        self,
        *,
        messages: list[Any],
        fetch_next_context: dict[str, Any] | None = None,
        provider: str | None = None,
        model: str | None = None,
        user_display_name: str | None = None,
        user_timezone: str | None = None,
    ) -> TurnResponseBody:
        """Submit a conversation turn and (optionally) fetch the next
        enriched context in the same request.

        ``provider``/``model`` here override the session-level defaults.
        Pass ``fetch_next_context={"query": ...}`` to have the server
        return an enriched context (same shape as ``GET /context``)
        under ``next_context`` so the next user message can render
        without a second round-trip.
        """
        prov, mdl = self._resolve_provider_model(provider, model)
        raw: dict[str, Any] = {
            "userId": self.user_id,
            "messages": messages,
        }
        if self.instance_id is not None:
            raw["instanceId"] = self.instance_id
        if fetch_next_context is not None:
            raw["fetchNextContext"] = fetch_next_context
        if prov is not None:
            raw["provider"] = prov
        if mdl is not None:
            raw["model"] = mdl
        display = user_display_name if user_display_name is not None else self.user_display_name
        if display is not None:
            raw["userDisplayName"] = display
        tz = user_timezone if user_timezone is not None else self.user_timezone
        if tz is not None:
            raw["userTimezone"] = tz

        body = encode_body(TurnRequestBody, raw)
        path = (
            f"/api/v1/agents/{quote(self.agent_id, safe='')}"
            f"/sessions/{quote(self.session_id, safe='')}/turn"
        )
        data = self._http.post(path, json_data=body)
        return TurnResponseBody.model_validate(data)

    def status(self, extraction_id: str) -> TurnStatusOutputBody:
        """Poll the deferred-extraction state for a previously-submitted turn.

        Thin wrapper over ``GET /api/v1/agents/{agentId}/turns/{extractionId}/status``,
        scoped to this session's ``agent_id``. Mirrors TS ``session.status()``
        and Go ``Session.TurnStatus``.
        """
        path = (
            f"/api/v1/agents/{quote(self.agent_id, safe='')}"
            f"/turns/{quote(extraction_id, safe='')}/status"
        )
        data = self._http.get(path)
        return TurnStatusOutputBody.model_validate(data)

    def end(
        self,
        *,
        total_messages: int = 0,
        duration_seconds: int = 0,
        messages: list[ChatMessage | dict[str, str]] | None = None,
        wait: bool = False,
        provider: str | None = None,
        model: str | None = None,
        user_display_name: str | None = None,
        user_timezone: str | None = None,
        poll_timeout: float | None = None,
    ) -> SessionResponse:
        """End the session and (optionally) wait for the CE pipeline.

        Delegates to :meth:`Sessions.end`, threading the session's
        identity + ``provider``/``model`` defaults. Per-call args
        override the session defaults.
        """
        prov, mdl = self._resolve_provider_model(provider, model)
        kwargs: dict[str, Any] = {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "total_messages": total_messages,
            "duration_seconds": duration_seconds,
            "wait": wait,
        }
        if self.instance_id is not None:
            kwargs["instance_id"] = self.instance_id
        if messages is not None:
            kwargs["messages"] = messages
        display = user_display_name if user_display_name is not None else self.user_display_name
        if display is not None:
            kwargs["user_display_name"] = display
        tz = user_timezone if user_timezone is not None else self.user_timezone
        if tz is not None:
            kwargs["user_timezone"] = tz
        if poll_timeout is not None:
            kwargs["poll_timeout"] = poll_timeout
        if prov is not None:
            kwargs["provider"] = prov
        if mdl is not None:
            kwargs["model"] = mdl
        return self._sessions.end(self.agent_id, **kwargs)


class AsyncSession(_SessionBase):
    """Asynchronous session handle. Mirrors :class:`Session`."""

    def __init__(
        self,
        sessions: AsyncSessions,
        *,
        agent_id: str,
        user_id: str,
        session_id: str,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        user_display_name: str | None = None,
        user_timezone: str | None = None,
        start_response: SessionResponse | None = None,
    ) -> None:
        super().__init__(
            agent_id=agent_id,
            user_id=user_id,
            session_id=session_id,
            instance_id=instance_id,
            provider=provider,
            model=model,
            user_display_name=user_display_name,
            user_timezone=user_timezone,
            start_response=start_response,
        )
        self._sessions = sessions
        self._http = sessions._http

    async def context(
        self,
        *,
        query: str | None = None,
        language: str | None = None,
        timezone: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {
            "userId": self.user_id,
            "sessionId": self.session_id,
        }
        if self.instance_id is not None:
            params["instanceId"] = self.instance_id
        if query is not None:
            params["query"] = query
        if language is not None:
            params["language"] = language
        if timezone is not None:
            params["timezone"] = timezone
        path = f"/api/v1/agents/{quote(self.agent_id, safe='')}/context"
        return await self._http.get(path, params=params)

    async def turn(
        self,
        *,
        messages: list[Any],
        fetch_next_context: dict[str, Any] | None = None,
        provider: str | None = None,
        model: str | None = None,
        user_display_name: str | None = None,
        user_timezone: str | None = None,
    ) -> TurnResponseBody:
        prov, mdl = self._resolve_provider_model(provider, model)
        raw: dict[str, Any] = {
            "userId": self.user_id,
            "messages": messages,
        }
        if self.instance_id is not None:
            raw["instanceId"] = self.instance_id
        if fetch_next_context is not None:
            raw["fetchNextContext"] = fetch_next_context
        if prov is not None:
            raw["provider"] = prov
        if mdl is not None:
            raw["model"] = mdl
        display = user_display_name if user_display_name is not None else self.user_display_name
        if display is not None:
            raw["userDisplayName"] = display
        tz = user_timezone if user_timezone is not None else self.user_timezone
        if tz is not None:
            raw["userTimezone"] = tz

        body = encode_body(TurnRequestBody, raw)
        path = (
            f"/api/v1/agents/{quote(self.agent_id, safe='')}"
            f"/sessions/{quote(self.session_id, safe='')}/turn"
        )
        data = await self._http.post(path, json_data=body)
        return TurnResponseBody.model_validate(data)

    async def status(self, extraction_id: str) -> TurnStatusOutputBody:
        """Poll the deferred-extraction state for a previously-submitted turn.

        Thin wrapper over ``GET /api/v1/agents/{agentId}/turns/{extractionId}/status``,
        scoped to this session's ``agent_id``. Mirrors TS ``session.status()``
        and Go ``Session.TurnStatus``.
        """
        path = (
            f"/api/v1/agents/{quote(self.agent_id, safe='')}"
            f"/turns/{quote(extraction_id, safe='')}/status"
        )
        data = await self._http.get(path)
        return TurnStatusOutputBody.model_validate(data)

    async def end(
        self,
        *,
        total_messages: int = 0,
        duration_seconds: int = 0,
        messages: list[ChatMessage | dict[str, str]] | None = None,
        wait: bool = False,
        provider: str | None = None,
        model: str | None = None,
        user_display_name: str | None = None,
        user_timezone: str | None = None,
        poll_timeout: float | None = None,
    ) -> SessionResponse:
        prov, mdl = self._resolve_provider_model(provider, model)
        kwargs: dict[str, Any] = {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "total_messages": total_messages,
            "duration_seconds": duration_seconds,
            "wait": wait,
        }
        if self.instance_id is not None:
            kwargs["instance_id"] = self.instance_id
        if messages is not None:
            kwargs["messages"] = messages
        display = user_display_name if user_display_name is not None else self.user_display_name
        if display is not None:
            kwargs["user_display_name"] = display
        tz = user_timezone if user_timezone is not None else self.user_timezone
        if tz is not None:
            kwargs["user_timezone"] = tz
        if poll_timeout is not None:
            kwargs["poll_timeout"] = poll_timeout
        if prov is not None:
            kwargs["provider"] = prov
        if mdl is not None:
            kwargs["model"] = mdl
        return await self._sessions.end(self.agent_id, **kwargs)
