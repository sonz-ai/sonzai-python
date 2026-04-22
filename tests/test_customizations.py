"""Regression tests for _customizations/ layer."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from sonzai import AgentCapabilities, ChatStreamEvent, StoredFact


class TestStoredFact:
    def test_imports_from_customizations(self) -> None:
        from sonzai._customizations import StoredFact as CustStoredFact

        assert StoredFact is CustStoredFact

    def test_roundtrips_all_spec_fields(self) -> None:
        payload = {
            "fact_id": "fact_123",
            "content": "user likes coffee",
            "fact_type": "preference",
            "importance": 0.8,
            "confidence": 0.95,
            "entity": "user",
            "source_type": "chat",
            "source_id": "msg_42",
            "session_id": "sess_abc",
            "mention_count": 3,
            "metadata": {"extra": "info"},
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-02T00:00:00Z",
        }
        fact = StoredFact.model_validate(payload)
        assert fact.fact_id == "fact_123"
        assert fact.session_id == "sess_abc"
        assert fact.source_id == "msg_42"
        assert fact.metadata == {"extra": "info"}

    def test_unknown_fields_raise_under_forbid(self) -> None:
        """Generated StoredFact uses extra='forbid' per spec
        additionalProperties: false. Unknown fields must raise
        ValidationError — this is the loud-drift-detection behavior that
        would have caught the release-time session_id/source_id bug.
        """
        with pytest.raises(ValidationError) as exc:
            StoredFact.model_validate({
                "fact_id": "x",
                "content": "y",
                "fact_type": "t",
                "importance": 0.0,
                "confidence": 0.0,
                "mention_count": 0,
                "created_at": "",
                "updated_at": "",
                "future_field_that_does_not_exist_yet": "foo",
            })
        assert "future_field_that_does_not_exist_yet" in str(exc.value)


class TestAgentCapabilities:
    # Required fields in the generated spec: imageGeneration, musicGeneration,
    # videoGeneration, voiceGeneration (no defaults → must always be present).
    _REQUIRED = {
        "imageGeneration": False,
        "musicGeneration": False,
        "videoGeneration": False,
        "voiceGeneration": False,
    }
    # Same required fields in snake_case form (for populate_by_name=True tests).
    _REQUIRED_SNAKE = {
        "image_generation": False,
        "music_generation": False,
        "video_generation": False,
        "voice_generation": False,
    }

    def test_imports_from_customizations(self) -> None:
        from sonzai._customizations import AgentCapabilities as CustAgentCapabilities

        assert AgentCapabilities is CustAgentCapabilities

    def test_camel_case_alias_input(self) -> None:
        """Server sends camelCase; SDK exposes snake_case with aliases."""
        payload = {
            **self._REQUIRED,
            "imageGeneration": True,
            "memoryMode": "full",
            "musicGeneration": False,
        }
        caps = AgentCapabilities.model_validate(payload)
        assert caps.custom_tools is None
        assert caps.image_generation is True
        assert caps.memory_mode == "full"

    def test_snake_case_input_also_works(self) -> None:
        """populate_by_name=True lets users pass either form."""
        payload = {
            **self._REQUIRED_SNAKE,
            "image_generation": True,
            "memory_mode": "summary",
        }
        caps = AgentCapabilities.model_validate(payload)
        assert caps.image_generation is True

    def test_dump_round_trips_to_camel(self) -> None:
        caps = AgentCapabilities.model_validate({
            **self._REQUIRED,
            "imageGeneration": True,
            "memoryMode": "full",
        })
        dumped = caps.model_dump(by_alias=True, exclude_none=True)
        assert "imageGeneration" in dumped
        assert "musicGeneration" in dumped
        assert "memoryMode" in dumped


class TestChatStreamEvent:
    def test_imports_from_customizations(self) -> None:
        from sonzai._customizations import ChatStreamEvent as CustChatStreamEvent

        assert ChatStreamEvent is CustChatStreamEvent

    def test_content_property_on_delta_frame(self) -> None:
        event = ChatStreamEvent.model_validate(
            {"choices": [{"delta": {"content": "Hello"}, "index": 0}]}
        )
        assert event.content == "Hello"

    def test_empty_event_has_no_content(self) -> None:
        event = ChatStreamEvent.model_validate({})
        assert event.content == ""
        assert not event.is_finished

    def test_is_finished_on_stop_frame(self) -> None:
        event = ChatStreamEvent.model_validate(
            {"choices": [{"delta": {"content": "."}, "finish_reason": "stop", "index": 0}]}
        )
        assert event.is_finished

    def test_client_extension_fields_default_empty(self) -> None:
        event = ChatStreamEvent.model_validate({})
        assert event.full_content == ""
        assert event.finish_reason == ""
        assert event.external_tool_calls == []
        assert event.is_token_error is False

    def test_client_extension_fields_round_trip(self) -> None:
        event = ChatStreamEvent(
            full_content="done",
            finish_reason="stop",
            continuation_token="abc",
            is_token_error=True,
        )
        assert event.full_content == "done"
        assert event.continuation_token == "abc"
        assert event.is_token_error is True

    def test_free_form_data_preserved(self) -> None:
        """`data` on side_effects frames is free-form per spec — must survive."""
        event = ChatStreamEvent.model_validate(
            {"type": "side_effects", "data": {"facts": [{"content": "x"}]}}
        )
        assert event.type == "side_effects"
        assert event.data == {"facts": [{"content": "x"}]}
