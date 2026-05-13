"""Tests for the ``temperature`` chat option (sonzai-go parity).

Mirror of sonzai-go's chat_options_temperature_test.go. Verifies the
on-wire contract:

* ``temperature=None`` → field absent from the JSON payload (so the AI
  service applies its own default — required for OpenAI reasoning
  models, which reject any explicit temperature override).
* ``temperature=0.7`` → field present with the literal value.
* ``temperature=0.0`` → field present (pointer-vs-value distinction in
  Go; ``None``-vs-``0.0`` here). A caller asking for deterministic
  output must not be silently dropped.
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai


@pytest.fixture
def base_url() -> str:
    return "https://api.test.sonz.ai"


@pytest.fixture
def client(base_url: str):
    c = Sonzai(api_key="test-key", base_url=base_url)
    yield c
    c.close()


@pytest.fixture
def async_client(base_url: str):
    return AsyncSonzai(api_key="test-key", base_url=base_url)


# Minimal SSE body that closes immediately so the request lifecycle
# resolves and the captured body becomes inspectable.
_TERMINAL_SSE_BODY = (
    'data: {"choices":[{"delta":{"content":""},"finish_reason":"stop","index":0}]}\n\n'
    "data: [DONE]\n\n"
)


def _captured_json(route) -> dict:
    """Read the JSON payload off the last captured request on a respx route."""
    call = route.calls.last
    return json.loads(call.request.content.decode("utf-8"))


class TestChatTemperatureSync:
    @respx.mock
    def test_omitted_when_none(self, client, base_url):
        route = respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=_TERMINAL_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )
        client.agents.chat(
            "agent-1",
            messages=[{"role": "user", "content": "hi"}],
        )
        body = _captured_json(route)
        assert "temperature" not in body, (
            f"expected temperature key omitted when None, got {body}"
        )

    @respx.mock
    def test_present_when_set(self, client, base_url):
        route = respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=_TERMINAL_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )
        client.agents.chat(
            "agent-1",
            messages=[{"role": "user", "content": "hi"}],
            temperature=0.7,
        )
        body = _captured_json(route)
        assert body["temperature"] == 0.7

    @respx.mock
    def test_zero_preserved(self, client, base_url):
        """A caller asking for deterministic output (temperature=0.0)
        must not be silently dropped — None and 0.0 are different
        contracts.
        """
        route = respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=_TERMINAL_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )
        client.agents.chat(
            "agent-1",
            messages=[{"role": "user", "content": "hi"}],
            temperature=0.0,
        )
        body = _captured_json(route)
        assert "temperature" in body
        assert body["temperature"] == 0.0

    @respx.mock
    def test_one_for_reasoning_models(self, client, base_url):
        """Reasoning models (gpt-5 / o1-* / o3-*) require temperature=1.
        Verify the SDK lets a caller pass it through.
        """
        route = respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=_TERMINAL_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )
        client.agents.chat(
            "agent-1",
            messages=[{"role": "user", "content": "hi"}],
            model="gpt-5",
            temperature=1.0,
        )
        body = _captured_json(route)
        assert body["temperature"] == 1.0
        assert body["model"] == "gpt-5"


class TestChatAsyncQueueTemperature:
    """chat_async (queue endpoint) must respect the same temperature contract."""

    @respx.mock
    def test_omitted_when_none(self, client, base_url):
        route = respx.post(f"{base_url}/api/v1/agents/agent-1/chat/async").mock(
            return_value=httpx.Response(
                200,
                json={"processing_id": "pid-1", "status": "queued"},
            )
        )
        client.agents.chat_async(
            "agent-1",
            messages=[{"role": "user", "content": "hi"}],
        )
        body = _captured_json(route)
        assert "temperature" not in body

    @respx.mock
    def test_present_when_set(self, client, base_url):
        route = respx.post(f"{base_url}/api/v1/agents/agent-1/chat/async").mock(
            return_value=httpx.Response(
                200,
                json={"processing_id": "pid-1", "status": "queued"},
            )
        )
        client.agents.chat_async(
            "agent-1",
            messages=[{"role": "user", "content": "hi"}],
            temperature=0.3,
        )
        body = _captured_json(route)
        assert body["temperature"] == 0.3


class TestChatTemperatureAsync:
    @pytest.mark.asyncio
    @respx.mock
    async def test_async_omitted_when_none(self, async_client, base_url):
        route = respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=_TERMINAL_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )
        await async_client.agents.chat(
            "agent-1",
            messages=[{"role": "user", "content": "hi"}],
        )
        body = _captured_json(route)
        assert "temperature" not in body
        await async_client.close()

    @pytest.mark.asyncio
    @respx.mock
    async def test_async_present_when_set(self, async_client, base_url):
        route = respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=_TERMINAL_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )
        await async_client.agents.chat(
            "agent-1",
            messages=[{"role": "user", "content": "hi"}],
            temperature=0.5,
        )
        body = _captured_json(route)
        assert body["temperature"] == 0.5
        await async_client.close()
