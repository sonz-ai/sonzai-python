"""Regression tests for typed exception classes."""

from __future__ import annotations

from datetime import datetime

import httpx
import pytest
import respx

from sonzai import Sonzai
from sonzai._exceptions import (
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
    StreamError,
    ValidationError,
)


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
