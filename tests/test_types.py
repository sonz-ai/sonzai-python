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
                {"node_id": "n1", "title": "Food", "importance": 0.9},
                {"node_id": "n2", "title": "Hobbies", "importance": 0.7},
            ],
            "contents": {
                "n1": [
                    {
                        "fact_id": "f1",
                        "atomic_text": "Loves sushi",
                        "fact_type": "preference",
                        "importance": 0.95,
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
        data = {
            "profile": {
                "agent_id": "a1",
                "name": "Luna",
                "gender": "female",
                "bio": "A curious soul",
                "big5": {
                    "openness": {"score": 0.85, "percentile": 90},
                    "conscientiousness": {"score": 0.6, "percentile": 55},
                    "extraversion": {"score": 0.75, "percentile": 70},
                    "agreeableness": {"score": 0.9, "percentile": 95},
                    "neuroticism": {"score": 0.25, "percentile": 20},
                },
                "dimensions": {
                    "warmth": 8,
                    "energy": 7,
                    "openness": 9,
                    "emotional_depth": 8,
                    "playfulness": 7,
                    "supportiveness": 9,
                    "curiosity": 10,
                    "wisdom": 6,
                },
                "speech_patterns": ["uses ellipses...", "asks questions"],
                "true_interests": ["astronomy", "cooking"],
            },
            "evolution": [
                {
                    "delta_id": "d1",
                    "change": "Became more curious",
                    "reason": "Many exploratory conversations",
                }
            ],
        }
        result = PersonalityResponse.model_validate(data)
        assert result.profile.name == "Luna"
        assert result.profile.big5.openness.score == 0.85
        assert result.profile.dimensions.curiosity == 10
        assert len(result.evolution) == 1


class TestEvalTemplate:
    def test_parse_template(self):
        data = {
            "id": "tpl-1",
            "name": "Empathy Check",
            "scoring_rubric": "Evaluate empathy",
            "categories": [
                {"name": "Emotional Awareness", "weight": 0.5, "criteria": "Shows understanding"},
                {"name": "Response Quality", "weight": 0.5, "criteria": "Appropriate response"},
            ],
        }
        result = EvalTemplate.model_validate(data)
        assert result.name == "Empathy Check"
        assert len(result.categories) == 2
        assert result.categories[0].weight == 0.5
