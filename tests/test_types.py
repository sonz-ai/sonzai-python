"""Tests for Sonzai type models."""

from sonzai.types import (
    AgentInstance,
    ChatStreamEvent,
    ChatUsage,
    EvalTemplate,
    MemoryNode,
    MemoryResponse,
    Notification,
    PersonalityProfile,
    PersonalityResponse,
)


class TestChatStreamEvent:
    def test_content_extraction(self):
        event = ChatStreamEvent.model_validate(
            {"choices": [{"delta": {"content": "Hello"}, "index": 0}]}
        )
        assert event.content == "Hello"

    def test_empty_event(self):
        event = ChatStreamEvent.model_validate({})
        assert event.content == ""
        assert not event.is_finished

    def test_finish_detection(self):
        event = ChatStreamEvent.model_validate(
            {"choices": [{"delta": {"content": "."}, "finish_reason": "stop", "index": 0}]}
        )
        assert event.is_finished

    def test_usage_parsing(self):
        event = ChatStreamEvent.model_validate(
            {
                "choices": [{"delta": {}, "index": 0}],
                "usage": {
                    "promptTokens": 100,
                    "completionTokens": 50,
                    "totalTokens": 150,
                },
            }
        )
        assert event.usage is not None
        assert event.usage.prompt_tokens == 100
        assert event.usage.total_tokens == 150


class TestMemoryResponse:
    def test_parse_with_contents(self):
        data = {
            "nodes": [
                {
                    "node_id": "n1",
                    "agent_id": "a1",
                    "name": "Food",
                    "description": "Food preferences",
                    "path": "root/food",
                    "memory_type": "semantic",
                    "importance": 0.9,
                    "created_at": "2026-01-01T00:00:00Z",
                    "updated_at": "2026-01-01T00:00:00Z",
                },
                {
                    "node_id": "n2",
                    "agent_id": "a1",
                    "name": "Hobbies",
                    "description": "Hobby interests",
                    "path": "root/hobbies",
                    "memory_type": "semantic",
                    "importance": 0.7,
                    "created_at": "2026-01-01T00:00:00Z",
                    "updated_at": "2026-01-01T00:00:00Z",
                },
            ],
            "contents": {
                "n1": [
                    {
                        "fact_id": "f1",
                        "agent_id": "a1",
                        "node_id": "n1",
                        "atomic_text": "Loves sushi",
                        "fact_type": "preference",
                        "importance": 0.95,
                        "confidence": 0.9,
                        "mention_count": 1,
                        "retention_strength": 0.5,
                        "last_confirmed": "2026-01-01T00:00:00Z",
                        "last_retrieved_at": "2026-01-01T00:00:00Z",
                        "created_at": "2026-01-01T00:00:00Z",
                        "updated_at": "2026-01-01T00:00:00Z",
                    }
                ]
            },
        }
        result = MemoryResponse.model_validate(data)
        assert len(result.nodes) == 2
        assert "n1" in result.contents
        assert result.contents["n1"][0].atomic_text == "Loves sushi"


class TestPersonalityResponse:
    def test_parse_full_profile(self):
        _trait = {"score": 0.85, "confidence": 0.9}
        data = {
            "profile": {
                "agent_id": "a1",
                "name": "Luna",
                "gender": "female",
                "bio": "A curious soul",
                "created_at": "2026-01-01T00:00:00Z",
                "temperature": 0.7,
                "speech_patterns": ["uses ellipses...", "asks questions"],
                "true_interests": ["astronomy", "cooking"],
                "true_dislikes": [],
                "primary_traits": ["curious"],
                "big5": {
                    "openness": {"score": 0.85, "confidence": 0.9},
                    "conscientiousness": {"score": 0.6, "confidence": 0.8},
                    "extraversion": {"score": 0.75, "confidence": 0.85},
                    "agreeableness": {"score": 0.9, "confidence": 0.95},
                    "neuroticism": {"score": 0.25, "confidence": 0.75},
                },
                "dimensions": {
                    "intellect": 9.0,
                    "aesthetic": 7.0,
                    "industriousness": 6.0,
                    "orderliness": 5.0,
                    "enthusiasm": 7.0,
                    "assertiveness": 6.0,
                    "compassion": 9.0,
                    "politeness": 8.0,
                    "withdrawal": 3.0,
                    "volatility": 2.0,
                },
                "preferences": {
                    "conversation_pace": "relaxed",
                    "emotional_expression": "open",
                    "formality": "casual",
                    "humor_style": "dry",
                },
                "behaviors": {
                    "conflict_approach": "collaborative",
                    "empathy_style": "reflective",
                    "question_frequency": "moderate",
                    "response_length": "medium",
                },
            },
            "evolution": [
                {
                    "trait_category": "big5",
                    "trait_name": "openness",
                    "old_value": 0.8,
                    "new_value": 0.85,
                    "delta": 0.05,
                    "trigger_type": "conversation",
                    "timestamp": "2026-01-01T00:00:00Z",
                }
            ],
        }
        result = PersonalityResponse.model_validate(data)
        assert result.profile.name == "Luna"
        assert result.profile.big5.openness.score == 0.85
        assert result.profile.dimensions.intellect == 9.0
        assert len(result.evolution) == 1


class TestEvalTemplate:
    def test_parse_template(self):
        data = {
            "template_id": "tpl-1",
            "name": "Empathy Check",
            "description": "Evaluates empathy in responses",
            "template_type": "quality",
            "judge_model": "gpt-4",
            "temperature": 0.3,
            "max_tokens": 8192,
            "scoring_rubric": "Evaluate empathy",
            "is_system": False,
            "categories": [
                {"key": "emotional_awareness", "label": "Emotional Awareness", "prompt_instructions": "Shows understanding"},
                {"key": "response_quality", "label": "Response Quality", "prompt_instructions": "Appropriate response"},
            ],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-02T00:00:00Z",
        }
        result = EvalTemplate.model_validate(data)
        assert result.name == "Empathy Check"
        assert len(result.categories) == 2
        assert result.categories[0].key == "emotional_awareness"
