# Step 3 A.4: Typed Streaming Events Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `ChatStreamEvent` from "one class with every possible field" into a discriminated union of concrete event types (`ChatDeltaEvent`, `ChatContextReadyEvent`, `ChatSideEffectsEvent`, `ChatMessageBoundaryEvent`, `ChatCompleteEvent`, `ChatErrorEvent`).

**Architecture:** Split `src/sonzai/_customizations/chat.py` into multiple subclasses, one per frame type. `ChatStreamEvent` becomes a type alias for the union. A `_classify_chat_frame(dict)` function in `src/sonzai/_http.py` inspects the raw frame shape and constructs the right subclass. `isinstance` / `match` in user code narrows to concrete types.

**Tech Stack:** pydantic v2 (subclasses already work), Python 3.11+ `match` statement, no new runtime deps.

---

## File Structure

**Created:**
- `tests/test_chat_streaming_events.py` — classifier + each subclass behavior

**Modified:**
- `src/sonzai/_customizations/chat.py` — add 5 new subclasses; repurpose current class as `ChatDeltaEvent`; add union alias
- `src/sonzai/_http.py` — add `_classify_chat_frame`; route SSE stream reads through it
- `src/sonzai/__init__.py` — export the 6 concrete event classes
- `src/sonzai/resources/agents.py` — stream return type annotations updated if they reference a concrete union

---

## Task 1: Concrete event subclasses

**Files:**
- Modify: `src/sonzai/_customizations/chat.py`
- Test: `tests/test_chat_streaming_events.py`

- [ ] **Step 1: Write failing unit tests for each subclass**

Create `tests/test_chat_streaming_events.py`:

```python
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
```

- [ ] **Step 2: Run tests — expect ImportError**

Run: `uv run --extra dev pytest tests/test_chat_streaming_events.py -v`
Expected: ImportError on the new class names.

- [ ] **Step 3: Replace `src/sonzai/_customizations/chat.py`**

Overwrite with:

```python
"""Chat streaming event types.

The public `ChatStreamEvent` is a discriminated union over concrete
subclasses. Users should `isinstance(event, ChatDeltaEvent)` or use
`match event:` to narrow — the current-frame's fields are then
typed.

Internal stream reader uses `_classify_chat_frame` (in _http.py) to
construct the right subclass from a raw frame dict.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from pydantic import ConfigDict, Field

from sonzai._generated.models import ChatSSEChunk as _GenChatSSEChunk

if TYPE_CHECKING:
    from sonzai.types import ChatUsage


class _ChatStreamEventBase(_GenChatSSEChunk):
    """Internal base — never construct directly.

    Carries every field that can appear on any frame. Subclasses
    narrow the type semantically; pydantic doesn't enforce which
    fields each subclass uses.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    # Client-side aggregation / extension fields shared across frames:
    is_follow_up: bool = False
    replacement: bool = False
    full_content: str = ""
    finish_reason: str = ""
    continuation_token: str = ""
    response_cookie: str = ""
    message_count: int = 0
    external_tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    error_message: str = ""
    error_code: str = ""
    is_token_error: bool = False
    usage: "ChatUsage | None" = None

    @property
    def content(self) -> str:
        if not self.choices:
            return ""
        delta = self.choices[0].delta
        if delta is None:
            return ""
        return delta.content or ""

    @property
    def is_finished(self) -> bool:
        return bool(self.choices and self.choices[0].finish_reason)


class ChatDeltaEvent(_ChatStreamEventBase):
    """Streaming content delta — the most common frame.

    No `type` on the wire. Use `.content` to read the incremental text.
    """


class ChatContextReadyEvent(_ChatStreamEventBase):
    """Fired once when the context engine has built the prompt context.

    Typed fields: `build_duration_ms`, `used_fast_path`, `enriched_context`.
    """


class ChatSideEffectsEvent(_ChatStreamEventBase):
    """Fired when the turn produced side effects (facts, personality deltas, etc.).

    `data` holds the opaque side-effect payload; inspect it with the
    Process / Extraction types.
    """


class ChatMessageBoundaryEvent(_ChatStreamEventBase):
    """Fired at the start of a new agentic turn (follow-up messages)."""


class ChatCompleteEvent(_ChatStreamEventBase):
    """Terminal frame. `finish_reason` is set; aggregated fields populated."""


class ChatErrorEvent(_ChatStreamEventBase):
    """Error occurred mid-stream. `error_message`/`error_code` populated."""


# Public type alias: a ChatStreamEvent is any of these concrete subclasses.
# Users annotate method returns as `Iterator[ChatStreamEvent]` and match
# on `isinstance(event, ChatXxxEvent)` to narrow.
ChatStreamEvent = Union[
    ChatDeltaEvent,
    ChatContextReadyEvent,
    ChatSideEffectsEvent,
    ChatMessageBoundaryEvent,
    ChatCompleteEvent,
    ChatErrorEvent,
]
```

