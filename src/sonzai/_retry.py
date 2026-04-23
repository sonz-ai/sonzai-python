"""Retry policy for SDK HTTP requests.

The `_http.py` request loop calls `policy.should_retry(...)` after each
response (or network error) and `policy.backoff_seconds(...)` before
sleeping. Defaults are tuned for "be resilient but not abusive" against
the production API.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

import httpx

DEFAULT_RETRY_STATUSES = frozenset({408, 429, 500, 502, 503, 504})
NETWORK_EXCEPTION_TYPES = (
    httpx.ConnectError,
    httpx.ReadTimeout,
    httpx.ConnectTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.ReadError,
)


@dataclass(frozen=True)
class RetryPolicy:
    """Config for HTTP request retries.

    Usage:
        Sonzai(api_key=..., retry=RetryPolicy(max_attempts=5))

    Or disable retries entirely:
        Sonzai(api_key=..., retry=RetryPolicy.none())
    """

    max_attempts: int = 3
    backoff_factor: float = 0.3
    backoff_max: float = 30.0
    backoff_jitter: float = 0.1
    retry_on_statuses: frozenset[int] = field(default_factory=lambda: DEFAULT_RETRY_STATUSES)
    retry_on_network: bool = True
    respect_retry_after: bool = True

    @classmethod
    def none(cls) -> "RetryPolicy":
        return cls(max_attempts=1)

    def should_retry(
        self, *, attempt: int, status: int | None, exc: Exception | None
    ) -> bool:
        if attempt >= self.max_attempts:
            return False
        if status is not None:
            return status in self.retry_on_statuses
        if exc is not None and self.retry_on_network:
            return isinstance(exc, NETWORK_EXCEPTION_TYPES)
        return False

    def backoff_seconds(
        self, *, attempt: int, retry_after_header: str | None
    ) -> float:
        if self.respect_retry_after and retry_after_header:
            try:
                return min(float(retry_after_header), self.backoff_max)
            except (TypeError, ValueError):
                pass
        base = self.backoff_factor * (2 ** (attempt - 1))
        base = min(base, self.backoff_max)
        if self.backoff_jitter > 0:
            jitter = random.uniform(-self.backoff_jitter, self.backoff_jitter) * base
            return max(0.0, base + jitter)
        return base
