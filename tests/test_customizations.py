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


class TestMemoryNodeMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import MemoryNode
        from sonzai._generated.models import MemoryNode as GenMemoryNode
        assert MemoryNode is GenMemoryNode

    def test_spec_fields_roundtrip(self) -> None:
        """Spec fields are name/description (not title/summary)."""
        from sonzai import MemoryNode
        payload = {
            "node_id": "n1",
            "agent_id": "a1",
            "path": "root/child",
            "name": "my-node",
            "description": "hello",
            "memory_type": "semantic",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }
        node = MemoryNode.model_validate(payload)
        assert node.name == "my-node"
        assert node.description == "hello"
        assert node.memory_type == "semantic"

    def test_old_hand_rolled_fields_gone(self) -> None:
        """title/summary are no longer fields — hand-rolled was stale."""
        from sonzai import MemoryNode
        assert "title" not in MemoryNode.model_fields
        assert "summary" not in MemoryNode.model_fields


class TestAtomicFactMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import AtomicFact
        from sonzai._generated.models import AtomicFact as GenAtomicFact
        assert AtomicFact is GenAtomicFact

    def test_surfaces_new_spec_fields(self) -> None:
        """Spec has extra fields like cluster_id, character_salience that hand-rolled lacked."""
        from sonzai import AtomicFact
        assert "cluster_id" in AtomicFact.model_fields
        assert "character_salience" in AtomicFact.model_fields
        assert "retention_strength" in AtomicFact.model_fields

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import AtomicFact
        payload = {
            "fact_id": "f1",
            "agent_id": "a1",
            "node_id": "n1",
            "atomic_text": "hello",
            "fact_type": "stable",
            "confidence": 0.9,
            "mention_count": 1,
            "last_confirmed": "2026-01-01T00:00:00Z",
            "retention_strength": 0.5,
            "last_retrieved_at": "2026-01-01T00:00:00Z",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }
        fact = AtomicFact.model_validate(payload)
        assert fact.fact_id == "f1"
        assert fact.confidence == 0.9


class TestMemoryResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import MemoryResponse
        from sonzai._generated.models import MemoryResponse as GenMemoryResponse
        assert MemoryResponse is GenMemoryResponse

    def test_schema_field_aliased(self) -> None:
        """$schema is a field (aliased to field_schema in Python)."""
        from sonzai import MemoryResponse
        payload = {
            "$schema": "https://api.sonz.ai/api/v1/schemas/MemoryResponse.json",
            "nodes": [],
        }
        resp = MemoryResponse.model_validate(payload)
        assert resp.field_schema is not None
        assert "MemoryResponse" in str(resp.field_schema)
        assert resp.nodes == []


class TestTimelineSessionMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import TimelineSession
        from sonzai._generated.models import TimelineSession as GenTimelineSession
        assert TimelineSession is GenTimelineSession

    def test_required_roundtrip(self) -> None:
        from sonzai import TimelineSession
        payload = {
            "session_id": "s1",
            "facts": [],
            "first_fact_at": "2026-01-01T00:00:00Z",
            "last_fact_at": "2026-01-01T00:00:00Z",
            "fact_count": 0,
        }
        ts = TimelineSession.model_validate(payload)
        assert ts.session_id == "s1"
        assert ts.fact_count == 0


class TestListAllFactsResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import ListAllFactsResponse
        from sonzai._generated.models import ListAllFactsResponse as GenListAllFactsResponse
        assert ListAllFactsResponse is GenListAllFactsResponse

    def test_references_stored_fact(self) -> None:
        from sonzai import ListAllFactsResponse
        payload = {"facts": [], "total": 0}
        resp = ListAllFactsResponse.model_validate(payload)
        assert resp.total == 0
