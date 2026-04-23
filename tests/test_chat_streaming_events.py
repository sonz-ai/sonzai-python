"""Tests for typed chat streaming event subclasses."""

from __future__ import annotations

import pytest

from sonzai._customizations.chat import (
    ChatCompleteEvent,
    ChatContextReadyEvent,
    ChatDeltaEvent,
    ChatErrorEvent,
    ChatMessageBoundaryEvent,
    ChatSideEffectsEvent,
)


class TestChatDeltaEvent:
    def test_content_from_delta(self) -> None:
        e = ChatDeltaEvent.model_validate(
            {"choices": [{"delta": {"content": "Hi"}, "index": 0}]}
        )
        assert e.content == "Hi"

    def test_not_finished(self) -> None:
        e = ChatDeltaEvent.model_validate(
            {"choices": [{"delta": {"content": "Hi"}, "index": 0}]}
        )
        assert e.is_finished is False


class TestChatContextReadyEvent:
    def test_build_duration_ms_typed(self) -> None:
        e = ChatContextReadyEvent.model_validate({
            "type": "context_ready",
            "build_duration_ms": 125,
            "used_fast_path": False,
        })
        assert e.build_duration_ms == 125
        assert e.used_fast_path is False


class TestChatSideEffectsEvent:
    def test_data_preserved(self) -> None:
        e = ChatSideEffectsEvent.model_validate({
            "type": "side_effects",
            "data": {"facts": [{"content": "x"}]},
        })
        assert e.data == {"facts": [{"content": "x"}]}


class TestChatMessageBoundaryEvent:
    def test_message_index(self) -> None:
        e = ChatMessageBoundaryEvent.model_validate({
            "type": "message_boundary",
            "message_index": 2,
            "is_follow_up": True,
        })
        assert e.message_index == 2
        assert e.is_follow_up is True


class TestChatCompleteEvent:
    def test_aggregated_fields(self) -> None:
        e = ChatCompleteEvent.model_validate({
            "choices": [{"delta": {}, "finish_reason": "stop", "index": 0}],
            "full_content": "Hello world",
            "finish_reason": "stop",
            "continuation_token": "ct123",
            "response_cookie": "rc456",
            "message_count": 1,
        })
        assert e.full_content == "Hello world"
        assert e.finish_reason == "stop"
        assert e.continuation_token == "ct123"
        assert e.is_finished is True


class TestChatErrorEvent:
    def test_error_fields(self) -> None:
        e = ChatErrorEvent.model_validate({
            "error": {"message": "Rate limit exceeded", "code": "rate_limited"},
            "error_message": "Rate limit exceeded",
            "error_code": "rate_limited",
            "is_token_error": False,
        })
        assert e.error_message == "Rate limit exceeded"
        assert e.error_code == "rate_limited"
        assert e.is_token_error is False


from sonzai._http import _classify_chat_frame


class TestClassifier:
    def test_context_ready(self) -> None:
        e = _classify_chat_frame({"type": "context_ready", "build_duration_ms": 10})
        assert isinstance(e, ChatContextReadyEvent)

    def test_side_effects(self) -> None:
        e = _classify_chat_frame({"type": "side_effects", "data": {}})
        assert isinstance(e, ChatSideEffectsEvent)

    def test_message_boundary(self) -> None:
        e = _classify_chat_frame({"type": "message_boundary", "message_index": 1})
        assert isinstance(e, ChatMessageBoundaryEvent)

    def test_error_frame(self) -> None:
        e = _classify_chat_frame({"error": {"message": "boom", "code": "x"}})
        assert isinstance(e, ChatErrorEvent)

    def test_complete_frame_from_finish_reason(self) -> None:
        e = _classify_chat_frame({
            "choices": [{"delta": {}, "finish_reason": "stop", "index": 0}],
        })
        assert isinstance(e, ChatCompleteEvent)

    def test_default_is_delta(self) -> None:
        e = _classify_chat_frame({"choices": [{"delta": {"content": "a"}, "index": 0}]})
        assert isinstance(e, ChatDeltaEvent)
