# Step 3 A.1: Typed Errors Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the opaque `APIError` / `RateLimitError` / etc. with typed exception classes that carry structured response fields (status code, error code, rate-limit hints, validation details).

**Architecture:** Keep the existing `SonzaiError` base; extend each subclass with kwargs defaulting to `None`. Add `ErrorBody` and `FieldError` pydantic models to parse response JSON. HTTP layer's `_raise_for_status` becomes the single site that builds typed exceptions.

**Tech Stack:** pydantic v2 for structured bodies, httpx for response headers (`Retry-After`, `X-RateLimit-*`), stdlib `datetime` for reset_at, `respx` for tests.

---

## File Structure

**Created:**
- `tests/test_exceptions.py` — exception-class regression tests

**Modified:**
- `src/sonzai/_exceptions.py` — extend classes with kwargs + add `ErrorBody`, `FieldError`, new `ConflictError`/`ValidationError`
- `src/sonzai/_http.py` — rewrite `_raise_for_status` to construct typed exceptions from response
- `src/sonzai/__init__.py` — export `ConflictError`, `ValidationError`, `FieldError`, `ErrorBody`

---

## Task 1: Scaffold `ErrorBody` and `FieldError` models

**Files:**
- Modify: `src/sonzai/_exceptions.py`
- Test: `tests/test_exceptions.py`

- [ ] **Step 1: Create the test file with failing shape tests**

Create `tests/test_exceptions.py`:

```python
"""Regression tests for typed exception classes."""

from __future__ import annotations

from sonzai._exceptions import ErrorBody, FieldError


class TestErrorBody:
    def test_parses_structured_body(self) -> None:
        body = ErrorBody.model_validate(
            {"code": "rate_limited", "message": "Too many requests"}
        )
        assert body.code == "rate_limited"
        assert body.message == "Too many requests"

    def test_preserves_unknown_fields_via_extra(self) -> None:
        body = ErrorBody.model_validate(
            {"code": "oops", "message": "x", "custom_debug": {"a": 1}}
        )
        assert body.model_extra == {"custom_debug": {"a": 1}}

    def test_all_fields_optional(self) -> None:
        body = ErrorBody.model_validate({})
        assert body.code is None
        assert body.message is None


class TestFieldError:
    def test_parses_per_field_error(self) -> None:
        err = FieldError.model_validate(
            {"field": "email", "message": "invalid format", "code": "invalid_email"}
        )
        assert err.field == "email"
        assert err.message == "invalid format"
        assert err.code == "invalid_email"

    def test_code_optional(self) -> None:
        err = FieldError.model_validate({"field": "x", "message": "bad"})
        assert err.code is None
```

- [ ] **Step 2: Run tests — expect ImportError**

Run: `uv run --extra dev pytest tests/test_exceptions.py -v`
Expected: ImportError on `from sonzai._exceptions import ErrorBody, FieldError`.

- [ ] **Step 3: Add `ErrorBody` and `FieldError` to `_exceptions.py`**

At the top of `src/sonzai/_exceptions.py` (after `from __future__ import annotations`), add:

```python
from pydantic import BaseModel, ConfigDict


class FieldError(BaseModel):
    """A single field-level validation error from a 422 response."""

    model_config = ConfigDict(extra="allow")

    field: str
    message: str
    code: str | None = None


class ErrorBody(BaseModel):
    """Parsed JSON body from an error response.

    Preserves unknown top-level fields via pydantic `extra="allow"` so
    server-side additions are visible on `exc.body.model_extra` without
    needing an SDK regen.
    """

    model_config = ConfigDict(extra="allow")

    code: str | None = None
    message: str | None = None
    errors: list[FieldError] | None = None
```

- [ ] **Step 4: Run tests — all pass**

Run: `uv run --extra dev pytest tests/test_exceptions.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add src/sonzai/_exceptions.py tests/test_exceptions.py
git commit -m "feat: add ErrorBody and FieldError scaffolding for typed exceptions

Structured parse of error-response JSON. ErrorBody uses extra='allow'
so unknown server fields surface via .model_extra. Used by the typed
exception classes (subsequent tasks)."
```

---

## Task 2: Augment existing exception classes with typed kwargs

**Files:**
- Modify: `src/sonzai/_exceptions.py`
- Test: `tests/test_exceptions.py`

