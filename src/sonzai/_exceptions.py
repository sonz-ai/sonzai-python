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
