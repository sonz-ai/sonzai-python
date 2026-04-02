from __future__ import annotations


class SonzaiError(Exception):
    """Base exception for all Sonzai SDK errors."""


class AuthenticationError(SonzaiError):
    """Raised when the API key is invalid or missing."""

    def __init__(self, message: str = "Invalid or missing API key") -> None:
        super().__init__(message)


class NotFoundError(SonzaiError):
    """Raised when the requested resource is not found."""


class BadRequestError(SonzaiError):
    """Raised when the request is invalid."""


class PermissionDeniedError(SonzaiError):
    """Raised when the API key lacks permission for the operation."""


class RateLimitError(SonzaiError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", *, retry_after: float | None = None) -> None:
        super().__init__(message)
        self.retry_after: float | None = retry_after


class InternalServerError(SonzaiError):
    """Raised when the server returns a 5xx error."""


class APIError(SonzaiError):
    """Raised for unexpected API errors."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"[{status_code}] {message}")


class StreamError(SonzaiError):
    """Raised when an error occurs during SSE streaming."""
