"""Tests for async session-end polling in the Sonzai SDK.

Covers the 202 → status-poll loop path introduced for the NATS-backed
async session-end pipeline. When the server responds with a
``processing_id`` the SDK must poll ``/sessions/end/status/{pid}`` with
exponential backoff until state transitions to ``done`` or ``failed``.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai, SonzaiError


@pytest.fixture
def base_url() -> str:
    return "https://api.test.sonz.ai"


@pytest.fixture
def client(base_url):
    c = Sonzai(api_key="test-key", base_url=base_url)
    yield c
    c.close()


class TestSyncSessionEndPolling:
    @respx.mock
    def test_legacy_200_passes_through(self, client, base_url):
        """When the server returns the classic 200 {success:true}, the SDK
        must not attempt to poll — that's the pre-async path."""
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/end").mock(
            return_value=httpx.Response(200, json={"success": True, "async": True})
        )
        resp = client.agents.sessions.end(
            "a1", user_id="u1", session_id="s1", total_messages=0
        )
        assert resp.success is True

    @respx.mock
    def test_202_polls_until_done(self, client, base_url):
        """202 with processing_id → poll; first /status hit is 'processing',
        second is 'done'. Assert both requests fired and the caller got a
        successful SessionResponse."""
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/end").mock(
            return_value=httpx.Response(
                202,
                json={
                    "success": True,
                    "async": True,
                    "processing_id": "11111111-1111-1111-1111-111111111111",
                    "status_url": "/api/v1/sessions/end/status/11111111-1111-1111-1111-111111111111",
                    "session_id": "s1",
                    "agent_id": "a1",
                    "enqueued_at": "2026-04-24T10:00:00Z",
                },
            )
        )
        status_route = respx.get(
            f"{base_url}/api/v1/sessions/end/status/11111111-1111-1111-1111-111111111111"
        ).mock(
            side_effect=[
                httpx.Response(
                    200,
                    json={
                        "state": "processing",
                        "enqueued_at": "2026-04-24T10:00:00Z",
                        "session_id": "s1",
                        "agent_id": "a1",
                    },
                ),
                httpx.Response(
                    200,
                    json={
                        "state": "done",
                        "enqueued_at": "2026-04-24T10:00:00Z",
                        "started_at": "2026-04-24T10:00:05Z",
                        "finished_at": "2026-04-24T10:00:42Z",
                        "session_id": "s1",
                        "agent_id": "a1",
                    },
                ),
            ]
        )

        resp = client.agents.sessions.end(
            "a1", user_id="u1", session_id="s1", total_messages=0
        )
        assert resp.success is True
        assert status_route.call_count == 2

    @respx.mock
    def test_202_then_failed_raises(self, client, base_url):
        """202 → failed status must surface a SonzaiError with the reason."""
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/end").mock(
            return_value=httpx.Response(
                202,
                json={
                    "success": True,
                    "async": True,
                    "processing_id": "22222222-2222-2222-2222-222222222222",
                    "status_url": "/api/v1/sessions/end/status/22222222-2222-2222-2222-222222222222",
                    "session_id": "s1",
                    "agent_id": "a1",
                    "enqueued_at": "2026-04-24T10:00:00Z",
                },
            )
        )
        respx.get(
            f"{base_url}/api/v1/sessions/end/status/22222222-2222-2222-2222-222222222222"
        ).mock(
            return_value=httpx.Response(
                200,
                json={
                    "state": "failed",
                    "enqueued_at": "2026-04-24T10:00:00Z",
                    "session_id": "s1",
                    "agent_id": "a1",
                    "error": "LLM upstream timeout",
                },
            )
        )
        with pytest.raises(SonzaiError, match="LLM upstream timeout"):
            client.agents.sessions.end(
                "a1", user_id="u1", session_id="s1", total_messages=0
            )

    @respx.mock
    def test_poll_timeout_raises(self, client, base_url):
        """A stuck status (always 'pending') must raise a timeout error
        bounded by poll_timeout rather than hang forever."""
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/end").mock(
            return_value=httpx.Response(
                202,
                json={
                    "success": True,
                    "async": True,
                    "processing_id": "33333333-3333-3333-3333-333333333333",
                    "status_url": "/api/v1/sessions/end/status/33333333-3333-3333-3333-333333333333",
                    "session_id": "s1",
                    "agent_id": "a1",
                    "enqueued_at": "2026-04-24T10:00:00Z",
                },
            )
        )
        respx.get(
            f"{base_url}/api/v1/sessions/end/status/33333333-3333-3333-3333-333333333333"
        ).mock(
            return_value=httpx.Response(
                200,
                json={
                    "state": "pending",
                    "enqueued_at": "2026-04-24T10:00:00Z",
                    "session_id": "s1",
                    "agent_id": "a1",
                },
            )
        )
        with pytest.raises(SonzaiError, match="timed out"):
            client.agents.sessions.end(
                "a1",
                user_id="u1",
                session_id="s1",
                total_messages=0,
                poll_timeout=0.2,
            )


class TestAsyncSessionEndPolling:
    @pytest.mark.asyncio
    @respx.mock
    async def test_202_polls_until_done(self, base_url):
        respx.post(f"{base_url}/api/v1/agents/a1/sessions/end").mock(
            return_value=httpx.Response(
                202,
                json={
                    "success": True,
                    "async": True,
                    "processing_id": "44444444-4444-4444-4444-444444444444",
                    "status_url": "/api/v1/sessions/end/status/44444444-4444-4444-4444-444444444444",
                    "session_id": "s1",
                    "agent_id": "a1",
                    "enqueued_at": "2026-04-24T10:00:00Z",
                },
            )
        )
        respx.get(
            f"{base_url}/api/v1/sessions/end/status/44444444-4444-4444-4444-444444444444"
        ).mock(
            side_effect=[
                httpx.Response(
                    200,
                    json={
                        "state": "processing",
                        "enqueued_at": "2026-04-24T10:00:00Z",
                        "session_id": "s1",
                        "agent_id": "a1",
                    },
                ),
                httpx.Response(
                    200,
                    json={
                        "state": "done",
                        "enqueued_at": "2026-04-24T10:00:00Z",
                        "session_id": "s1",
                        "agent_id": "a1",
                    },
                ),
            ]
        )

        async with AsyncSonzai(api_key="test-key", base_url=base_url) as client:
            resp = await client.agents.sessions.end(  # type: ignore[attr-defined]
                "a1", user_id="u1", session_id="s1", total_messages=0
            )
            assert resp.success is True