- [ ] **Step 4: Run tests — all pass**

Run: `uv run --extra dev pytest tests/test_chat_streaming_events.py -v`
Expected: All 6 classes import and validate; their tests pass.

- [ ] **Step 5: Run full suite**

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: Existing `tests/test_customizations.py::TestChatStreamEvent` and `tests/test_types.py::TestChatStreamEvent` tests should still pass — they use `ChatStreamEvent.model_validate(...)`. Since `ChatStreamEvent` is now a Union, pydantic won't accept it as a class directly. **This is a breaking API.** If existing tests fail with "cannot instantiate Union", the next task (classifier) has not yet replaced the call path; the test file may need a one-line swap to `ChatDeltaEvent.model_validate(...)` since that's the default fall-through.

If tests fail, fix them surgically: tests that construct a raw frame dict and assert `event.content` should use `ChatDeltaEvent.model_validate`; tests that check `is_finished` use `ChatCompleteEvent.model_validate`. Keep the behavior tests exactly as they were.

Run: `uv run --extra dev pytest 2>&1 | tail -3` after test fixes.
Expected: All pass.

- [ ] **Step 6: Commit**

```bash
git add src/sonzai/_customizations/chat.py tests/test_chat_streaming_events.py tests/test_customizations.py tests/test_types.py
git commit -m "feat: split ChatStreamEvent into typed subclasses

Replaces the single-class-with-every-field ChatStreamEvent with a
union of six concrete subclasses (Delta, ContextReady, SideEffects,
MessageBoundary, Complete, Error). The public name ChatStreamEvent is
now a type alias for the Union — annotate method returns with it and
match on isinstance() to narrow.

BREAKING: ChatStreamEvent.model_validate no longer works (Union isn't
constructible). Swap to the correct concrete subclass at call sites
(most are in the stream reader and will be replaced by the classifier
in the next commit)."
```

---

## Task 2: Classifier in `_http.py` + streaming pipeline

**Files:**
- Modify: `src/sonzai/_http.py`
- Modify: `src/sonzai/resources/agents.py`

- [ ] **Step 1: Write a classifier unit test**

Append to `tests/test_chat_streaming_events.py`:

```python
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
```

- [ ] **Step 2: Run test — expect ImportError**

Run: `uv run --extra dev pytest tests/test_chat_streaming_events.py::TestClassifier -v`
Expected: ImportError — `_classify_chat_frame` doesn't exist.

- [ ] **Step 3: Add `_classify_chat_frame` to `src/sonzai/_http.py`**

Near the top of `_http.py` (after imports), add:

```python
from ._customizations.chat import (
    ChatCompleteEvent,
    ChatContextReadyEvent,
    ChatDeltaEvent,
    ChatErrorEvent,
    ChatMessageBoundaryEvent,
    ChatSideEffectsEvent,
    ChatStreamEvent,   # Union alias, for type hints
)


def _classify_chat_frame(frame: dict[str, Any]) -> ChatStreamEvent:
    """Classify a raw SSE frame dict into the correct ChatXxxEvent subclass."""
    if frame.get("error"):
        return ChatErrorEvent.model_validate(frame)
    frame_type = frame.get("type")
    if frame_type == "context_ready":
        return ChatContextReadyEvent.model_validate(frame)
    if frame_type == "side_effects":
        return ChatSideEffectsEvent.model_validate(frame)
    if frame_type == "message_boundary":
        return ChatMessageBoundaryEvent.model_validate(frame)
    if frame.get("finish_reason") or frame.get("full_content"):
        return ChatCompleteEvent.model_validate(frame)
    if frame.get("choices"):
        choices = frame.get("choices") or []
        if choices and isinstance(choices[0], dict) and choices[0].get("finish_reason"):
            return ChatCompleteEvent.model_validate(frame)
    return ChatDeltaEvent.model_validate(frame)
```

