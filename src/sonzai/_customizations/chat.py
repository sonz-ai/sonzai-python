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

from pydantic import ConfigDict, Field, TypeAdapter

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

    # Override the generated `error` field (ChatSSEChunkError, which has
    # extra="forbid" and only `message`) with a free-form Any so that
    # error frames with additional server fields (e.g. `code`) are accepted.
    error: Any = None

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
_ChatStreamEventUnion = Union[
    ChatDeltaEvent,
    ChatContextReadyEvent,
    ChatSideEffectsEvent,
    ChatMessageBoundaryEvent,
    ChatCompleteEvent,
    ChatErrorEvent,
]

# Lazy-initialized TypeAdapter for backward-compat model_validate shim.
_adapter: "TypeAdapter[_ChatStreamEventUnion] | None" = None


def _get_adapter() -> "TypeAdapter[_ChatStreamEventUnion]":
    global _adapter
    if _adapter is None:
        _adapter = TypeAdapter(_ChatStreamEventUnion)
    return _adapter


class _ChatStreamEventMeta:
    """Namespace that makes ``ChatStreamEvent.model_validate(...)`` work.

    ``ChatStreamEvent`` is a Union type alias for static type-checkers, but
    existing call-sites (agents.py) call ``ChatStreamEvent.model_validate``
    or construct it directly.  This shim forwards those calls so that
    agents.py keeps working until Task 2 replaces the construction sites.
    """

    def __new__(cls, **kwargs: Any) -> "ChatDeltaEvent":  # type: ignore[misc]
        # Backward compat: ``ChatStreamEvent(field=value, ...)`` constructs
        # a ChatDeltaEvent, which is the most general concrete subclass.
        return ChatDeltaEvent(**kwargs)

    @classmethod
    def model_validate(cls, obj: Any) -> _ChatStreamEventUnion:  # type: ignore[return]
        return _get_adapter().validate_python(obj)

    def __class_getitem__(cls, item: Any) -> Any:
        return _ChatStreamEventUnion[item]  # type: ignore[index]


# ChatStreamEvent is exposed as the Union to type-checkers via the annotation,
# but at runtime it is the shim class so that `ChatStreamEvent.model_validate`
# keeps working until agents.py is updated in Task 2.
ChatStreamEvent: type[_ChatStreamEventUnion] = _ChatStreamEventMeta  # type: ignore[assignment]