- [ ] **Step 1: Add failing tests for each augmented class**

Append to `tests/test_exceptions.py`:

```python
from datetime import datetime

from sonzai._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    StreamError,
)


class TestAugmentedExceptions:
    def test_rate_limit_carries_retry_after(self) -> None:
        exc = RateLimitError(
            "Slow down",
            retry_after=30,
            limit=60,
            remaining=0,
            reset_at=datetime(2026, 1, 1),
        )
        assert exc.retry_after == 30
        assert exc.limit == 60
        assert exc.remaining == 0
        assert exc.reset_at == datetime(2026, 1, 1)
        assert "Slow down" in str(exc)

    def test_rate_limit_fields_optional(self) -> None:
        exc = RateLimitError("rate limited")
        assert exc.retry_after is None
        assert exc.limit is None

    def test_permission_denied_carries_scope(self) -> None:
        exc = PermissionDeniedError("forbidden", required_scope="agents:write")
        assert exc.required_scope == "agents:write"

    def test_not_found_carries_resource(self) -> None:
        exc = NotFoundError("agent not found", resource="agent:abc")
        assert exc.resource == "agent:abc"

    def test_api_error_carries_body(self) -> None:
        body = ErrorBody(code="oops", message="server err")
        exc = APIError(500, "server err", code="oops", body=body)
        assert exc.status_code == 500
        assert exc.code == "oops"
        assert exc.body is body
        assert exc.body.message == "server err"

    def test_all_inherit_sonzai_error(self) -> None:
        from sonzai._exceptions import SonzaiError
        assert issubclass(RateLimitError, SonzaiError)
        assert issubclass(PermissionDeniedError, APIError)
        assert issubclass(ValidationError, APIError)

    def test_stream_error_carries_cause(self) -> None:
        exc = StreamError("stream broke", cause="connection_reset")
        assert exc.cause == "connection_reset"
```

Note: `ValidationError` is a new class we add in Step 3.

- [ ] **Step 2: Run tests — expect failures**

Run: `uv run --extra dev pytest tests/test_exceptions.py::TestAugmentedExceptions -v`
Expected: Multiple failures / ImportErrors on `ValidationError` and kwargs.

- [ ] **Step 3: Rewrite `src/sonzai/_exceptions.py` with typed kwargs**

Replace the entire `src/sonzai/_exceptions.py` (keeping the pydantic imports and `ErrorBody`/`FieldError` from Task 1):

