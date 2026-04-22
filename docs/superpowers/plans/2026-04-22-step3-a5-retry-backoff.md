# Step 3 A.5: Retry, Backoff, and Idempotency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Auto-retry transient failures (429/5xx/network) with exponential backoff + jitter, honor `Retry-After`, and generate idempotency keys for POST/PUT/PATCH so retries are safe.

**Architecture:** New `RetryPolicy` dataclass holds the config. `Sonzai(retry=...)` accepts it at construction (defaults to sensible baseline). `_http.py`'s request loop consults `policy.should_retry()` after each response and `policy.backoff_seconds()` between retries. Idempotency-Key header is auto-added for mutating methods.

**Tech Stack:** No new deps. `uuid4` for idempotency, `time.sleep` / `asyncio.sleep` for backoff, `random.random` for jitter.

---

## File Structure

**Created:**
- `src/sonzai/_retry.py` — `RetryPolicy` dataclass + helpers
- `tests/test_retry.py` — unit + integration tests

**Modified:**
- `src/sonzai/_http.py` — request loop accepts `RetryPolicy`; adds idempotency key header
- `src/sonzai/_client.py` — `Sonzai(...)` constructor accepts `retry=RetryPolicy(...)` kwarg
- `src/sonzai/__init__.py` — export `RetryPolicy`

---

## Task 1: `RetryPolicy` dataclass + unit tests

**Files:**
- Create: `src/sonzai/_retry.py`
- Test: `tests/test_retry.py`

- [ ] **Step 1: Write failing unit tests**

Create `tests/test_retry.py`:

```python
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
        # attempt 1 → 0.3 * 2^0 = 0.3
        # attempt 2 → 0.3 * 2^1 = 0.6
        # attempt 3 → 0.3 * 2^2 = 1.2
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
        # Falls back to exponential
        assert p.backoff_seconds(attempt=1, retry_after_header="15") == 0.3

    def test_jitter_within_bounds(self) -> None:
        p = RetryPolicy(backoff_factor=1.0, backoff_max=10.0, backoff_jitter=0.5)
        # Base = 1.0; jitter adds ±0.5 * 1.0
        for _ in range(20):
            s = p.backoff_seconds(attempt=1, retry_after_header=None)
            assert 0.5 <= s <= 1.5
```

- [ ] **Step 2: Run — expect ImportError**

Run: `uv run --extra dev pytest tests/test_retry.py -v`
Expected: ImportError on `sonzai._retry`.

- [ ] **Step 3: Create `src/sonzai/_retry.py`**

```python
"""Retry policy for SDK HTTP requests.

The `_http.py` request loop calls `policy.should_retry(...)` after each
response (or network error) and `policy.backoff_seconds(...)` before
sleeping. Defaults are tuned for "be resilient but not abusive" against
the production API.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

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
    backoff_factor: float = 0.3           # seconds; base for exponential
    backoff_max: float = 30.0             # cap on any single sleep
    backoff_jitter: float = 0.1           # 0.1 means ±10% randomness
    retry_on_statuses: frozenset[int] = field(default_factory=lambda: DEFAULT_RETRY_STATUSES)
    retry_on_network: bool = True
    respect_retry_after: bool = True

    @classmethod
    def none(cls) -> RetryPolicy:
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
```

- [ ] **Step 4: Run tests — all pass**

Run: `uv run --extra dev pytest tests/test_retry.py -v`
Expected: All pass.

- [ ] **Step 5: Commit**

```bash
git add src/sonzai/_retry.py tests/test_retry.py
git commit -m "feat: add RetryPolicy dataclass

Dataclass holding retry config: max_attempts, backoff (factor, max,
jitter), status/network filters, Retry-After opt-in. .should_retry()
and .backoff_seconds() are pure functions used by the HTTP loop.
RetryPolicy.none() disables retries entirely."
```

---

## Task 2: Wire `RetryPolicy` into `_http.py` request loop

**Files:**
- Modify: `src/sonzai/_http.py`
- Test: `tests/test_retry.py`

- [ ] **Step 1: Add integration tests stubbing httpx responses**

Append to `tests/test_retry.py`:

