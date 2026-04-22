# Step 3 A.1: Typed Errors Design

**Goal:** Replace the opaque `APIError` / `RateLimitError` / etc. with typed exception classes that carry structured response fields (status code, error code, rate-limit hints, validation details) so callers can handle API failures with narrow `except` clauses and typed attribute access instead of parsing strings out of `Exception.args[0]`.

**Architecture:** Keep the existing `SonzaiError` base; extend each subclass with the fields the server actually returns. The HTTP layer (`src/sonzai/_http.py`) continues to be the single raise site, but now parses the JSON body (if present) and constructs the typed exception with structured kwargs. No change to the public class names — backwards-compatible on `except APIError:` but new on attribute access.

**Tech Stack:** pydantic v2 for the structured body parse (reuse `_generated.models.ErrorModel` if spec emits one, else a small hand-written `_ErrorBody`), httpx for header access, stdlib `dataclasses` out.

---

## What users get

```python
from sonzai import RateLimitError, ValidationError, PermissionDeniedError

try:
    client.agents.chat(agent_id="x", messages=[...])
except RateLimitError as e:
    print(f"Slow down — try again in {e.retry_after}s")
    print(f"Quota: {e.remaining}/{e.limit} left this minute")
except ValidationError as e:
    for err in e.errors:  # list[FieldError]
        print(f"{err.field}: {err.message}")
except PermissionDeniedError as e:
    print(f"Need scope: {e.required_scope}")
```

Today every caller unpacks `str(exc)` or reaches into an opaque `e.body` dict. After this change, the typed attributes are the primary API.

## Classes to change (in `src/sonzai/_exceptions.py`)

Each gains keyword-only structured fields, defaulting to None/empty when the server omits them, plus a lightweight `ErrorBody` for the full parsed JSON.

| Status | Class | New typed fields |
| --- | --- | --- |
| 400 | `BadRequestError` | `code: str \| None`, `body: ErrorBody \| None` |
| 401 | `AuthenticationError` | `code: str \| None`, `body: ErrorBody \| None` |
| 403 | `PermissionDeniedError` | `required_scope: str \| None`, `code: str \| None`, `body: ErrorBody \| None` |
| 404 | `NotFoundError` | `resource: str \| None`, `code: str \| None`, `body: ErrorBody \| None` |
| 409 | `ConflictError` (new) | `resource: str \| None`, `code: str \| None`, `body: ErrorBody \| None` |
| 422 | `ValidationError` (new) | `errors: list[FieldError]`, `body: ErrorBody \| None` |
| 429 | `RateLimitError` | `retry_after: int \| None`, `limit: int \| None`, `remaining: int \| None`, `reset_at: datetime \| None`, `body: ErrorBody \| None` |
| 5xx | `InternalServerError` | `code: str \| None`, `body: ErrorBody \| None` |
| — | `StreamError` | `cause: str \| None`, `body: ErrorBody \| None` |
| fallback | `APIError` | `status_code: int`, `code: str \| None`, `body: ErrorBody \| None` (existing, augmented) |

`FieldError` is a small pydantic model with `field: str`, `message: str`, `code: str | None`.

`ErrorBody` is pydantic v2 with `extra="allow"` so unknown server fields are preserved via `__pydantic_extra__`.

## Raise site (`src/sonzai/_http.py`)

Existing `_raise_for_status(status, message)` becomes `_raise_for_status(response)`:
1. Extract headers (`Retry-After`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`) for 429.
2. Attempt `response.json()`; parse into `ErrorBody` with pydantic. If body isn't JSON, `body=None`.
3. Dispatch on `status_code` to the correct class, passing `message` + typed kwargs.
4. 409 and 422 are new statuses we start raising separately (today they flow through `APIError` generic).

All raises happen inside one function — no new call sites.

## Backwards compatibility

- Every existing class name and module path is preserved.
- `except APIError:` still catches everything (all typed classes inherit from it).
- Old constructor signatures (`RateLimitError(message)`) keep working — new kwargs are defaulted.
- Users who string-parse from `str(exc)` keep working.
- New `ConflictError` and `ValidationError` subclass `APIError`, so anyone using the generic-catch pattern loses nothing.

## Testing

`tests/test_exceptions.py` (new):
- Stub a 429 response with full rate-limit headers → assert `RateLimitError.retry_after == 30`, etc.
- Stub a 422 with a typical validation body → assert `err.errors[0].field == "email"`.
- Stub a 403 with `required_scope` in body → assert extracted.
- Stub an error with non-JSON body → assert `body is None`, `message` populated.
- Assert `except APIError:` still catches a `RateLimitError` (inheritance).

Use `respx` to mock httpx responses — matches the pattern in existing `tests/test_client.py`.

## Scope check

This is one focused implementation plan. ~1 file to write (`_exceptions.py` expansion), ~1 file to modify (`_http.py` raise-site), ~1 file to add (`test_exceptions.py`). Estimate: 6 tasks in the plan.

## Out of scope (future follow-ups)

- Mapping *per-error-code* (not just per-status) to subclasses — e.g., `InsufficientCreditsError` extends `BadRequestError`. Deferrable; not every API has stable error codes.
- Translating errors back to typed ones inside streaming events (`ChatStreamEvent.error`) — covered by Step 3 A.4 (typed streaming).
- Retry hints (should 429 be auto-retried?) — covered by Step 3 A.5 (retry/backoff).
