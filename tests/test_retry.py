"""Unit tests for RetryPolicy decision logic."""

from __future__ import annotations

import pytest
from httpx import ConnectError

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