```python
import httpx
import respx

from sonzai import RateLimitError, Sonzai
from sonzai._retry import RetryPolicy


class TestHTTPRetry:
    def test_retries_on_429_then_succeeds(self) -> None:
        with respx.mock() as router:
            route = router.get("https://api.sonz.ai/api/v1/projects")
            route.side_effect = [
                httpx.Response(429, headers={"Retry-After": "0"}, json={"message": "slow"}),
                httpx.Response(200, json={"projects": [], "total": 0}),
            ]
            client = Sonzai(api_key="test-key", retry=RetryPolicy(max_attempts=3, backoff_factor=0.001, backoff_jitter=0.0))
            client.projects.list()   # should succeed on 2nd attempt
            assert route.call_count == 2

    def test_exhausts_retries_and_raises(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/projects").mock(
                return_value=httpx.Response(503, json={"message": "down"})
            )
            client = Sonzai(api_key="test-key", retry=RetryPolicy(max_attempts=2, backoff_factor=0.001, backoff_jitter=0.0))
            with pytest.raises(Exception) as exc_info:
                client.projects.list()
            # InternalServerError inherits APIError
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
            return httpx.Response(200, json={"agent_id": "a1"})

        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/agents").mock(side_effect=capture)
            client = Sonzai(api_key="test-key")
            client.agents.create(name="x")
            assert "Idempotency-Key" in captured[0].headers
            assert len(captured[0].headers["Idempotency-Key"]) == 32   # uuid4 hex

    def test_idempotency_key_consistent_across_retries(self) -> None:
        captured: list[str] = []

        def capture(request: httpx.Request) -> httpx.Response:
            captured.append(request.headers["Idempotency-Key"])
            if len(captured) == 1:
                return httpx.Response(503, json={"message": "down"})
            return httpx.Response(200, json={"agent_id": "a1"})

        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/agents").mock(side_effect=capture)
            client = Sonzai(api_key="test-key", retry=RetryPolicy(max_attempts=3, backoff_factor=0.001, backoff_jitter=0.0))
            client.agents.create(name="x")
            # Same key across both attempts
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

    def test_user_supplied_idempotency_key_preserved(self) -> None:
        captured: list[httpx.Request] = []

        def capture(request: httpx.Request) -> httpx.Response:
            captured.append(request)
            return httpx.Response(200, json={"agent_id": "a1"})

        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/agents").mock(side_effect=capture)
            client = Sonzai(api_key="test-key")
            client.agents.create(name="x", idempotency_key="my-custom-key")
            assert captured[0].headers["Idempotency-Key"] == "my-custom-key"
```

- [ ] **Step 2: Run — expect failures (retry not wired, key not injected)**

Run: `uv run --extra dev pytest tests/test_retry.py::TestHTTPRetry tests/test_retry.py::TestIdempotencyKey -v`
Expected: Failures.

- [ ] **Step 3: Update `src/sonzai/_http.py` request loop**

Find the existing `request(...)` method in `HTTPClient`. Replace its body (keep the signature but add optional `idempotency_key` kwarg):

```python
import time
import uuid

# At the top:
from ._retry import NETWORK_EXCEPTION_TYPES, RetryPolicy

# In HTTPClient.__init__, accept retry:
def __init__(
    self,
    *,
    api_key: str,
    base_url: str = "https://api.sonz.ai",
    timeout: float = 60.0,
    retry: RetryPolicy | None = None,
    # ... existing kwargs ...
) -> None:
    self._retry = retry or RetryPolicy()
    # ... existing code ...

# In the request() method:
def request(
    self,
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    body: Any = None,
    stream: bool = False,
    idempotency_key: str | None = None,
) -> Any:
    url = f"{self._base_url}{path}"
    headers = dict(self._base_headers)
    if method.upper() in {"POST", "PUT", "PATCH"}:
        headers["Idempotency-Key"] = idempotency_key or uuid.uuid4().hex

    attempt = 0
    last_exc: Exception | None = None
    while attempt < self._retry.max_attempts:
        attempt += 1
        try:
            response = self._client.request(
                method, url, params=params, json=body, headers=headers
            )
        except Exception as e:
            if not self._retry.should_retry(attempt=attempt, status=None, exc=e):
                raise
            last_exc = e
            time.sleep(self._retry.backoff_seconds(attempt=attempt, retry_after_header=None))
            continue

        if response.is_success:
            if not response.content:
                return None
            return response.json()

        if self._retry.should_retry(attempt=attempt, status=response.status_code, exc=None):
            time.sleep(
                self._retry.backoff_seconds(
                    attempt=attempt,
                    retry_after_header=response.headers.get("Retry-After"),
                )
            )
            continue

        _raise_for_status(response)

    # All retries exhausted on a non-raising path (e.g., network errors)
    if last_exc is not None:
        raise last_exc
    raise APIError(0, "retries exhausted")
```

Mirror the same in `AsyncHTTPClient.request()` with `await asyncio.sleep(...)`.

