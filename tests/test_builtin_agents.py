"""Tests for the Sonzai Built-in Agents resource.

Covers:

- Catalog listing parses into :class:`BuiltinAgentListResponse`.
- ``invoke`` sends ``{input, title}`` with ``?stream=false``, applies the
  15-minute per-request timeout, and parses :class:`BuiltinAgentInvokeResult`.
- ``invoke_stream`` consumes the named-event SSE envelope (``event: update``
  frames + terminal ``event: result``) and yields typed items; a terminal
  ``event: error`` raises :class:`StreamError`.
- Session CRUD + message turns (blocking and streaming).
- The named-event SSE parser itself, against a synthetic stream.
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai, StreamError
from sonzai._http import _parse_named_sse_stream
from sonzai.types import (
    BuiltinAgentChatTurnResult,
    BuiltinAgentInvokeResult,
    BuiltinAgentListResponse,
    BuiltinAgentSession,
    BuiltinAgentSessionListResponse,
    BuiltinAgentUpdate,
)


@pytest.fixture
def base_url() -> str:
    return "https://api.test.sonz.ai"


@pytest.fixture
def client(base_url: str) -> Sonzai:
    c = Sonzai(api_key="test-key", base_url=base_url)
    yield c
    c.close()


@pytest.fixture
def async_client(base_url: str) -> AsyncSonzai:
    return AsyncSonzai(api_key="test-key", base_url=base_url)


CATALOG_RESPONSE = {
    "agents": [
        {
            "slug": "lead_research",
            "name": "Lead Research",
            "description": "Deep-dive research on a single lead.",
            "model": "deep-work-v1",
            "provisioned": True,
        },
        {
            "slug": "market_intel",
            "name": "Market Intel",
            "description": "Market landscape and competitor intelligence.",
            "model": "deep-work-v1",
            "provisioned": False,
        },
    ]
}

INVOKE_RESULT = {
    "findings": "# Findings\n\nAyala Land is expanding office leasing.",
    "summary": "Expansion signals in office leasing.",
    "session_id": "ses-1",
    "model": "deep-work-v1",
    "byok": False,
    "usage": {
        "input_tokens": 1200,
        "output_tokens": 800,
        "cache_creation_input_tokens": 100,
        "cache_read_input_tokens": 50,
    },
    "running_seconds": 73.4,
    "cost_usd": 0.42,
}

SESSION = {
    "id": "ses-1",
    "agent": "lead_research",
    "model": "deep-work-v1",
    "status": "active",
    "title": "Ayala Land",
    "byok": False,
    "cost_usd": 0.0,
    "created_at": "2026-06-10T01:02:03Z",
}

CHAT_TURN_RESULT = {
    "reply": "Here is what I found.",
    "findings": "# Turn findings",
    "usage": {"input_tokens": 10, "output_tokens": 20},
    "turn_cost_usd": 0.01,
    "running_seconds": 4.2,
}


def _sse(events: list[tuple[str, dict]]) -> str:
    """Build a named-event SSE body from (event_name, payload) pairs."""
    return "".join(
        f"event: {name}\ndata: {json.dumps(payload, separators=(',', ':'))}\n\n"
        for name, payload in events
    )


STREAM_BODY = _sse(
    [
        ("update", {"type": "tool_use", "tool": "web_search", "elapsed": 1.5}),
        ("update", {"type": "text", "text": "Scanning filings...", "elapsed": 9.0}),
        ("result", INVOKE_RESULT),
    ]
)

ERROR_STREAM_BODY = _sse(
    [
        ("update", {"type": "tool_use", "tool": "web_search"}),
        ("error", {"error": "agent run failed: budget exceeded"}),
    ]
)


# ---------------------------------------------------------------------------
# Named-event SSE parser — synthetic stream
# ---------------------------------------------------------------------------


class TestParseNamedSSEStream:
    def test_named_events_paired_with_payloads(self) -> None:
        lines = [
            "event: update",
            'data: {"type":"tool_use","tool":"web_search"}',
            "",
            "event: result",
            'data: {"summary":"done"}',
            "",
        ]
        items = list(_parse_named_sse_stream(iter(lines)))
        assert items == [
            ("update", {"type": "tool_use", "tool": "web_search"}),
            ("result", {"summary": "done"}),
        ]

    def test_default_event_name_is_message(self) -> None:
        items = list(_parse_named_sse_stream(iter(['data: {"x":1}', ""])))
        assert items == [("message", {"x": 1})]

    def test_event_name_resets_after_dispatch(self) -> None:
        lines = [
            "event: update",
            'data: {"a":1}',
            "",
            'data: {"b":2}',  # no event: line — must NOT inherit "update"
            "",
        ]
        items = list(_parse_named_sse_stream(iter(lines)))
        assert items == [("update", {"a": 1}), ("message", {"b": 2})]

    def test_done_terminates_stream(self) -> None:
        lines = ['data: {"a":1}', "", "data: [DONE]", 'data: {"b":2}', ""]
        items = list(_parse_named_sse_stream(iter(lines)))
        assert items == [("message", {"a": 1})]

    def test_malformed_json_and_comments_skipped(self) -> None:
        lines = [
            ": keepalive",
            "event: update",
            "data: {not json",
            'data: {"ok":true}',
            "",
        ]
        items = list(_parse_named_sse_stream(iter(lines)))
        # The malformed line is dropped but does not consume the event name.
        assert items == [("update", {"ok": True})]


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------


class TestList:
    @respx.mock
    def test_list_catalog(self, client: Sonzai, base_url: str) -> None:
        respx.get(f"{base_url}/api/v1/builtin-agents").mock(
            return_value=httpx.Response(200, json=CATALOG_RESPONSE)
        )

        resp = client.builtin_agents.list()

        assert isinstance(resp, BuiltinAgentListResponse)
        assert [a.slug for a in resp.agents] == ["lead_research", "market_intel"]
        assert resp.agents[0].provisioned is True
        assert resp.agents[1].provisioned is False

    @respx.mock
    async def test_list_catalog_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        respx.get(f"{base_url}/api/v1/builtin-agents").mock(
            return_value=httpx.Response(200, json=CATALOG_RESPONSE)
        )
        try:
            resp = await async_client.builtin_agents.list()
            assert isinstance(resp, BuiltinAgentListResponse)
            assert len(resp.agents) == 2
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# Invoke (non-streaming)
# ---------------------------------------------------------------------------


class TestInvoke:
    @respx.mock
    def test_invoke_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/builtin-agents/lead_research/invoke").mock(
            return_value=httpx.Response(200, json=INVOKE_RESULT)
        )

        result = client.builtin_agents.invoke(
            "lead_research",
            input={"company": "Ayala Land"},
            title="Ayala Land deep dive",
        )

        assert route.called
        request = route.calls.last.request
        assert request.url.params["stream"] == "false"
        sent = json.loads(request.content)
        assert sent == {"input": {"company": "Ayala Land"}, "title": "Ayala Land deep dive"}

        assert isinstance(result, BuiltinAgentInvokeResult)
        assert result.summary == "Expansion signals in office leasing."
        assert result.session_id == "ses-1"
        assert result.usage is not None
        assert result.usage.input_tokens == 1200
        assert result.usage.cache_read_input_tokens == 50
        assert result.cost_usd == 0.42

    @respx.mock
    def test_invoke_title_omitted_when_none(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/builtin-agents/lead_score/invoke").mock(
            return_value=httpx.Response(200, json=INVOKE_RESULT)
        )

        client.builtin_agents.invoke("lead_score", input={"lead_id": "l-1"})

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"input": {"lead_id": "l-1"}}

    @respx.mock
    def test_invoke_uses_long_read_timeout(self, client: Sonzai, base_url: str) -> None:
        """Deep-work runs take minutes — the default per-request timeout is 15 min."""
        route = respx.post(f"{base_url}/api/v1/builtin-agents/lead_research/invoke").mock(
            return_value=httpx.Response(200, json=INVOKE_RESULT)
        )

        client.builtin_agents.invoke("lead_research", input={})

        timeout = route.calls.last.request.extensions["timeout"]
        assert timeout["read"] == 900.0
        assert timeout["connect"] == 10.0

    @respx.mock
    async def test_invoke_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/builtin-agents/market_intel/invoke").mock(
            return_value=httpx.Response(200, json=INVOKE_RESULT)
        )
        try:
            result = await async_client.builtin_agents.invoke(
                "market_intel", input={"market": "Makati CBD"}
            )
            assert isinstance(result, BuiltinAgentInvokeResult)
            assert route.calls.last.request.url.params["stream"] == "false"
            assert route.calls.last.request.extensions["timeout"]["read"] == 900.0
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# Invoke (streaming)
# ---------------------------------------------------------------------------


class TestInvokeStream:
    @respx.mock
    def test_stream_yields_updates_then_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/builtin-agents/lead_research/invoke").mock(
            return_value=httpx.Response(
                200,
                content=STREAM_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )

        items = list(
            client.builtin_agents.invoke_stream("lead_research", input={"company": "Ayala Land"})
        )

        assert route.calls.last.request.url.params["stream"] == "true"
        assert json.loads(route.calls.last.request.content) == {
            "input": {"company": "Ayala Land"}
        }

        assert len(items) == 3
        assert isinstance(items[0], BuiltinAgentUpdate)
        assert items[0].type == "tool_use"
        assert items[0].tool == "web_search"
        assert items[0].elapsed == 1.5
        assert isinstance(items[1], BuiltinAgentUpdate)
        assert items[1].text == "Scanning filings..."
        # Final item is the typed terminal result.
        assert isinstance(items[2], BuiltinAgentInvokeResult)
        assert items[2].summary == "Expansion signals in office leasing."

    @respx.mock
    def test_stream_error_event_raises(self, client: Sonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/builtin-agents/lead_research/invoke").mock(
            return_value=httpx.Response(
                200,
                content=ERROR_STREAM_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = client.builtin_agents.invoke_stream("lead_research", input={})
        first = next(stream)
        assert isinstance(first, BuiltinAgentUpdate)
        with pytest.raises(StreamError, match="budget exceeded"):
            next(stream)

    @respx.mock
    async def test_stream_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/builtin-agents/lead_research/invoke").mock(
            return_value=httpx.Response(
                200,
                content=STREAM_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )
        try:
            items = [
                item
                async for item in async_client.builtin_agents.invoke_stream(
                    "lead_research", input={}
                )
            ]
            assert len(items) == 3
            assert isinstance(items[0], BuiltinAgentUpdate)
            assert isinstance(items[-1], BuiltinAgentInvokeResult)
        finally:
            await async_client.close()

    @respx.mock
    async def test_stream_async_error_event_raises(
        self, async_client: AsyncSonzai, base_url: str
    ) -> None:
        respx.post(f"{base_url}/api/v1/builtin-agents/lead_research/invoke").mock(
            return_value=httpx.Response(
                200,
                content=ERROR_STREAM_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )
        try:
            with pytest.raises(StreamError, match="budget exceeded"):
                async for _ in async_client.builtin_agents.invoke_stream("lead_research", input={}):
                    pass
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------


class TestSessions:
    @respx.mock
    def test_create(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/builtin-agents/sessions").mock(
            return_value=httpx.Response(200, json=SESSION)
        )

        session = client.builtin_agents.sessions.create(
            agent="lead_research", title="Ayala Land"
        )

        sent = json.loads(route.calls.last.request.content)
        assert sent == {"agent": "lead_research", "title": "Ayala Land"}
        assert isinstance(session, BuiltinAgentSession)
        assert session.id == "ses-1"
        assert session.status == "active"

    @respx.mock
    def test_create_title_omitted_when_none(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/builtin-agents/sessions").mock(
            return_value=httpx.Response(200, json=SESSION)
        )

        client.builtin_agents.sessions.create(agent="lead_research")

        assert json.loads(route.calls.last.request.content) == {"agent": "lead_research"}

    @respx.mock
    def test_list_with_limit(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(f"{base_url}/api/v1/builtin-agents/sessions").mock(
            return_value=httpx.Response(200, json={"sessions": [SESSION]})
        )

        resp = client.builtin_agents.sessions.list(limit=5)

        assert route.calls.last.request.url.params["limit"] == "5"
        assert isinstance(resp, BuiltinAgentSessionListResponse)
        assert resp.sessions[0].agent == "lead_research"

    @respx.mock
    def test_get_includes_billed_tokens(self, client: Sonzai, base_url: str) -> None:
        detail = {
            **SESSION,
            "billed_input_tokens": 1200,
            "billed_output_tokens": 800,
            "billed_cache_read_tokens": 50,
            "billed_cache_creation_tokens": 100,
        }
        respx.get(f"{base_url}/api/v1/builtin-agents/sessions/ses-1").mock(
            return_value=httpx.Response(200, json=detail)
        )

        session = client.builtin_agents.sessions.get("ses-1")

        assert session.billed_input_tokens == 1200
        assert session.billed_cache_creation_tokens == 100

    @respx.mock
    def test_send_blocking(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/sessions/ses-1/messages"
        ).mock(return_value=httpx.Response(200, json=CHAT_TURN_RESULT))

        result = client.builtin_agents.sessions.send("ses-1", "Score this lead.")

        request = route.calls.last.request
        assert request.url.params["stream"] == "false"
        assert json.loads(request.content) == {"text": "Score this lead."}
        assert request.extensions["timeout"]["read"] == 900.0

        assert isinstance(result, BuiltinAgentChatTurnResult)
        assert result.reply == "Here is what I found."
        assert result.turn_cost_usd == 0.01

    @respx.mock
    def test_send_streaming(self, client: Sonzai, base_url: str) -> None:
        body = _sse(
            [
                ("update", {"type": "text", "text": "thinking", "elapsed": 0.5}),
                ("result", CHAT_TURN_RESULT),
            ]
        )
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/sessions/ses-1/messages"
        ).mock(
            return_value=httpx.Response(
                200, content=body, headers={"content-type": "text/event-stream"}
            )
        )

        items = list(client.builtin_agents.sessions.send("ses-1", "Hi", stream=True))

        assert route.calls.last.request.url.params["stream"] == "true"
        assert len(items) == 2
        assert isinstance(items[0], BuiltinAgentUpdate)
        assert isinstance(items[1], BuiltinAgentChatTurnResult)
        assert items[1].reply == "Here is what I found."

    @respx.mock
    def test_send_stream_sync(self, client: Sonzai, base_url: str) -> None:
        """The public sync ``send_stream`` mirrors the async ``send_stream``."""
        body = _sse(
            [
                ("update", {"type": "text", "text": "thinking", "elapsed": 0.5}),
                ("result", CHAT_TURN_RESULT),
            ]
        )
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/sessions/ses-1/messages"
        ).mock(
            return_value=httpx.Response(
                200, content=body, headers={"content-type": "text/event-stream"}
            )
        )

        items = list(client.builtin_agents.sessions.send_stream("ses-1", "Hi"))

        request = route.calls.last.request
        assert request.method == "POST"
        assert request.url.params["stream"] == "true"
        assert json.loads(request.content) == {"text": "Hi"}
        assert len(items) == 2
        assert isinstance(items[0], BuiltinAgentUpdate)
        assert isinstance(items[1], BuiltinAgentChatTurnResult)
        assert items[1].reply == "Here is what I found."

    @respx.mock
    def test_send_stream_sync_raises_on_error_frame(
        self, client: Sonzai, base_url: str
    ) -> None:
        body = _sse(
            [
                ("update", {"type": "tool_use", "tool": "web_search"}),
                ("error", {"error": "turn failed: budget exceeded"}),
            ]
        )
        respx.post(f"{base_url}/api/v1/builtin-agents/sessions/ses-1/messages").mock(
            return_value=httpx.Response(
                200, content=body, headers={"content-type": "text/event-stream"}
            )
        )

        with pytest.raises(StreamError, match="budget exceeded"):
            list(client.builtin_agents.sessions.send_stream("ses-1", "Hi"))

    @respx.mock
    async def test_session_flow_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/builtin-agents/sessions").mock(
            return_value=httpx.Response(200, json=SESSION)
        )
        respx.get(f"{base_url}/api/v1/builtin-agents/sessions").mock(
            return_value=httpx.Response(200, json={"sessions": [SESSION]})
        )
        respx.get(f"{base_url}/api/v1/builtin-agents/sessions/ses-1").mock(
            return_value=httpx.Response(200, json=SESSION)
        )
        send_route = respx.post(
            f"{base_url}/api/v1/builtin-agents/sessions/ses-1/messages"
        ).mock(return_value=httpx.Response(200, json=CHAT_TURN_RESULT))
        try:
            session = await async_client.builtin_agents.sessions.create(agent="lead_research")
            assert session.id == "ses-1"

            listed = await async_client.builtin_agents.sessions.list(limit=3)
            assert len(listed.sessions) == 1

            fetched = await async_client.builtin_agents.sessions.get("ses-1")
            assert fetched.agent == "lead_research"

            result = await async_client.builtin_agents.sessions.send("ses-1", "Hello")
            assert isinstance(result, BuiltinAgentChatTurnResult)
            assert send_route.calls.last.request.url.params["stream"] == "false"
        finally:
            await async_client.close()

    @respx.mock
    async def test_send_stream_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        body = _sse(
            [
                ("update", {"type": "text", "text": "thinking"}),
                ("result", CHAT_TURN_RESULT),
            ]
        )
        respx.post(f"{base_url}/api/v1/builtin-agents/sessions/ses-1/messages").mock(
            return_value=httpx.Response(
                200, content=body, headers={"content-type": "text/event-stream"}
            )
        )
        try:
            items = [
                item
                async for item in async_client.builtin_agents.sessions.send_stream("ses-1", "Hi")
            ]
            assert len(items) == 2
            assert isinstance(items[0], BuiltinAgentUpdate)
            assert isinstance(items[1], BuiltinAgentChatTurnResult)
        finally:
            await async_client.close()
