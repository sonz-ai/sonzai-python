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


from datetime import datetime

from sonzai._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    StreamError,
    ValidationError,
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
