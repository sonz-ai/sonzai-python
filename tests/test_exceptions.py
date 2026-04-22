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