```python
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FieldError(BaseModel):
    """A single field-level validation error from a 422 response."""

    model_config = ConfigDict(extra="allow")

    field: str
    message: str
    code: str | None = None


class ErrorBody(BaseModel):
    """Parsed JSON body from an error response.

    Preserves unknown top-level fields via pydantic `extra="allow"` so
    server-side additions are visible on `exc.body.model_extra` without
    needing an SDK regen.
    """

    model_config = ConfigDict(extra="allow")

    code: str | None = None
    message: str | None = None
    errors: list[FieldError] | None = None


class SonzaiError(Exception):
    """Base exception for all Sonzai SDK errors."""


class APIError(SonzaiError):
    """Raised for API errors. All typed status-code subclasses inherit from this."""

    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        code: str | None = None,
        body: ErrorBody | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.body = body
        super().__init__(f"[{status_code}] {message}")


class AuthenticationError(APIError):
    """Raised on 401."""

    def __init__(
        self,
        message: str = "Invalid or missing API key",
        *,
        code: str | None = None,
        body: ErrorBody | None = None,
    ) -> None:
        super().__init__(401, message, code=code, body=body)


class PermissionDeniedError(APIError):
    """Raised on 403."""

    def __init__(
        self,
        message: str = "Permission denied",
        *,
        required_scope: str | None = None,
        code: str | None = None,
        body: ErrorBody | None = None,
    ) -> None:
        self.required_scope = required_scope
        super().__init__(403, message, code=code, body=body)


class NotFoundError(APIError):
    """Raised on 404."""

    def __init__(
        self,
        message: str = "Resource not found",
        *,
        resource: str | None = None,
        code: str | None = None,
        body: ErrorBody | None = None,
    ) -> None:
        self.resource = resource
        super().__init__(404, message, code=code, body=body)


class BadRequestError(APIError):
    """Raised on 400."""

    def __init__(
        self,
        message: str = "Bad request",
        *,
        code: str | None = None,
        body: ErrorBody | None = None,
    ) -> None:
        super().__init__(400, message, code=code, body=body)


class ConflictError(APIError):
    """Raised on 409."""

    def __init__(
        self,
        message: str = "Conflict",
        *,
        resource: str | None = None,
        code: str | None = None,
        body: ErrorBody | None = None,
    ) -> None:
        self.resource = resource
        super().__init__(409, message, code=code, body=body)


class ValidationError(APIError):
    """Raised on 422 with structured per-field errors."""

    def __init__(
        self,
        message: str = "Validation failed",
        *,
        errors: list[FieldError] | None = None,
        body: ErrorBody | None = None,
    ) -> None:
        self.errors = errors or []
        super().__init__(422, message, body=body)


class RateLimitError(APIError):
    """Raised on 429."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        *,
        retry_after: int | None = None,
        limit: int | None = None,
        remaining: int | None = None,
        reset_at: datetime | None = None,
        code: str | None = None,
        body: ErrorBody | None = None,
    ) -> None:
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining
        self.reset_at = reset_at
        super().__init__(429, message, code=code, body=body)


class InternalServerError(APIError):
    """Raised on 5xx."""

    def __init__(
        self,
        message: str = "Internal server error",
        *,
        status_code: int = 500,
        code: str | None = None,
        body: ErrorBody | None = None,
    ) -> None:
        super().__init__(status_code, message, code=code, body=body)


class StreamError(SonzaiError):
    """Raised when an error occurs during SSE streaming."""

    def __init__(
        self,
        message: str,
        *,
        cause: str | None = None,
        body: ErrorBody | None = None,
    ) -> None:
        self.cause = cause
        self.body = body
        super().__init__(message)
```

- [ ] **Step 4: Run tests — all pass**

Run: `uv run --extra dev pytest tests/test_exceptions.py -v`
Expected: All tests pass.

- [ ] **Step 5: Run full suite — no regressions**

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: All existing tests still pass (existing callers use the string positional arg which still works).

- [ ] **Step 6: Commit**

```bash
git add src/sonzai/_exceptions.py tests/test_exceptions.py
git commit -m "feat: augment SDK exception classes with typed kwargs

Each status-code exception now carries structured fields:
- RateLimitError: retry_after, limit, remaining, reset_at
- PermissionDeniedError: required_scope
- NotFoundError: resource
- ConflictError (NEW): 409 Conflict with resource
- ValidationError (NEW): 422 with list[FieldError]
- All: code (server's error code), body (ErrorBody with extras)

Every class still inherits from APIError (and through that, SonzaiError),
so existing \`except APIError:\` catches continue to work. The old
message-only constructors still work because all new kwargs are
keyword-only with defaults."
```

---

## Task 3: Rewrite `_http.py`'s `_raise_for_status`

**Files:**
- Modify: `src/sonzai/_http.py`
- Test: `tests/test_exceptions.py`

- [ ] **Step 1: Add integration-style tests stubbing httpx responses**

Append to `tests/test_exceptions.py`:

