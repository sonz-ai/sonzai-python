"""Tests for omnichannel conversations resource."""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import (
    CONVERSATION_MESSAGE,
    CONVERSATION_MESSAGE_FAILED,
    CONVERSATION_STARTED,
    CONVERSATION_TAKEOVER_RELEASED,
    CONVERSATION_TAKEOVER_STARTED,
    CONVERSATION_UNROUTED,
    AsyncSonzai,
    Sonzai,
)
from sonzai.resources.conversations import AsyncConversations, Conversations


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


CONVERSATION_ROW = {
    "agent": "agent-1",
    "agent_name": "Luna",
    "channel": "whatsapp",
    "cost_usd": 0.01,
    "created_at": "2026-07-01T00:00:00Z",
    "handoffs": [],
    "id": "conv-1",
    "last_activity": "2026-07-01T00:01:00Z",
    "last_message": "Hi",
    "model": "gemini",
    "status": "open",
    "tags": [],
    "tier": "durable",
    "title": "WhatsApp chat",
}

CONVERSATION_DTO = {
    "agent_id": "agent-1",
    "channel_type": "whatsapp",
    "connection_id": "conn-1",
    "controller": "agent",
    "controller_operator_id": None,
    "conversation_id": "conv-1",
    "created_at": "2026-07-01T00:00:00Z",
    "handoffs": [],
    "last_direction": "inbound",
    "last_message_at": "2026-07-01T00:01:00Z",
    "last_message_preview": "Hi",
    "meta": {},
    "project_id": "proj-1",
    "session_id": "session-1",
    "status": "open",
    "takeover_started_at": None,
    "unread_count": 1,
    "updated_at": "2026-07-01T00:01:00Z",
    "user_id": "user-1",
}

MESSAGE = {
    "attachments": None,
    "author_id": "agent-1",
    "author_type": "agent",
    "channel_message_id": "wamid-1",
    "content": "Hi",
    "conversation_id": "conv-1",
    "created_at": "2026-07-01T00:01:00Z",
    "delivery_detail": None,
    "delivery_status": "sent",
    "direction": "outbound",
    "message_id": "msg-1",
    "role": "assistant",
    "session_id": "session-1",
}


def test_client_exposes_conversations(client: Sonzai, async_client: AsyncSonzai) -> None:
    assert isinstance(client.conversations, Conversations)
    assert isinstance(async_client.conversations, AsyncConversations)
    assert hasattr(client.conversations, "list_conversations")


@respx.mock
def test_list_uses_filters_and_cursor(client: Sonzai, base_url: str) -> None:
    route = respx.get(f"{base_url}/api/v1/conversations").mock(
        return_value=httpx.Response(
            200,
            json={
                "conversations": [CONVERSATION_ROW],
                "items": [CONVERSATION_ROW],
                "has_more": False,
                "next_cursor": None,
                "total": 1,
            },
        )
    )

    page = client.conversations.list(
        project_id="proj-1",
        channel="whatsapp",
        agent_id="agent-1",
        user_id="user-1",
        controller="agent",
        status="open",
        q="alex",
        cursor="cur-1",
        limit=25,
    )
    items = page.first_page()

    request = route.calls.last.request
    assert request.method == "GET"
    assert request.url.params["project_id"] == "proj-1"
    assert request.url.params["channel"] == "whatsapp"
    assert request.url.params["agent_id"] == "agent-1"
    assert request.url.params["user_id"] == "user-1"
    assert request.url.params["controller"] == "agent"
    assert request.url.params["status"] == "open"
    assert request.url.params["q"] == "alex"
    assert request.url.params["cursor"] == "cur-1"
    assert request.url.params["limit"] == "25"
    assert items[0].id == "conv-1"


@respx.mock
def test_get_and_messages(client: Sonzai, base_url: str) -> None:
    get_route = respx.get(f"{base_url}/api/v1/conversations/conv-1").mock(
        return_value=httpx.Response(
            200, json={"conversation": CONVERSATION_DTO, "source": "durable"}
        )
    )
    messages_route = respx.get(f"{base_url}/api/v1/conversations/conv-1/messages").mock(
        return_value=httpx.Response(
            200,
            json={
                "items": [MESSAGE],
                "messages": [MESSAGE],
                "has_more": False,
                "next_cursor": None,
            },
        )
    )

    detail = client.conversations.get("conv-1")
    messages = client.conversations.messages("conv-1", cursor="msg-cur", limit=10).first_page()

    assert get_route.calls.last.request.method == "GET"
    assert detail.conversation.conversation_id == "conv-1"
    assert messages_route.calls.last.request.url.params["cursor"] == "msg-cur"
    assert messages_route.calls.last.request.url.params["limit"] == "10"
    assert messages[0].message_id == "msg-1"


