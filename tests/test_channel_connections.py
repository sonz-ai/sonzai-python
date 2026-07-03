"""Tests for Meta channel connections resource."""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai
from sonzai.resources.channel_connections import AsyncChannelConnections, ChannelConnections


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


CONNECTION = {
    "app_id": "app-1",
    "channel_type": "whatsapp",
    "connection_id": "conn-1",
    "created_at": "2026-07-01T00:00:00Z",
    "default_agent_id": "agent-1",
    "display_name": "Support WhatsApp",
    "ig_account_id": None,
    "page_id": None,
    "phone_number_id": "phone-1",
    "project_id": "proj-1",
    "provider_mode": "byo_app",
    "status": "active",
    "status_detail": None,
    "templates": {"hello": "world"},
    "test_send_succeeded": None,
    "updated_at": "2026-07-01T00:00:00Z",
    "verify_token": "raw-secret",
    "waba_id": "waba-1",
    "webhook_callback_url": "https://api.sonz.ai/webhooks/meta/proj-1/conn-1",
}


def test_client_exposes_channel_connections(client: Sonzai, async_client: AsyncSonzai) -> None:
    assert isinstance(client.channel_connections, ChannelConnections)
    assert isinstance(async_client.channel_connections, AsyncChannelConnections)
    assert hasattr(client.channel_connections, "create_channel_connection")


@respx.mock
def test_list_returns_redacted_connections(client: Sonzai, base_url: str) -> None:
    route = respx.get(f"{base_url}/api/v1/projects/proj-1/channel-connections").mock(
        return_value=httpx.Response(
            200,
            json={
                "connections": [{**CONNECTION, "app_secret": "secret", "access_token": "token"}],
                "items": [],
            },
        )
    )

    result = client.channel_connections.list("proj-1")

    assert route.calls.last.request.method == "GET"
    assert len(result) == 1
    assert result[0].connection_id == "conn-1"
    assert result[0].verify_token == "redacted"
    assert not hasattr(result[0], "app_secret")
    assert not hasattr(result[0], "access_token")


@respx.mock
def test_create_sends_byo_fields_and_redacts_response(client: Sonzai, base_url: str) -> None:
    route = respx.post(f"{base_url}/api/v1/projects/proj-1/channel-connections").mock(
        return_value=httpx.Response(
            200,
            json={**CONNECTION, "app_secret": "secret", "access_token": "token"},
        )
    )

    result = client.channel_connections.create(
        "proj-1",
        channel_type="whatsapp",
        provider_mode="byo_app",
        app_id="app-1",
        app_secret="secret",
        phone_number_id="phone-1",
        waba_id="waba-1",
        access_token="token",
        verify_token="verify-secret",
        display_name="Support WhatsApp",
        default_agent_id="agent-1",
    )

    sent = json.loads(route.calls.last.request.content)
    assert sent == {
        "channel_type": "whatsapp",
        "provider_mode": "byo_app",
        "app_id": "app-1",
        "app_secret": "secret",
        "phone_number_id": "phone-1",
        "waba_id": "waba-1",
        "access_token": "token",
        "verify_token": "verify-secret",
        "display_name": "Support WhatsApp",
        "default_agent_id": "agent-1",
    }
    assert result.connection_id == "conn-1"
    assert result.verify_token == "redacted"


@respx.mock
def test_get_update_delete_and_test(client: Sonzai, base_url: str) -> None:
    get_route = respx.get(f"{base_url}/api/v1/projects/proj-1/channel-connections/conn-1").mock(
        return_value=httpx.Response(200, json=CONNECTION)
    )
    update_route = respx.patch(
        f"{base_url}/api/v1/projects/proj-1/channel-connections/conn-1"
    ).mock(return_value=httpx.Response(200, json={**CONNECTION, "status": "disabled"}))
    delete_route = respx.delete(
        f"{base_url}/api/v1/projects/proj-1/channel-connections/conn-1"
    ).mock(return_value=httpx.Response(204))
    test_route = respx.post(
        f"{base_url}/api/v1/projects/proj-1/channel-connections/conn-1/test"
    ).mock(return_value=httpx.Response(200, json={**CONNECTION, "test_send_succeeded": True}))

    got = client.channel_connections.get("proj-1", "conn-1")
    updated = client.channel_connections.update(
        "proj-1",
        "conn-1",
        default_agent_id="agent-2",
        status="disabled",
        templates={"welcome": "template"},
    )
    deleted = client.channel_connections.delete("proj-1", "conn-1")
    tested = client.channel_connections.test(
        "proj-1",
        "conn-1",
        to="+15551234567",
        message="hello",
    )

    assert get_route.calls.last.request.method == "GET"
    assert got.connection_id == "conn-1"
    assert json.loads(update_route.calls.last.request.content) == {
        "default_agent_id": "agent-2",
        "status": "disabled",
        "templates": {"welcome": "template"},
    }
    assert updated.status == "disabled"
    assert delete_route.calls.last.request.method == "DELETE"
    assert deleted is None
    assert json.loads(test_route.calls.last.request.content) == {
        "to": "+15551234567",
        "message": "hello",
    }
    assert tested.test_send_succeeded is True


@respx.mock
async def test_async_create(async_client: AsyncSonzai, base_url: str) -> None:
    route = respx.post(f"{base_url}/api/v1/projects/proj-1/channel-connections").mock(
        return_value=httpx.Response(200, json=CONNECTION)
    )
    try:
        result = await async_client.channel_connections.create(
            "proj-1",
            channel_type="instagram",
            provider_mode="embedded_signup",
            code="oauth-code",
            ig_account_id="ig-1",
            display_name="Instagram",
        )
        sent = json.loads(route.calls.last.request.content)
        assert sent == {
            "channel_type": "instagram",
            "provider_mode": "embedded_signup",
            "code": "oauth-code",
            "ig_account_id": "ig-1",
            "display_name": "Instagram",
        }
        assert result.connection_id == "conn-1"
    finally:
        await async_client.close()