Then add `idempotency_key: str | None = None` to `get/post/put/patch/delete` helper methods (pass through to `request`). Only `post/put/patch` actually use it at the wire; `get/delete` ignore.

- [ ] **Step 4: Update `Sonzai` + `AsyncSonzai` constructors**

In `src/sonzai/_client.py`, add:

```python
from ._retry import RetryPolicy

class Sonzai:
    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = "https://api.sonz.ai",
        timeout: float = 60.0,
        retry: RetryPolicy | None = None,
        max_retries: int | None = None,   # backwards-compat kwarg
    ) -> None:
        if retry is None and max_retries is not None:
            retry = RetryPolicy(max_attempts=max_retries)
        self._http = HTTPClient(
            api_key=api_key or os.environ.get("SONZAI_API_KEY", ""),
            base_url=base_url,
            timeout=timeout,
            retry=retry,
        )
        # ... existing resource wiring ...
```

Mirror for `AsyncSonzai`.

- [ ] **Step 5: Plumb `idempotency_key` through mutating resource methods**

For resource methods where the user might want to supply a key (all `post`/`put`/`patch` methods), add an optional `idempotency_key: str | None = None` kwarg and forward it to `self._http.post(..., idempotency_key=idempotency_key)`.

Start with `agents.create` (test coverage); extending to all mutating methods is mechanical and can be piggy-backed on the Step 3 A.2 typed-request-body migration. For this plan, just wire `agents.create` and the other top-hit methods the test coverage touches.

- [ ] **Step 6: Run tests**

Run: `uv run --extra dev pytest tests/test_retry.py -v`
Expected: All pass.

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: Full suite passes. Sleep times in tests use `backoff_factor=0.001` so retries complete in milliseconds.

- [ ] **Step 7: Commit**

```bash
git add src/sonzai/_http.py src/sonzai/_client.py src/sonzai/resources/agents.py tests/test_retry.py
git commit -m "feat: RetryPolicy wired into HTTP loop + idempotency keys

Request loop honors RetryPolicy:
- retry_on_statuses (default: 408/429/500/502/503/504)
- retry_on_network (default: True, for ConnectError/timeouts)
- Retry-After header respected
- exponential backoff with jitter, capped at backoff_max

Mutating methods (POST/PUT/PATCH) carry Idempotency-Key header:
- auto-generated uuid4 by default
- consistent across retries (server dedupes retry hits)
- user can override via idempotency_key= kwarg on resource methods

Sonzai(...) and AsyncSonzai(...) accept retry=RetryPolicy(...). The
existing max_retries= kwarg maps to RetryPolicy.max_attempts for
backwards compat."
```

---

## Task 3: Export `RetryPolicy`

**Files:**
- Modify: `src/sonzai/__init__.py`

- [ ] **Step 1: Test public import**

```bash
uv run --extra dev python -c "from sonzai import RetryPolicy; print('ok')"
```
Expected: ImportError.

- [ ] **Step 2: Add to `sonzai/__init__.py`**

```python
from ._retry import RetryPolicy
```

In `__all__` (alphabetical):
```python
    "RetryPolicy",
```

- [ ] **Step 3: Verify + commit**

Run: `uv run --extra dev python -c "from sonzai import RetryPolicy; print('ok')"` → `ok`.

Run: `uv run --extra dev pytest 2>&1 | tail -3` → all pass.

```bash
git add src/sonzai/__init__.py
git commit -m "feat: export RetryPolicy at top level"
```

---

## Self-Review Findings

- **Spec `RetryPolicy` dataclass** — Task 1 Step 3 matches the spec exactly.
- **Spec idempotency keys on POST/PUT/PATCH only** — Task 2 Step 3 gates by `method.upper() in {"POST", "PUT", "PATCH"}`.
- **Spec same key across retries** — Task 2 Step 3 generates the key once outside the loop; all retries reuse it.
- **Spec `Retry-After` respected** — `backoff_seconds` returns the parsed header value when `respect_retry_after=True`.
- **Spec `max_retries=` backwards-compat** — Task 2 Step 4 adapter shown.
- **Spec out-of-scope: streaming retries** — respected; the request loop covers non-streaming paths only. Streaming passes retry=None-equivalent today.

**Placeholder scan**: no TBDs. Resource-method `idempotency_key=` kwarg plumbing acknowledged as partial (top-hit methods only in this plan) with a note that A.2 batch migration naturally extends it.

**Type consistency**: `RetryPolicy`, `NETWORK_EXCEPTION_TYPES`, `should_retry()`, `backoff_seconds()` signatures consistent across tasks.
