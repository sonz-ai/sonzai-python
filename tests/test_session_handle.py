"""Tests for the handwritten Session / AsyncSession handles.

The handle bundles agent_id / user_id / session_id (+ provider/model
defaults) returned by ``client.agents.sessions.start(...)`` so callers
drive the real-time loop with ``session.context() / .turn() / .end()``
without re-passing identity on every call.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from sonzai import AsyncSession, AsyncSonzai, Session, Sonzai


@pytest.fixture
def base_url() -> str:
    return "https://api.test.sonz.ai"


@pytest.fixture
def client(base_url):
    c = Sonzai(api_key="test-key", base_url=base_url)
    yield c
    c.close()


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------


class TestSessionStartReturnsHandle:
    @respx.mock
    def test_start_returns_session_handle(self, client, base_url):
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/start").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        result = client.agents.sessions.start(
            "a1",
            user_id="u1",
            session_id="s1",
            provider="gemini",
            model="gemini-3.1-flash-lite-preview",
        )

        assert isinstance(result, Session)
        # Backward compat — `.success` from the legacy SessionResponse.
        assert result.success is True
        # Identity + defaults captured on the handle.
        assert result.agent_id == "a1"
        assert result.user_id == "u1"
        assert result.session_id == "s1"
        assert result.provider == "gemini"
        assert result.model == "gemini-3.1-flash-lite-preview"


class TestSessionContext:
    @respx.mock
    def test_context_threads_session_identity(self, client, base_url):
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/start").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        ctx_route = respx.get(f"{base_url}/api/v1/agents/a1/context").mock(
            return_value=httpx.Response(200, json={"summary": "..."})
        )

        session = client.agents.sessions.start("a1", user_id="u1", session_id="s1")
        ctx = session.context(query="what did we discuss?")

        assert ctx == {"summary": "..."}
        # Identity flows from the handle — no re-passing required.
        req = ctx_route.calls[0].request
        assert req.url.params["userId"] == "u1"
        assert req.url.params["sessionId"] == "s1"
        assert req.url.params["query"] == "what did we discuss?"


class TestSessionTurn:
    @respx.mock
    def test_turn_uses_session_provider_model(self, client, base_url):
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/start").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        turn_route = respx.post(f"{base_url}/api/v1/agents/a1/sessions/s1/turn").mock(
            return_value=httpx.Response(
                200,
                json={
                    "extraction_id": "ext-1",
                    "extraction_status": "queued",
                    "success": True,
                },
            )
        )

        session = client.agents.sessions.start(
            "a1",
            user_id="u1",
            session_id="s1",
            provider="gemini",
            model="gemini-3.1-flash-lite-preview",
        )
        result = session.turn(
            messages=[{"role": "user", "content": "hi"}],
            fetch_next_context={"query": "next?"},
        )

        assert result.extraction_id == "ext-1"
        body = turn_route.calls[0].request.read()
        # Session-level provider/model flowed into the request.
        assert b'"provider":"gemini"' in body
        assert b'"model":"gemini-3.1-flash-lite-preview"' in body
        assert b'"fetchNextContext"' in body

    @respx.mock
    def test_per_call_provider_overrides_session_default(self, client, base_url):
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/start").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        turn_route = respx.post(f"{base_url}/api/v1/agents/a1/sessions/s1/turn").mock(
            return_value=httpx.Response(
                200,
                json={
                    "extraction_id": "ext-2",
                    "extraction_status": "queued",
                    "success": True,
                },
            )
        )

        session = client.agents.sessions.start(
            "a1",
            user_id="u1",
            session_id="s1",
            provider="gemini",
            model="gemini-3.1-flash-lite-preview",
        )
        session.turn(
            messages=[{"role": "user", "content": "hi"}],
            provider="anthropic",
            model="claude-opus-4-7",
        )

        body = turn_route.calls[0].request.read()
        # Per-call wins.
        assert b'"provider":"anthropic"' in body
        assert b'"model":"claude-opus-4-7"' in body
        assert b'"gemini"' not in body

    @respx.mock
    def test_no_provider_model_when_neither_set(self, client, base_url):
        """When neither session defaults nor per-call args are supplied,
        the wire body must omit provider/model so the server-side
        resolver picks the deployment default."""
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/start").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        turn_route = respx.post(f"{base_url}/api/v1/agents/a1/sessions/s1/turn").mock(
            return_value=httpx.Response(
                200,
                json={
                    "extraction_id": "ext-3",
                    "extraction_status": "queued",
                    "success": True,
                },
            )
        )

        session = client.agents.sessions.start("a1", user_id="u1", session_id="s1")
        session.turn(messages=[{"role": "user", "content": "hi"}])

        body = turn_route.calls[0].request.read()
        assert b'"provider"' not in body
        assert b'"model"' not in body


class TestSessionStatus:
    @respx.mock
    def test_status_threads_session_agent_id(self, client, base_url):
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/start").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        status_route = respx.get(
            f"{base_url}/api/v1/agents/a1/turns/ext-1/status"
        ).mock(
            return_value=httpx.Response(
                200,
                json={"extraction_id": "ext-1", "state": "done"},
            )
        )

        session = client.agents.sessions.start("a1", user_id="u1", session_id="s1")
        result = session.status("ext-1")

        assert status_route.called
        assert result.extraction_id == "ext-1"
        assert result.state == "done"


class TestSessionEnd:
    @respx.mock
    def test_end_threads_identity(self, client, base_url):
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/start").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        end_route = respx.post(f"{base_url}/api/v1/agents/a1/sessions/end").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        session = client.agents.sessions.start(
            "a1",
            user_id="u1",
            session_id="s1",
            provider="gemini",
            model="gemini-3.1-flash-lite-preview",
        )
        resp = session.end(total_messages=4, duration_seconds=42, wait=True)

        assert resp.success is True
        body = end_route.calls[0].request.read()
        assert b'"user_id":"u1"' in body
        assert b'"session_id":"s1"' in body
        # Session-default provider/model flow into /sessions/end.
        assert b'"provider":"gemini"' in body
        assert b'"model":"gemini-3.1-flash-lite-preview"' in body
        assert b'"wait":true' in body


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------


class TestAsyncSessionHandle:
    @pytest.mark.asyncio
    @respx.mock
    async def test_async_start_returns_handle_and_turn_works(self, base_url):
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/start").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/s1/turn").mock(
            return_value=httpx.Response(
                200,
                json={
                    "extraction_id": "ext-async",
                    "extraction_status": "queued",
                    "success": True,
                },
            )
        )

        async with AsyncSonzai(api_key="test-key", base_url=base_url) as client:
            session = await client.agents.sessions.start(  # type: ignore[attr-defined]
                "a1",
                user_id="u1",
                session_id="s1",
                provider="gemini",
            )
            assert isinstance(session, AsyncSession)
            assert session.success is True
            assert session.provider == "gemini"

            result = await session.turn(messages=[{"role": "user", "content": "hi"}])
            assert result.extraction_id == "ext-async"

    @pytest.mark.asyncio
    @respx.mock
    async def test_async_status_threads_session_agent_id(self, base_url):
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/start").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        status_route = respx.get(
            f"{base_url}/api/v1/agents/a1/turns/ext-async/status"
        ).mock(
            return_value=httpx.Response(
                200,
                json={"extraction_id": "ext-async", "state": "running"},
            )
        )

        async with AsyncSonzai(api_key="test-key", base_url=base_url) as client:
            session = await client.agents.sessions.start(  # type: ignore[attr-defined]
                "a1",
                user_id="u1",
                session_id="s1",
            )
            result = await session.status("ext-async")

        assert status_route.called
        assert result.extraction_id == "ext-async"
        assert result.state == "running"
