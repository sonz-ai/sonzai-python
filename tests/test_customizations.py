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


# ---------------------------------------------------------------------------
# Batch 4 — Mood & Diary
# ---------------------------------------------------------------------------

_MOOD_STATE = {
    "agent_id": "agent_1",
    "valence": 0.6,
    "arousal": 0.4,
    "tension": 0.2,
    "affiliation": 0.8,
    "label": "content",
    "baseline_valence": 0.5,
    "baseline_arousal": 0.5,
    "baseline_tension": 0.3,
    "baseline_affiliation": 0.7,
    "last_interaction_at": "2026-01-01T00:00:00Z",
    "last_decay_at": "2026-01-01T00:00:00Z",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-02T00:00:00Z",
}


class TestMoodStateMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import MoodState
        from sonzai._generated.models import MoodState as GenMoodState
        assert MoodState is GenMoodState

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import MoodState
        ms = MoodState.model_validate(_MOOD_STATE)
        assert ms.agent_id == "agent_1"
        assert ms.valence == 0.6
        assert ms.arousal == 0.4
        assert ms.tension == 0.2
        assert ms.affiliation == 0.8
        assert ms.label == "content"
        assert ms.baseline_valence == 0.5
        assert ms.last_interaction_at is not None

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import MoodState
        with pytest.raises(ValidationError):
            MoodState.model_validate({**_MOOD_STATE, "unknown_field": "boom"})

    def test_old_hand_rolled_fields_gone(self) -> None:
        """Hand-rolled MoodState lacked agent_id and baseline_* fields."""
        from sonzai import MoodState
        assert "agent_id" in MoodState.model_fields
        assert "baseline_valence" in MoodState.model_fields
        assert "baseline_arousal" in MoodState.model_fields
        assert "baseline_tension" in MoodState.model_fields
        assert "baseline_affiliation" in MoodState.model_fields


class TestMoodResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import MoodResponse
        from sonzai._generated.models import MoodResponse as GenMoodResponse
        assert MoodResponse is GenMoodResponse

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import MoodResponse
        resp = MoodResponse.model_validate({"mood": _MOOD_STATE})
        assert resp.mood.agent_id == "agent_1"
        assert resp.mood.valence == 0.6

    def test_schema_field_aliased(self) -> None:
        from sonzai import MoodResponse
        resp = MoodResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/MoodResponse.json",
            "mood": _MOOD_STATE,
        })
        assert resp.field_schema is not None
        assert "MoodResponse" in str(resp.field_schema)

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import MoodResponse
        with pytest.raises(ValidationError):
            MoodResponse.model_validate({"mood": _MOOD_STATE, "unknown_field": "boom"})


class TestMoodHistoryEntryMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import MoodHistoryEntry
        from sonzai._generated.models import MoodHistoryEntry as GenMoodHistoryEntry
        assert MoodHistoryEntry is GenMoodHistoryEntry

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import MoodHistoryEntry
        entry = MoodHistoryEntry.model_validate({
            "valence": 0.5,
            "arousal": 0.3,
            "tension": 0.2,
            "affiliation": 0.7,
            "timestamp": "2026-01-01T00:00:00Z",
        })
        assert entry.valence == 0.5
        assert entry.tension == 0.2
        assert entry.timestamp == "2026-01-01T00:00:00Z"
        assert entry.label is None

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import MoodHistoryEntry
        with pytest.raises(ValidationError):
            MoodHistoryEntry.model_validate({
                "valence": 0.5, "arousal": 0.3, "tension": 0.2,
                "affiliation": 0.7, "timestamp": "2026-01-01T00:00:00Z",
                "unknown_field": "boom",
            })


class TestMoodHistoryResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import MoodHistoryResponse
        from sonzai._generated.models import MoodHistoryResponse as GenMoodHistoryResponse
        assert MoodHistoryResponse is GenMoodHistoryResponse

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import MoodHistoryResponse
        resp = MoodHistoryResponse.model_validate({"entries": None})
        assert resp.entries is None

    def test_with_entries(self) -> None:
        from sonzai import MoodHistoryResponse
        resp = MoodHistoryResponse.model_validate({
            "entries": [{
                "valence": 0.5, "arousal": 0.3, "tension": 0.2,
                "affiliation": 0.7, "timestamp": "2026-01-01T00:00:00Z",
            }],
        })
        assert resp.entries is not None
        assert len(resp.entries) == 1
        assert resp.entries[0].valence == 0.5

    def test_schema_field_aliased(self) -> None:
        from sonzai import MoodHistoryResponse
        resp = MoodHistoryResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/MoodHistoryResponse.json",
            "entries": None,
        })
        assert resp.field_schema is not None
        assert "MoodHistoryResponse" in str(resp.field_schema)


class TestDiaryEntryMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import DiaryEntry
        from sonzai._generated.models import DiaryEntry as GenDiaryEntry
        assert DiaryEntry is GenDiaryEntry

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import DiaryEntry
        entry = DiaryEntry.model_validate({
            "entry_id": "e1",
            "agent_id": "a1",
            "date": "2026-01-01",
            "content": "Today was a good day.",
            "created_at": "2026-01-01T00:00:00Z",
        })
        assert entry.entry_id == "e1"
        assert entry.agent_id == "a1"
        assert entry.date == "2026-01-01"
        assert entry.content == "Today was a good day."
        assert entry.created_at is not None

    def test_optional_fields_default_none(self) -> None:
        from sonzai import DiaryEntry
        entry = DiaryEntry.model_validate({
            "entry_id": "e1",
            "agent_id": "a1",
            "date": "2026-01-01",
            "content": "Hello.",
            "created_at": "2026-01-01T00:00:00Z",
        })
        assert entry.mood is None
        assert entry.tags is None
        assert entry.title is None
        assert entry.user_id is None

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import DiaryEntry
        with pytest.raises(ValidationError):
            DiaryEntry.model_validate({
                "entry_id": "e1",
                "agent_id": "a1",
                "date": "2026-01-01",
                "content": "Hello.",
                "created_at": "2026-01-01T00:00:00Z",
                "body": "old deprecated field",
            })


# ---------------------------------------------------------------------------
# Batch 5 — Memory Extensions
# ---------------------------------------------------------------------------


class TestMoodAggregateResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import MoodAggregateResponse
        from sonzai._generated.models import MoodAggregateResponse as GenMoodAggregateResponse
        assert MoodAggregateResponse is GenMoodAggregateResponse

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import MoodAggregateResponse
        resp = MoodAggregateResponse.model_validate({
            "valence": 0.6,
            "arousal": 0.4,
            "tension": 0.2,
            "affiliation": 0.8,
            "label": "positive",
            "user_count": 42,
            "days_window": 7,
        })
        assert resp.valence == 0.6
        assert resp.arousal == 0.4
        assert resp.tension == 0.2
        assert resp.affiliation == 0.8
        assert resp.label == "positive"
        assert resp.user_count == 42
        assert resp.days_window == 7

    def test_old_hand_rolled_fields_gone(self) -> None:
        """Hand-rolled had float defaults; generated fields are required (no defaults)."""
        from sonzai import MoodAggregateResponse
        # All 7 spec fields should be present
        for field in ("valence", "arousal", "tension", "affiliation", "label", "user_count", "days_window"):
            assert field in MoodAggregateResponse.model_fields

    def test_schema_field_aliased(self) -> None:
        from sonzai import MoodAggregateResponse
        resp = MoodAggregateResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/MoodAggregateResponse.json",
            "valence": 0.0, "arousal": 0.0, "tension": 0.0,
            "affiliation": 0.0, "label": "", "user_count": 0, "days_window": 0,
        })
        assert resp.field_schema is not None
        assert "MoodAggregateResponse" in str(resp.field_schema)


class TestTimeMachineMoodSnapshotMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import TimeMachineMoodSnapshot
        from sonzai._generated.models import TimeMachineMoodSnapshot as GenTimeMachineMoodSnapshot
        assert TimeMachineMoodSnapshot is GenTimeMachineMoodSnapshot

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import TimeMachineMoodSnapshot
        snap = TimeMachineMoodSnapshot.model_validate({
            "valence": 0.5,
            "arousal": 0.3,
            "tension": 0.1,
            "affiliation": 0.7,
            "label": "calm",
        })
        assert snap.valence == 0.5
        assert snap.arousal == 0.3
        assert snap.tension == 0.1
        assert snap.affiliation == 0.7
        assert snap.label == "calm"

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import TimeMachineMoodSnapshot
        with pytest.raises(ValidationError):
            TimeMachineMoodSnapshot.model_validate({
                "valence": 0.0, "arousal": 0.0, "tension": 0.0,
                "affiliation": 0.0, "label": "", "unknown_field": "boom",
            })