```python
import httpx
import pytest
import respx

from sonzai import Sonzai


class TestRaiseForStatus:
    def test_429_populates_retry_after(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/projects").mock(
                return_value=httpx.Response(
                    429,
                    headers={
                        "Retry-After": "30",
                        "X-RateLimit-Limit": "60",
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": "1735689600",
                    },
                    json={"code": "rate_limited", "message": "Too many requests"},
                )
            )
            client = Sonzai(api_key="test-key")
            with pytest.raises(RateLimitError) as exc_info:
                client.projects.list()
            exc = exc_info.value
            assert exc.retry_after == 30
            assert exc.limit == 60
            assert exc.remaining == 0
            assert exc.reset_at == datetime.fromtimestamp(1735689600)
            assert exc.code == "rate_limited"
            assert exc.body is not None
            assert exc.body.message == "Too many requests"

    def test_422_populates_field_errors(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/projects").mock(
                return_value=httpx.Response(
                    422,
                    json={
                        "code": "validation_failed",
                        "message": "Invalid input",
                        "errors": [
                            {"field": "email", "message": "bad", "code": "invalid_email"},
                            {"field": "name", "message": "required"},
                        ],
                    },
                )
            )
            client = Sonzai(api_key="test-key")
            with pytest.raises(ValidationError) as exc_info:
                client.projects.list()
            exc = exc_info.value
            assert len(exc.errors) == 2
            assert exc.errors[0].field == "email"
            assert exc.errors[0].code == "invalid_email"
            assert exc.errors[1].field == "name"

    def test_403_populates_required_scope(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/projects").mock(
                return_value=httpx.Response(
                    403,
                    json={"code": "forbidden", "message": "need scope", "required_scope": "admin"},
                )
            )
            client = Sonzai(api_key="test-key")
            with pytest.raises(PermissionDeniedError) as exc_info:
                client.projects.list()
            exc = exc_info.value
            assert exc.required_scope == "admin"

    def test_non_json_body_parses_gracefully(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/projects").mock(
                return_value=httpx.Response(500, content=b"<html>nope</html>")
            )
            client = Sonzai(api_key="test-key")
            with pytest.raises(InternalServerError) as exc_info:
                client.projects.list()
            exc = exc_info.value
            assert exc.body is None
            assert exc.status_code == 500

    def test_409_raises_conflict(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/projects").mock(
                return_value=httpx.Response(
                    409,
                    json={"code": "already_exists", "message": "duplicate", "resource": "project:foo"},
                )
            )
            client = Sonzai(api_key="test-key")
            with pytest.raises(ConflictError) as exc_info:
                client.projects.list()
            exc = exc_info.value
            assert exc.resource == "project:foo"
```

Add `ConflictError`, `ValidationError` to the existing imports at the top of the file.

- [ ] **Step 2: Run tests — expect failures on new error classes**

Run: `uv run --extra dev pytest tests/test_exceptions.py::TestRaiseForStatus -v`
Expected: `ConflictError` and `ValidationError` not raised; existing exceptions don't populate typed fields.

- [ ] **Step 3: Replace `_raise_for_status` in `src/sonzai/_http.py`**

Find the existing `_raise_for_status` function (near the top of the file — currently takes `status: int, message: str`). Replace its signature and body with:

```python
from datetime import datetime
from pydantic import ValidationError as _PydanticValidationError

from ._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ErrorBody,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ValidationError,
)


def _raise_for_status(response: httpx.Response) -> None:
    """Raise the typed exception matching the response status. Never returns on failure."""
    status = response.status_code
    body = _parse_error_body(response)
    message = _message_from(body, default=f"HTTP {status}")
    code = body.code if body else None

    if status == 401:
        raise AuthenticationError(message, code=code, body=body)
    if status == 403:
        scope = body.model_extra.get("required_scope") if body and body.model_extra else None
        raise PermissionDeniedError(message, required_scope=scope, code=code, body=body)
    if status == 404:
        resource = body.model_extra.get("resource") if body and body.model_extra else None
        raise NotFoundError(message, resource=resource, code=code, body=body)
    if status == 409:
        resource = body.model_extra.get("resource") if body and body.model_extra else None
        raise ConflictError(message, resource=resource, code=code, body=body)
    if status == 422:
        errors = body.errors if body else None
        raise ValidationError(message, errors=errors, body=body)
    if status == 429:
        raise RateLimitError(
            message,
            retry_after=_parse_int(response.headers.get("Retry-After")),
            limit=_parse_int(response.headers.get("X-RateLimit-Limit")),
            remaining=_parse_int(response.headers.get("X-RateLimit-Remaining")),
            reset_at=_parse_reset(response.headers.get("X-RateLimit-Reset")),
            code=code,
            body=body,
        )
    if status == 400:
        raise BadRequestError(message, code=code, body=body)
    if 500 <= status < 600:
        raise InternalServerError(message, status_code=status, code=code, body=body)
    raise APIError(status, message, code=code, body=body)


def _parse_error_body(response: httpx.Response) -> ErrorBody | None:
    if not response.content:
        return None
    try:
        data = response.json()
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    try:
        return ErrorBody.model_validate(data)
    except _PydanticValidationError:
        return None


def _message_from(body: ErrorBody | None, *, default: str) -> str:
    if body and body.message:
        return body.message
    return default


def _parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_reset(value: str | None) -> datetime | None:
    ts = _parse_int(value)
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(ts)
    except (OSError, OverflowError, ValueError):
        return None
```