- [ ] **Step 4: Replace stream-reader call sites**

Find every `ChatStreamEvent.model_validate(frame)` call in `_http.py` and `resources/agents.py`:

```bash
grep -rn "ChatStreamEvent.model_validate" src/
```

Each hit becomes `_classify_chat_frame(frame)`. In `agents.py`, ensure `_classify_chat_frame` is imported from `.._http` (internal import path).

- [ ] **Step 5: Run classifier tests + full suite**

Run: `uv run --extra dev pytest tests/test_chat_streaming_events.py -v`
Expected: All classifier tests pass.

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: All tests pass. Any remaining test that used `ChatStreamEvent.model_validate` needs swapping; surgical field-name-level updates only.

- [ ] **Step 6: Commit**

```bash
git add src/sonzai/_http.py src/sonzai/resources/agents.py tests/test_chat_streaming_events.py
git commit -m "feat: SSE classifier builds typed chat events from raw frames

_classify_chat_frame inspects frame shape (type, error, finish_reason,
choices) and constructs the matching Chat*Event subclass. All call
sites swapped from ChatStreamEvent.model_validate to the classifier.
Users iterate over \`Iterator[ChatStreamEvent]\` and isinstance-narrow."
```

---

## Task 3: Export subclasses at top level

**Files:**
- Modify: `src/sonzai/__init__.py`

- [ ] **Step 1: Add failing import test**

Append to `tests/test_chat_streaming_events.py`:

```python
class TestPublicExports:
    def test_all_event_subclasses_importable(self) -> None:
        from sonzai import (
            ChatCompleteEvent,
            ChatContextReadyEvent,
            ChatDeltaEvent,
            ChatErrorEvent,
            ChatMessageBoundaryEvent,
            ChatSideEffectsEvent,
            ChatStreamEvent,
        )
        from typing import get_args
        # Union includes all six:
        names = {t.__name__ for t in get_args(ChatStreamEvent)}
        assert names == {
            "ChatDeltaEvent", "ChatContextReadyEvent", "ChatSideEffectsEvent",
            "ChatMessageBoundaryEvent", "ChatCompleteEvent", "ChatErrorEvent",
        }
```

- [ ] **Step 2: Run — expect ImportError on the new names**

Run: `uv run --extra dev pytest tests/test_chat_streaming_events.py::TestPublicExports -v`
Expected: ImportError.

- [ ] **Step 3: Update `src/sonzai/__init__.py`**

Find the existing `from ._customizations import AgentCapabilities, ChatStreamEvent, StoredFact` line. Extend:

```python
from ._customizations import AgentCapabilities, StoredFact
from ._customizations.chat import (
    ChatCompleteEvent,
    ChatContextReadyEvent,
    ChatDeltaEvent,
    ChatErrorEvent,
    ChatMessageBoundaryEvent,
    ChatSideEffectsEvent,
    ChatStreamEvent,
)
```

Add to `__all__` (alphabetical):
```python
    "ChatCompleteEvent",
    "ChatContextReadyEvent",
    "ChatDeltaEvent",
    "ChatErrorEvent",
    "ChatMessageBoundaryEvent",
    "ChatSideEffectsEvent",
    # ChatStreamEvent already there
```

- [ ] **Step 4: Run tests**

Run: `uv run --extra dev pytest 2>&1 | tail -3`
Expected: All pass.

- [ ] **Step 5: Commit**

```bash
git add src/sonzai/__init__.py
git commit -m "feat: export typed chat event subclasses at top level

\`from sonzai import ChatDeltaEvent, ChatSideEffectsEvent, ...\` now
works. Users match on isinstance() to narrow; IDEs autocomplete the
per-frame typed fields."
```

---

## Self-Review Findings

- **Spec 6 subclasses** — Task 1 defines all 6.
- **Spec classifier** — Task 2 defines `_classify_chat_frame` exactly as specified.
- **Spec shape-matching fallback** — classifier's last check handles frames without `type` by inspecting choices/finish_reason/error.
- **Spec `ChatStreamEvent` as union alias** — Task 1 creates the alias; Task 3 exports it.
- **Spec out-of-scope: voice streaming** — plan respects that, no voice changes.

**Placeholder scan**: no TBDs; every code block is complete.

**Type consistency**: `ChatStreamEvent` Union membership stable across tasks. Classifier return type matches the Union.
