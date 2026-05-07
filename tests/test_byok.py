"""Tests for the BYOK (Bring-Your-Own-Key) resource."""

from __future__ import annotations

import json

import httpx
import respx

from sonzai import Sonzai

_KEY_FIXTURE = {
    "provider": "openai",
    "api_key_prefix": "sk-abcd",
    "is_active": True,
    "health_status": "healthy",
    "last_health_error": None,
    "last_health_check_at": "2026-05-07T00:00:00Z",
    "last_used_at": "2026-05-07T00:00:00Z",
    "updated_at": "2026-05-07T00:00:00Z",
}


def test_byok_list_returns_keys() -> None:
    with respx.mock() as router:
        router.get("https://api.sonz.ai/api/v1/projects/p1/byok-keys").mock(
            return_value=httpx.Response(200, json={"keys": [_KEY_FIXTURE]})
        )
        client = Sonzai(api_key="test-key")
        result = client.byok.list("p1")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].provider == "openai"
        assert result[0].api_key_prefix == "sk-abcd"
        assert result[0].is_active is True
        assert result[0].health_status == "healthy"


def test_byok_set_sends_api_key() -> None:
    with respx.mock() as router:
        route = router.put(
            "https://api.sonz.ai/api/v1/projects/p1/byok-keys/openai"
        ).mock(return_value=httpx.Response(200, json=_KEY_FIXTURE))
        client = Sonzai(api_key="test-key")
        result = client.byok.set("p1", "openai", api_key="sk-secret-xyz")

        assert route.called
        sent_body = json.loads(route.calls.last.request.content)
        assert sent_body == {"api_key": "sk-secret-xyz"}
        assert result.provider == "openai"
        assert result.api_key_prefix == "sk-abcd"


def test_byok_delete_returns_none() -> None:
    with respx.mock() as router:
        route = router.delete(
            "https://api.sonz.ai/api/v1/projects/p1/byok-keys/openai"
        ).mock(return_value=httpx.Response(204))
        client = Sonzai(api_key="test-key")
        result = client.byok.delete("p1", "openai")

        assert route.called
        assert result is None


def test_byok_set_active_uses_patch() -> None:
    disabled = {**_KEY_FIXTURE, "is_active": False}
    with respx.mock() as router:
        route = router.patch(
            "https://api.sonz.ai/api/v1/projects/p1/byok-keys/openai"
        ).mock(return_value=httpx.Response(200, json=disabled))
        client = Sonzai(api_key="test-key")
        result = client.byok.set_active("p1", "openai", is_active=False)

        assert route.called
        sent_body = json.loads(route.calls.last.request.content)
        assert sent_body == {"is_active": False}
        assert result.is_active is False


def test_byok_test_endpoint() -> None:
    with respx.mock() as router:
        route = router.post(
            "https://api.sonz.ai/api/v1/projects/p1/byok-keys/openai/test"
        ).mock(return_value=httpx.Response(200, json=_KEY_FIXTURE))
        client = Sonzai(api_key="test-key")
        result = client.byok.test("p1", "openai")

        assert route.called
        assert result.provider == "openai"
        assert result.health_status == "healthy"
