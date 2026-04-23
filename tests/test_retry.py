"""Unit tests for RetryPolicy decision logic."""

from __future__ import annotations

import pytest
import httpx
import respx
from httpx import ConnectError

from sonzai import RateLimitError, Sonzai
from sonzai._retry import RetryPolicy


class TestRetryPolicyDecisions:
    def test_default_retries_on_429(self) -> None:
        p = RetryPolicy()
        assert p.should_retry(attempt=1, status=429, exc=None) is True
        assert p.should_retry(attempt=p.max_attempts, status=429, exc=None) is False

    def test_default_retries_on_503(self) -> None:
        p = RetryPolicy()
        assert p.should_retry(attempt=1, status=503, exc=None) is True

    def test_default_does_not_retry_on_400(self) -> None:
        p = RetryPolicy()
        assert p.should_retry(attempt=1, status=400, exc=None) is False

    def test_default_retries_on_network_error(self) -> None:
        p = RetryPolicy()
        assert p.should_retry(attempt=1, status=None, exc=ConnectError("x")) is True

    def test_none_policy_never_retries(self) -> None:
        p = RetryPolicy.none()
        assert p.max_attempts == 1
        assert p.should_retry(attempt=1, status=503, exc=None) is False


class TestBackoff:
    def test_exponential_growth(self) -> None:
        p = RetryPolicy(backoff_factor=0.3, backoff_max=30.0, backoff_jitter=0.0)
        assert p.backoff_seconds(attempt=1, retry_after_header=None) == 0.3
        assert p.backoff_seconds(attempt=2, retry_after_header=None) == 0.6
        assert p.backoff_seconds(attempt=3, retry_after_header=None) == 1.2

    def test_capped_at_max(self) -> None:
        p = RetryPolicy(backoff_factor=10.0, backoff_max=5.0, backoff_jitter=0.0)
        assert p.backoff_seconds(attempt=1, retry_after_header=None) == 5.0
        assert p.backoff_seconds(attempt=5, retry_after_header=None) == 5.0

    def test_respects_retry_after_seconds(self) -> None:
        p = RetryPolicy(respect_retry_after=True, backoff_factor=0.3, backoff_jitter=0.0)
        assert p.backoff_seconds(attempt=1, retry_after_header="15") == 15.0

    def test_ignores_retry_after_when_disabled(self) -> None:
        p = RetryPolicy(respect_retry_after=False, backoff_factor=0.3, backoff_jitter=0.0)
        assert p.backoff_seconds(attempt=1, retry_after_header="15") == 0.3

    def test_jitter_within_bounds(self) -> None:
        p = RetryPolicy(backoff_factor=1.0, backoff_max=10.0, backoff_jitter=0.5)
        for _ in range(20):
            s = p.backoff_seconds(attempt=1, retry_after_header=None)
            assert 0.5 <= s <= 1.5


class TestHTTPRetry:
    def test_retries_on_429_then_succeeds(self) -> None:
        with respx.mock() as router:
            route = router.get("https://api.sonz.ai/api/v1/projects")
            route.side_effect = [
                httpx.Response(429, headers={"Retry-After": "0"}, json={"message": "slow"}),
                httpx.Response(200, json={"projects": [], "total": 0}),
            ]
            client = Sonzai(api_key="test-key", retry=RetryPolicy(max_attempts=3, backoff_factor=0.001, backoff_jitter=0.0))
            client.projects.list()
            assert route.call_count == 2

    def test_exhausts_retries_and_raises(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/projects").mock(
                return_value=httpx.Response(503, json={"message": "down"})
            )
            client = Sonzai(api_key="test-key", retry=RetryPolicy(max_attempts=2, backoff_factor=0.001, backoff_jitter=0.0))
            with pytest.raises(Exception) as exc_info:
                client.projects.list()
            assert exc_info.value.status_code == 503   # type: ignore[attr-defined]

    def test_network_error_retry(self) -> None:
        with respx.mock() as router:
            route = router.get("https://api.sonz.ai/api/v1/projects")
            route.side_effect = [
                httpx.ConnectError("boom"),
                httpx.Response(200, json={"projects": [], "total": 0}),
            ]
            client = Sonzai(api_key="test-key", retry=RetryPolicy(max_attempts=3, backoff_factor=0.001, backoff_jitter=0.0))
            client.projects.list()
            assert route.call_count == 2

    def test_none_policy_raises_on_first_failure(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/projects").mock(
                return_value=httpx.Response(503, json={"message": "down"})
            )
            client = Sonzai(api_key="test-key", retry=RetryPolicy.none())
            with pytest.raises(Exception):
                client.projects.list()


class TestIdempotencyKey:
    def test_idempotency_key_injected_on_post(self) -> None:
        captured: list[httpx.Request] = []

        def capture(request: httpx.Request) -> httpx.Response:
            captured.append(request)
            return httpx.Response(200, json={"agent_id": "a1", "name": "X", "owner_user_id": "u1", "tenant_id": "t1", "instance_count": 1, "is_active": True, "created_at": "2026-01-01T00:00:00Z"})

        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/agents").mock(side_effect=capture)
            client = Sonzai(api_key="test-key")
            client.agents.create(name="x")
            assert "Idempotency-Key" in captured[0].headers
            assert len(captured[0].headers["Idempotency-Key"]) == 32

    def test_idempotency_key_consistent_across_retries(self) -> None:
        captured: list[str] = []

        def capture(request: httpx.Request) -> httpx.Response:
            captured.append(request.headers["Idempotency-Key"])
            if len(captured) == 1:
                return httpx.Response(503, json={"message": "down"})
            return httpx.Response(200, json={"agent_id": "a1", "name": "X", "owner_user_id": "u1", "tenant_id": "t1", "instance_count": 1, "is_active": True, "created_at": "2026-01-01T00:00:00Z"})

        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/agents").mock(side_effect=capture)
            client = Sonzai(api_key="test-key", retry=RetryPolicy(max_attempts=3, backoff_factor=0.001, backoff_jitter=0.0))
            client.agents.create(name="x")
            assert len(captured) == 2
            assert captured[0] == captured[1]

    def test_no_idempotency_key_on_get(self) -> None:
        captured: list[httpx.Request] = []

        def capture(request: httpx.Request) -> httpx.Response:
            captured.append(request)
            return httpx.Response(200, json={"projects": [], "total": 0})

        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/projects").mock(side_effect=capture)
            client = Sonzai(api_key="test-key")
            client.projects.list()
            assert "Idempotency-Key" not in captured[0].headers