_BIG5_TRAIT_SNAP = {"score": 0.7, "confidence": 0.9}
_BIG5_ASSESSMENT_SNAP = {
    "agreeableness": _BIG5_TRAIT_SNAP,
    "conscientiousness": _BIG5_TRAIT_SNAP,
    "extraversion": _BIG5_TRAIT_SNAP,
    "neuroticism": _BIG5_TRAIT_SNAP,
    "openness": _BIG5_TRAIT_SNAP,
}
_MOOD_SNAP = {"valence": 0.5, "arousal": 0.3, "tension": 0.1, "affiliation": 0.7, "label": "calm"}


class TestTimeMachineResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import TimeMachineResponse
        from sonzai._generated.models import TimeMachineResponse as GenTimeMachineResponse
        assert TimeMachineResponse is GenTimeMachineResponse

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import TimeMachineResponse
        resp = TimeMachineResponse.model_validate({
            "personality_at": _BIG5_ASSESSMENT_SNAP,
            "current_personality": _BIG5_ASSESSMENT_SNAP,
            "evolution_events": None,
            "mood_at": _MOOD_SNAP,
            "requested_at": "2026-01-01T00:00:00Z",
        })
        assert resp.requested_at == "2026-01-01T00:00:00Z"
        assert resp.mood_at.valence == 0.5
        assert resp.mood_at.label == "calm"
        assert resp.personality_at.openness.score == 0.7
        assert resp.current_personality.agreeableness.confidence == 0.9
        assert resp.evolution_events is None

    def test_old_hand_rolled_fields_gone(self) -> None:
        """Hand-rolled had dict[str, Any] for personality_at/current_personality;
        generated uses Big5Assessment with typed fields."""
        from sonzai import TimeMachineResponse
        from sonzai._generated.models import Big5Assessment
        import inspect
        hints = TimeMachineResponse.model_fields
        assert "personality_at" in hints
        assert "current_personality" in hints
        # Verify these are Big5Assessment, not dict
        assert hints["personality_at"].annotation is Big5Assessment

    def test_schema_field_aliased(self) -> None:
        from sonzai import TimeMachineResponse
        resp = TimeMachineResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/TimeMachineResponse.json",
            "personality_at": _BIG5_ASSESSMENT_SNAP,
            "current_personality": _BIG5_ASSESSMENT_SNAP,
            "evolution_events": None,
            "mood_at": _MOOD_SNAP,
            "requested_at": "2026-01-01T00:00:00Z",
        })
        assert resp.field_schema is not None
        assert "TimeMachineResponse" in str(resp.field_schema)


class TestMemorySummaryMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import MemorySummary
        from sonzai._generated.models import MemorySummary as GenMemorySummary
        assert MemorySummary is GenMemorySummary

    def test_minimal_required_roundtrip(self) -> None:
        from sonzai import MemorySummary
        ms = MemorySummary.model_validate({
            "summary_id": "sum_1",
            "agent_id": "a1",
            "stage": "consolidation",
            "summary": "The user discussed hobbies and goals.",
            "period_start": "2026-01-01T00:00:00Z",
            "period_end": "2026-01-07T23:59:59Z",
            "created_at": "2026-01-08T00:00:00Z",
        })
        assert ms.summary_id == "sum_1"
        assert ms.agent_id == "a1"
        assert ms.stage == "consolidation"
        assert ms.summary == "The user discussed hobbies and goals."
        assert ms.period_start is not None
        assert ms.period_end is not None
        assert ms.created_at is not None

    def test_old_hand_rolled_fields_gone(self) -> None:
        """Hand-rolled had summary_text/timestamp/fact_count/confidence;
        generated uses summary/summary_id/period_start/period_end/created_at."""
        from sonzai import MemorySummary
        assert "summary_id" in MemorySummary.model_fields
        assert "summary" in MemorySummary.model_fields
        assert "period_start" in MemorySummary.model_fields
        assert "period_end" in MemorySummary.model_fields
        assert "created_at" in MemorySummary.model_fields
        assert "summary_text" not in MemorySummary.model_fields
        assert "timestamp" not in MemorySummary.model_fields
        assert "fact_count" not in MemorySummary.model_fields

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import MemorySummary
        with pytest.raises(ValidationError):
            MemorySummary.model_validate({
                "summary_id": "x", "agent_id": "a1", "stage": "s",
                "summary": "text",
                "period_start": "2026-01-01T00:00:00Z",
                "period_end": "2026-01-07T00:00:00Z",
                "created_at": "2026-01-08T00:00:00Z",
                "unknown_field": "boom",
            })


class TestSummariesResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import SummariesResponse
        from sonzai._generated.models import SummariesResponse as GenSummariesResponse
        assert SummariesResponse is GenSummariesResponse

    def test_minimal_required_roundtrip_none(self) -> None:
        from sonzai import SummariesResponse
        resp = SummariesResponse.model_validate({"summaries": None})
        assert resp.summaries is None

    def test_with_summaries(self) -> None:
        from sonzai import SummariesResponse
        resp = SummariesResponse.model_validate({
            "summaries": [{
                "summary_id": "sum_1",
                "agent_id": "a1",
                "stage": "consolidation",
                "summary": "text",
                "period_start": "2026-01-01T00:00:00Z",
                "period_end": "2026-01-07T00:00:00Z",
                "created_at": "2026-01-08T00:00:00Z",
            }],
        })
        assert resp.summaries is not None
        assert len(resp.summaries) == 1
        assert resp.summaries[0].summary_id == "sum_1"
        assert resp.summaries[0].summary == "text"

    def test_schema_field_aliased(self) -> None:
        from sonzai import SummariesResponse
        resp = SummariesResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/SummariesResponse.json",
            "summaries": None,
        })
        assert resp.field_schema is not None
        assert "SummariesResponse" in str(resp.field_schema)


class TestPersonalityShiftMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import PersonalityShift
        from sonzai._generated.models import PersonalityShift as GenPersonalityShift
        assert PersonalityShift is GenPersonalityShift

    def test_required_fields_roundtrip(self) -> None:
        from sonzai import PersonalityShift
        shift = PersonalityShift.model_validate({
            "trait_name": "openness",
            "direction": "increase",
            "magnitude": "moderate",
            "trigger_types": ["conversation"],
            "timeframe_days": 30,
        })
        assert shift.trait_name == "openness"
        assert shift.direction == "increase"
        assert shift.magnitude == "moderate"
        assert shift.trigger_types == ["conversation"]
        assert shift.timeframe_days == 30

    def test_optional_fields(self) -> None:
        from sonzai import PersonalityShift
        shift = PersonalityShift.model_validate({
            "trait_name": "conscientiousness",
            "direction": "decrease",
            "magnitude": "slight",
            "trigger_types": None,
            "timeframe_days": 7,
            "reasoning": "gradual change",
            "timestamp": "2026-04-01T00:00:00Z",
        })
        assert shift.reasoning == "gradual change"
        assert shift.trigger_types is None

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import PersonalityShift
        with pytest.raises(ValidationError):
            PersonalityShift.model_validate({
                "trait_name": "openness",
                "direction": "increase",
                "magnitude": "moderate",
                "trigger_types": [],
                "timeframe_days": 10,
                "unknown": "boom",
            })


class TestRecentShiftsResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import RecentShiftsResponse
        from sonzai._generated.models import RecentShiftsResponse as GenRecentShiftsResponse
        assert RecentShiftsResponse is GenRecentShiftsResponse

    def test_minimal_required_roundtrip_none(self) -> None:
        from sonzai import RecentShiftsResponse
        resp = RecentShiftsResponse.model_validate({"shifts": None})
        assert resp.shifts is None

    def test_with_shifts(self) -> None:
        from sonzai import RecentShiftsResponse
        resp = RecentShiftsResponse.model_validate({
            "shifts": [{
                "trait_name": "openness",
                "direction": "increase",
                "magnitude": "moderate",
                "trigger_types": ["event"],
                "timeframe_days": 14,
            }],
        })
        assert resp.shifts is not None
        assert len(resp.shifts) == 1
        assert resp.shifts[0].trait_name == "openness"

    def test_schema_field_aliased(self) -> None:
        from sonzai import RecentShiftsResponse
        resp = RecentShiftsResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/RecentShiftsResponse.json",
            "shifts": None,
        })
        assert resp.field_schema is not None
        assert "RecentShiftsResponse" in str(resp.field_schema)


class TestSignificantMomentMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import SignificantMoment
        from sonzai._generated.models import SignificantMoment as GenSignificantMoment
        assert SignificantMoment is GenSignificantMoment

    def test_required_fields_roundtrip(self) -> None:
        from sonzai import SignificantMoment
        moment = SignificantMoment.model_validate({
            "description": "First meeting",
            "reasoning": "Strong emotional impact",
            "trigger_type": "conversation",
            "created_at": "2026-04-01T00:00:00Z",
        })
        assert moment.description == "First meeting"
        assert moment.reasoning == "Strong emotional impact"
        assert moment.trigger_type == "conversation"
        assert moment.created_at == "2026-04-01T00:00:00Z"

    def test_optional_fields(self) -> None:
        from sonzai import SignificantMoment
        moment = SignificantMoment.model_validate({
            "description": "A walk in the park",
            "reasoning": "Shared experience",
            "trigger_type": "event",
            "created_at": "2026-04-10T00:00:00Z",
            "emotional_impact": "positive",
            "location": "Central Park",
            "partner_name": "Alex",
            "traits_affected": ["openness", "agreeableness"],
        })
        assert moment.emotional_impact == "positive"
        assert moment.location == "Central Park"
        assert moment.traits_affected == ["openness", "agreeableness"]

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import SignificantMoment
        with pytest.raises(ValidationError):
            SignificantMoment.model_validate({
                "description": "x",
                "reasoning": "y",
                "trigger_type": "z",
                "created_at": "2026-01-01T00:00:00Z",
                "unknown": "boom",
            })


class TestSignificantMomentsResponseMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import SignificantMomentsResponse
        from sonzai._generated.models import SignificantMomentsResponse as GenSignificantMomentsResponse
        assert SignificantMomentsResponse is GenSignificantMomentsResponse

    def test_minimal_required_roundtrip_none(self) -> None:
        from sonzai import SignificantMomentsResponse
        resp = SignificantMomentsResponse.model_validate({"moments": None})
        assert resp.moments is None

    def test_with_moments(self) -> None:
        from sonzai import SignificantMomentsResponse
        resp = SignificantMomentsResponse.model_validate({
            "moments": [{
                "description": "First meeting",
                "reasoning": "Impact",
                "trigger_type": "conversation",
                "created_at": "2026-04-01T00:00:00Z",
            }],
        })
        assert resp.moments is not None
        assert len(resp.moments) == 1
        assert resp.moments[0].description == "First meeting"

    def test_schema_field_aliased(self) -> None:
        from sonzai import SignificantMomentsResponse
        resp = SignificantMomentsResponse.model_validate({
            "$schema": "https://api.sonz.ai/api/v1/schemas/SignificantMomentsResponse.json",
            "moments": None,
        })
        assert resp.field_schema is not None
        assert "SignificantMomentsResponse" in str(resp.field_schema)


class TestBatchPersonalityEntryMigration:
    def test_imports_from_generated(self) -> None:
        from sonzai import BatchPersonalityEntry
        from sonzai._generated.models import BatchPersonalityEntry as GenBatchPersonalityEntry
        assert BatchPersonalityEntry is GenBatchPersonalityEntry

    def test_required_fields_present(self) -> None:
        from sonzai import BatchPersonalityEntry
        assert "profile" in BatchPersonalityEntry.model_fields
        assert "evolution_count" in BatchPersonalityEntry.model_fields

    def test_extra_fields_forbidden(self) -> None:
        from sonzai import BatchPersonalityEntry
        # model_config should have extra='forbid'
        assert BatchPersonalityEntry.model_config.get("extra") == "forbid"
