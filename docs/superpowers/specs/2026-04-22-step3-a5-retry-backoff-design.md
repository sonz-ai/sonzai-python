# Step 3 A.5: Retry, Backoff, and Idempotency Design

**Goal:** Make every SDK request resilient to transient failures out of the box. Today `_http.py` has a minimal max-retries counter with no backoff and no idempotency awareness; users with spotty networks or against a briefly-overloaded server see hard failures that would have succeeded on a second try.

**Architecture:** Pluggable retry policy objects passed to `Sonzai(...)` at construction time (or defaulted to a sensible baseline). The `_http.py` request layer consults the policy for each response: retry or raise. Idempotency keys are auto-generated for POST/PUT/PATCH requests so retries don't duplicate resources. `Retry-After` header on 429/503 is honored exactly.

**Tech Stack:** No new runtime deps. Uses existing `httpx` timeout handling, `uuid4` for idempotency keys, `time.sleep` / `asyncio.sleep` for backoff.

---

## Current state

`_http.py` has a primitive retry: `for _ in range(max_retries): ...` with no backoff, no status-code differentiation, no Retry-After awareness. Idempotency keys don't exist — retrying a POST that partially succeeded could create a duplicate.

Users on unstable networks today either catch + retry themselves (shouldn't have to) or see transient `httpx.ConnectError` bubble up.

## What users get

```python
# Defaults are sensible — most users won't configure anything:
client = Sonzai(api_key="...")

# But fine-grained control is there:
from sonzai import RetryPolicy

client = Sonzai(
    api_key="...",
    retry=RetryPolicy(
        max_attempts=5,
        backoff_factor=0.3,        # 0s, 0.3s, 0.6s, 1.2s, 2.4s
        backoff_max=30.0,
        retry_on_statuses={408, 429, 500, 502, 503, 504},
        retry_on_network=True,
        respect_retry_after=True,
    ),
)

# Disable retries entirely:
client = Sonzai(api_key="...", retry=RetryPolicy.none())

# Idempotency key override (advanced):
client.agents.chat(agent_id="x", messages=[...], idempotency_key="my-custom-key")
```

## Components

### `src/sonzai/_retry.py` (new)

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    backoff_factor: float = 0.3        # initial sleep = backoff_factor * 2^(attempt-1)
    backoff_max: float = 30.0
    backoff_jitter: float = 0.1        # randomness to prevent thundering herd
    retry_on_statuses: frozenset[int] = frozenset({408, 429, 500, 502, 503, 504})
    retry_on_network: bool = True      # httpx.ConnectError, ReadTimeout, etc.
    respect_retry_after: bool = True

    @classmethod
    def none(cls) -> "RetryPolicy":
        return cls(max_attempts=1)

    def should_retry(self, attempt: int, status: int | None, exc: Exception | None) -> bool: ...
    def backoff_seconds(self, attempt: int, retry_after_header: str | None) -> float: ...
```

`should_retry` centralizes the decision. `backoff_seconds` prefers `Retry-After` if the policy says to and the header is present; otherwise exponential + jitter.

### Idempotency keys

All state-mutating requests (POST, PUT, PATCH) carry `Idempotency-Key: <uuid4>` by default. If the server supports idempotency keys (server does), a retry with the same key returns the original response instead of creating a duplicate.

User-supplied keys via the `idempotency_key=` kwarg on any method override the default. For read-only methods (GET, DELETE without body), no key is sent.

### `_http.py` changes

Request loop becomes:
```python
attempt = 0
last_exc = None
while attempt < self._retry.max_attempts:
    attempt += 1
    try:
        response = self._client.request(method, url, ...)
        if response.is_success:
            return response.json() if response.content else None
        if self._retry.should_retry(attempt, response.status_code, None):
            delay = self._retry.backoff_seconds(attempt, response.headers.get("Retry-After"))
            time.sleep(delay)
            continue
        _raise_for_status(response)   # delegates to typed exceptions from A.1
    except (httpx.ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout) as e:
        last_exc = e
        if self._retry.should_retry(attempt, None, e):
            delay = self._retry.backoff_seconds(attempt, None)
            time.sleep(delay)
            continue
        raise
raise last_exc if last_exc else APIError(0, "retries exhausted")
```

Async mirror identical with `await asyncio.sleep(...)`.

### Observability

Every retry emits a structured log line (via stdlib `logging`):
```
WARNING sonzai.retry: attempt=2/3 status=429 retry_after=1.2s url=/api/v1/agents/x/chat
```

Users can opt in to more granular tracing by installing a logging handler on `sonzai.retry`. No OTel integration in this pass (would be a later A.6).

## Idempotency-key generation

`uuid4().hex` per request. Persisted to the `Idempotency-Key` header on mutating methods. The key is generated at HTTP-layer entry, so the SAME key is used across all retry attempts of one request (that's the whole point — server dedupes).

## Backwards compat

- Default policy means users who don't configure anything get retries for free. Net positive.
- One edge case: users who WERE manually retrying around the SDK may now see their fallback code never fire. Harmless — just surprising. Callout in release notes.
- `Sonzai(api_key="x", max_retries=5)` (existing kwarg) continues to work as a convenience: if set, it tunes `RetryPolicy.max_attempts`.

## Testing

`tests/test_retry.py` (new):
- Stub httpx to return `429` with `Retry-After: 2` → assert sleep, assert re-raises original 429 if policy exhausts attempts.
- Stub a 503, 503, 200 sequence → assert eventual success.
- Stub `httpx.ConnectError` × 2, then 200 → assert success.
- Stub same POST with the same idempotency key across retries → assert server-side dedupe (mocked).
- `RetryPolicy.none()` — zero retries, first failure raises.
- Jitter: mock `random.random`, assert bounds.

Integration: existing resource tests ALL pass unchanged (default policy is compatible).

## Scope check

One `_retry.py` module + `_http.py` request-loop refactor + tests. ~6 tasks in the plan. Single focused scope.

## Out of scope

- Retry of streaming responses mid-stream (harder — needs resume via `continuation_token`, which ties to A.4).
- OpenTelemetry span integration — separate follow-up.
- Circuit breakers / rate limiting on the client side — out of scope; server-authoritative.
- Server-side idempotency correctness — the SDK sends the key; the API already de-dupes (verified against backend).