Then update every existing `_raise_for_status(status, message)` call site in the file to `_raise_for_status(response)`. Use grep to find them:

```bash
grep -n "_raise_for_status" src/sonzai/_http.py
```

For each hit, the surrounding code probably has `response` already in scope — swap the call.

- [ ] **Step 4: Run tests — all pass**

Run: `uv run --extra dev pytest tests/test_exceptions.py -v`
Expected: All typed-exception tests pass.

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: Full suite passes. Existing tests that stubbed error responses still get the same exception classes raised.

- [ ] **Step 5: Commit**

```bash
git add src/sonzai/_http.py tests/test_exceptions.py
git commit -m "feat: _raise_for_status builds typed exceptions from response

Parses the response JSON into ErrorBody and builds the correct typed
exception per status code. Headers (Retry-After, X-RateLimit-*) populate
RateLimitError's structured fields. 409 now raises ConflictError and
422 raises ValidationError (previously both flowed through APIError).

All existing callers use \`except APIError:\` and continue to work
unchanged — typed subclasses inherit from APIError."
```

---

## Task 4: Export the new classes at the top level

**Files:**
- Modify: `src/sonzai/__init__.py`

- [ ] **Step 1: Write a smoke test asserting imports**

Append to `tests/test_exceptions.py`:

```python
class TestPublicImports:
    def test_all_error_classes_importable_from_sonzai(self) -> None:
        from sonzai import (
            APIError,
            AuthenticationError,
            BadRequestError,
            ConflictError,
            ErrorBody,
            FieldError,
            InternalServerError,
            NotFoundError,
            PermissionDeniedError,
            RateLimitError,
            SonzaiError,
            StreamError,
            ValidationError,
        )
        # All importable, no AttributeError.
        assert issubclass(ValidationError, APIError)
        assert issubclass(ConflictError, APIError)
```

- [ ] **Step 2: Run test — expect ImportError on ConflictError, ValidationError, ErrorBody, FieldError**

Run: `uv run --extra dev pytest tests/test_exceptions.py::TestPublicImports -v`
Expected: ImportError.

- [ ] **Step 3: Update `src/sonzai/__init__.py`**

Find the existing imports from `._exceptions`:

```python
from ._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    SonzaiError,
    StreamError,
)
```

Extend to:

```python
from ._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ErrorBody,
    FieldError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    SonzaiError,
    StreamError,
    ValidationError,
)
```

Find the `__all__` list — add the four new names alphabetically:

```python
    "ConflictError",
    # ... existing ...
    "ErrorBody",
    # ... existing ...
    "FieldError",
    # ... existing ...
    "ValidationError",
```

- [ ] **Step 4: Run tests — all pass**

Run: `uv run --extra dev pytest tests/test_exceptions.py -v`
Expected: All pass including `test_all_error_classes_importable_from_sonzai`.

- [ ] **Step 5: Run full suite — no regressions**

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: All tests pass.

- [ ] **Step 6: Commit**

```bash
git add src/sonzai/__init__.py
git commit -m "feat: export ConflictError, ValidationError, ErrorBody, FieldError

These are the new typed-exception surfaces added in this series.
Accessible via \`from sonzai import ValidationError\` etc. All entries
added alphabetically to __all__."
```

---

## Self-Review Findings

Checked the plan against the spec:
- **A.1 spec table** — every class in the table has a Task 2 kwarg + a Task 3 raise branch + a Task 3 test.
- **ErrorBody `extra="allow"`** — Task 1 Step 3 has `ConfigDict(extra="allow")` on both models.
- **409 Conflict and 422 Validation as new classes** — Task 2 Step 3 adds both; Task 3 adds the raise branches.
- **5xx fallback** — Task 3's `_raise_for_status` routes any 5xx into `InternalServerError(status_code=status)`.
- **Generic APIError fallback for unknown statuses** — Task 3's last line of `_raise_for_status` catches everything else.

**Placeholder scan:** no "TBD", "TODO", "implement later".
**Type consistency:** `ErrorBody`, `FieldError`, `RateLimitError.retry_after`, `ValidationError.errors` consistent across tasks. `reset_at: datetime` matches throughout.
