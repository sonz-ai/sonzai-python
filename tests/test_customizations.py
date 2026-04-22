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


# ---------------------------------------------------------------------------
# Batch 2 — Personality & Traits
# ---------------------------------------------------------------------------

_BIG5_TRAIT = {"score": 0.7, "confidence": 0.9}
_FULL_BIG5_ASSESSMENT = {
    "agreeableness": _BIG5_TRAIT,
    "conscientiousness": _BIG5_TRAIT,
    "extraversion": _BIG5_TRAIT,
    "neuroticism": _BIG5_TRAIT,
    "openness": _BIG5_TRAIT,
}
_DIMENSIONS = {
    "aesthetic": 7.0,
    "assertiveness": 6.0,
    "compassion": 9.0,
    "enthusiasm": 7.0,
    "industriousness": 6.0,
    "intellect": 9.0,
    "orderliness": 5.0,
    "politeness": 8.0,
    "volatility": 2.0,
    "withdrawal": 3.0,
}
_BEHAVIORS = {
    "conflict_approach": "collaborative",
    "empathy_style": "reflective",
    "question_frequency": "moderate",
    "response_length": "medium",
}
_PREFERENCES = {
    "conversation_pace": "relaxed",
    "emotional_expression": "open",
    "formality": "casual",
    "humor_style": "dry",
}
_PROFILE = {
    "agent_id": "agent_1",
    "behaviors": _BEHAVIORS,
    "big5": _FULL_BIG5_ASSESSMENT,
    "created_at": "2026-01-01T00:00:00Z",
    "dimensions": _DIMENSIONS,
    "gender": "female",
    "name": "Luna",
    "preferences": _PREFERENCES,
    "primary_traits": ["curious", "empathetic"],
    "speech_patterns": ["uses ellipses...", "asks questions"],
    "temperature": 0.7,
    "true_dislikes": ["rudeness"],
    "true_interests": ["astronomy", "cooking"],
}
_DELTA = {
    "delta": 0.05,
    "new_value": 0.8,
    "old_value": 0.75,
    "timestamp": "2026-01-01T00:00:00Z",
    "trait_category": "big5",
    "trait_name": "openness",
    "trigger_type": "conversation",
}


class TestBig5TraitMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import Big5Trait
        from sonzai._generated.models import Big5Trait as GenBig5Trait
        assert Big5Trait is GenBig5Trait

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import Big5Trait
        trait = Big5Trait.model_validate({"score": 0.75, "confidence": 0.9})
        assert trait.score == 0.75
        assert trait.confidence == 0.9
        assert trait.level is None
        assert trait.facets is None

    def test_old_fields_gone(self) -> None:
        from sonzai import Big5Trait
        # hand-rolled had `percentile` — spec does not
        assert "percentile" not in Big5Trait.model_fields


class TestBig5Migration:
    def test_imports_from_generated(self) -> None:
        from sonzai import Big5
        from sonzai._generated.models import Big5 as GenBig5
        assert Big5 is GenBig5

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import Big5
        payload = {
            "agreeableness": 0.9,
            "conscientiousness": 0.6,
            "extraversion": 0.75,
            "neuroticism": 0.25,
            "openness": 0.85,
        }
        b = Big5.model_validate(payload)
        assert b.openness == 0.85
        assert b.agreeableness == 0.9

    def test_old_fields_gone(self) -> None:
        from sonzai import Big5
        # hand-rolled Big5 had Big5Trait objects; generated has float fields
        # The field names are the same but types differ — verify they're floats
        b = Big5.model_validate({
            "agreeableness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "neuroticism": 0.5,
            "openness": 0.5,
        })
        assert isinstance(b.openness, float)


class TestPersonalityDimensionsMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import PersonalityDimensions
        from sonzai._generated.models import PersonalityDimensions as GenPersonalityDimensions
        assert PersonalityDimensions is GenPersonalityDimensions

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import PersonalityDimensions
        dims = PersonalityDimensions.model_validate(_DIMENSIONS)
        assert dims.intellect == 9.0
        assert dims.withdrawal == 3.0
        assert dims.volatility == 2.0


class TestTraitPrecisionMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import TraitPrecision
        from sonzai._generated.models import TraitPrecision as GenTraitPrecision
        assert TraitPrecision is GenTraitPrecision

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import TraitPrecision
        tp = TraitPrecision.model_validate({
            "precision": 0.85,
            "last_updated_at": "2026-01-01T00:00:00Z",
            "observation_count": 42,
        })
        assert tp.precision == 0.85
        assert tp.observation_count == 42
        assert tp.last_updated_at is not None


class TestPersonalityProfileMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import PersonalityProfile
        from sonzai._generated.models import PersonalityProfile as GenPersonalityProfile
        assert PersonalityProfile is GenPersonalityProfile

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import PersonalityProfile
        profile = PersonalityProfile.model_validate(_PROFILE)
        assert profile.agent_id == "agent_1"
        assert profile.name == "Luna"
        assert profile.temperature == 0.7
        assert profile.big5.openness.score == 0.7
        assert profile.dimensions.intellect == 9.0

    def test_old_fields_gone(self) -> None:
        from sonzai import PersonalityProfile
        # hand-rolled had bio/avatar_url/personality_prompt as required str (non-optional)
        # generated has them as optional — just verify field exists in right form
        assert "bio" in PersonalityProfile.model_fields
        # hand-rolled had no field_schema; generated PersonalityProfile has no $schema either


class TestPersonalityDeltaMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import PersonalityDelta
        from sonzai._generated.models import PersonalityDelta as GenPersonalityDelta
        assert PersonalityDelta is GenPersonalityDelta

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import PersonalityDelta
        delta = PersonalityDelta.model_validate(_DELTA)
        assert delta.trait_category == "big5"
        assert delta.trait_name == "openness"
        assert delta.delta == 0.05
        assert delta.trigger_type == "conversation"

    def test_old_fields_gone(self) -> None:
        from sonzai import PersonalityDelta
        # hand-rolled had delta_id, change, reason — spec does not
        assert "delta_id" not in PersonalityDelta.model_fields
        assert "change" not in PersonalityDelta.model_fields
        assert "reason" not in PersonalityDelta.model_fields


class TestPersonalityResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import PersonalityResponse
        from sonzai._generated.models import PersonalityResponse as GenPersonalityResponse
        assert PersonalityResponse is GenPersonalityResponse

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import PersonalityResponse
        resp = PersonalityResponse.model_validate({
            "profile": _PROFILE,
            "evolution": [_DELTA],
        })
        assert resp.profile.name == "Luna"
        assert len(resp.evolution) == 1
        assert resp.evolution[0].trait_name == "openness"

    def test_schema_field_aliased(self) -> None:
        from sonzai import PersonalityResponse
        resp = PersonalityResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/PersonalityResponse.json",
            "profile": _PROFILE,
            "evolution": None,
        })
        assert resp.field_schema is not None
        assert "PersonalityResponse" in str(resp.field_schema)
        assert resp.evolution is None

    def test_old_evolution_shape_gone(self) -> None:
        from sonzai import PersonalityDelta
        # old hand-rolled PersonalityDelta had delta_id; spec has trait_category
        assert "trait_category" in PersonalityDelta.model_fields


# ---------------------------------------------------------------------------
# Batch 3 — Agent Behavior (Goal, Habit, Interests)
# ---------------------------------------------------------------------------


class TestGoalMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import Goal
        from sonzai._generated.models import Goal as GenGoal
        assert Goal is GenGoal

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import Goal
        payload = {
            "goal_id": "g1",
            "agent_id": "a1",
            "type": "personal_growth",
            "title": "Learn Python",
            "description": "Become proficient in Python",
            "priority": 1,
            "status": "active",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-02T00:00:00Z",
        }
        goal = Goal.model_validate(payload)
        assert goal.goal_id == "g1"
        assert goal.agent_id == "a1"
        assert goal.type == "personal_growth"
        assert goal.status == "active"
        assert goal.priority == 1

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import Goal
        with pytest.raises(ValidationError):
            Goal.model_validate({
                "goal_id": "g1",
                "agent_id": "a1",
                "type": "personal_growth",
                "title": "Learn Python",
                "description": "desc",
                "priority": 1,
                "status": "active",
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-02T00:00:00Z",
                "unknown_field": "boom",
            })


class TestGoalsResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import GoalsResponse
        from sonzai._generated.models import GoalsResponse as GenGoalsResponse
        assert GoalsResponse is GenGoalsResponse

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import GoalsResponse
        resp = GoalsResponse.model_validate({"goals": None})
        assert resp.goals is None

    def test_schema_field_aliased(self) -> None:
        from sonzai import GoalsResponse
        resp = GoalsResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/GoalsResponse.json",
            "goals": None,
        })
        assert resp.field_schema is not None
        assert "GoalsResponse" in str(resp.field_schema)


class TestHabitMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import Habit
        from sonzai._generated.models import Habit as GenHabit
        assert Habit is GenHabit

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import Habit
        payload = {
            "agent_id": "a1",
            "name": "morning-run",
            "category": "fitness",
            "description": "Run every morning",
            "display_name": "Morning Run",
            "strength": 0.75,
            "formed": True,
            "observation_count": 30,
            "last_reinforced_at": "2026-01-15T08:00:00Z",
            "daily_reinforced": 0.9,
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-15T08:00:00Z",
        }
        habit = Habit.model_validate(payload)
        assert habit.agent_id == "a1"
        assert habit.name == "morning-run"
        assert habit.strength == 0.75
        assert habit.formed is True
        assert habit.observation_count == 30

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import Habit
        with pytest.raises(ValidationError):
            Habit.model_validate({
                "agent_id": "a1",
                "name": "morning-run",
                "category": "fitness",
                "description": "desc",
                "display_name": "Morning Run",
                "strength": 0.5,
                "formed": False,
                "observation_count": 0,
                "last_reinforced_at": "2026-01-01T00:00:00Z",
                "daily_reinforced": 0.0,
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
                "unknown_field": "boom",
            })


class TestHabitsResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import HabitsResponse
        from sonzai._generated.models import HabitsResponse as GenHabitsResponse
        assert HabitsResponse is GenHabitsResponse

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import HabitsResponse
        resp = HabitsResponse.model_validate({"habits": None})
        assert resp.habits is None

    def test_schema_field_aliased(self) -> None:
        from sonzai import HabitsResponse
        resp = HabitsResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/HabitsResponse.json",
            "habits": None,
        })
        assert resp.field_schema is not None
        assert "HabitsResponse" in str(resp.field_schema)


class TestInterestsResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import InterestsResponse
        from sonzai._generated.models import InterestsResponse as GenInterestsResponse
        assert InterestsResponse is GenInterestsResponse

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import InterestsResponse
        resp = InterestsResponse.model_validate({"interests": None})
        assert resp.interests is None

    def test_schema_field_aliased(self) -> None:
        from sonzai import InterestsResponse
        resp = InterestsResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/InterestsResponse.json",
            "interests": None,
        })
        assert resp.field_schema is not None
        assert "InterestsResponse" in str(resp.field_schema)