@respx.mock
def test_mutating_methods(client: Sonzai, base_url: str) -> None:
    takeover = respx.post(f"{base_url}/api/v1/conversations/conv-1/takeover").mock(
        return_value=httpx.Response(200, json={**CONVERSATION_DTO, "controller": "human"})
    )
    release = respx.delete(f"{base_url}/api/v1/conversations/conv-1/takeover").mock(
        return_value=httpx.Response(200, json=CONVERSATION_DTO)
    )
    send = respx.post(f"{base_url}/api/v1/conversations/conv-1/messages").mock(
        return_value=httpx.Response(200, json=CONVERSATION_DTO)
    )
    read = respx.post(f"{base_url}/api/v1/conversations/conv-1/read").mock(
        return_value=httpx.Response(200, json={**CONVERSATION_DTO, "unread_count": 0})
    )
    update = respx.patch(f"{base_url}/api/v1/conversations/conv-1").mock(
        return_value=httpx.Response(200, json={**CONVERSATION_DTO, "status": "closed"})
    )

    client.conversations.take_over("conv-1", operator_id="op-1", force=True)
    client.conversations.release("conv-1")
    client.conversations.send_as_agent(
        "conv-1", content="Hello", attachments=[{"type": "image", "url": "https://x.test/a.png"}]
    )
    client.conversations.mark_read("conv-1")
    client.conversations.update("conv-1", agent_id="agent-2", status="closed")

    assert takeover.calls.last.request.url.params["operator_id"] == "op-1"
    assert takeover.calls.last.request.url.params["force"] == "true"
    assert release.calls.last.request.method == "DELETE"
    assert json.loads(send.calls.last.request.content) == {
        "content": "Hello",
        "attachments": [{"type": "image", "url": "https://x.test/a.png"}],
    }
    assert read.calls.last.request.method == "POST"
    assert json.loads(update.calls.last.request.content) == {
        "agent_id": "agent-2",
        "status": "closed",
    }


@respx.mock
def test_stream(client: Sonzai, base_url: str) -> None:
    body = 'data: {"type":"conversation.message","conversation_id":"conv-1"}\n\ndata: [DONE]\n\n'
    route = respx.get(f"{base_url}/api/v1/conversations/stream").mock(
        return_value=httpx.Response(
            200, content=body, headers={"content-type": "text/event-stream"}
        )
    )

    events = list(client.conversations.stream(project_id="proj-1"))

    assert route.calls.last.request.url.params["project_id"] == "proj-1"
    assert events == [{"type": "conversation.message", "conversation_id": "conv-1"}]


@respx.mock
async def test_async_list(async_client: AsyncSonzai, base_url: str) -> None:
    route = respx.get(f"{base_url}/api/v1/conversations").mock(
        return_value=httpx.Response(
            200,
            json={
                "conversations": [CONVERSATION_ROW],
                "items": [CONVERSATION_ROW],
                "has_more": False,
                "next_cursor": None,
                "total": 1,
            },
        )
    )
    try:
        page = await async_client.conversations.list(project_id="proj-1")
        items = await page.first_page()
        assert route.calls.last.request.method == "GET"
        assert items[0].id == "conv-1"
    finally:
        await async_client.close()


def test_webhook_event_constants() -> None:
    assert CONVERSATION_STARTED == "conversation.started"
    assert CONVERSATION_MESSAGE == "conversation.message"
    assert CONVERSATION_TAKEOVER_STARTED == "conversation.takeover.started"
    assert CONVERSATION_TAKEOVER_RELEASED == "conversation.takeover.released"
    assert CONVERSATION_MESSAGE_FAILED == "conversation.message.failed"
    assert CONVERSATION_UNROUTED == "conversation.unrouted"
