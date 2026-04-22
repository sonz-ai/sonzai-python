"""Tests for _request_helpers.encode_body."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from sonzai._request_helpers import encode_body


class ExampleBody(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    user_id: str
    item_count: int = Field(alias="itemCount", default=0)
    tags: list[str] | None = None


class TestEncodeBody:
    def test_basic_validation_roundtrip(self) -> None:
        wire = encode_body(ExampleBody, {"user_id": "u1", "itemCount": 5})
        assert wire == {"user_id": "u1", "itemCount": 5}

    def test_snake_case_input_dumps_to_wire_alias(self) -> None:
        wire = encode_body(ExampleBody, {"user_id": "u1", "item_count": 5})
        assert wire == {"user_id": "u1", "itemCount": 5}

    def test_missing_required_raises(self) -> None:
        with pytest.raises(ValidationError):
            encode_body(ExampleBody, {"item_count": 5})

    def test_unknown_field_raises(self) -> None:
        """extra='forbid' on the body class must surface typos."""
        with pytest.raises(ValidationError) as exc_info:
            encode_body(ExampleBody, {"user_id": "u1", "uesr_typo": "oops"})
        assert "uesr_typo" in str(exc_info.value)

    def test_none_optional_dropped_from_wire(self) -> None:
        wire = encode_body(ExampleBody, {"user_id": "u1"})
        assert "tags" not in wire   # exclude_none default

    def test_null_optional_dropped(self) -> None:
        wire = encode_body(ExampleBody, {"user_id": "u1", "tags": None})
        assert "tags" not in wire
