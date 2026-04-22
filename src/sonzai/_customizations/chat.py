"""Chat streaming event, renamed from the spec's ChatSSEChunk.

Adds client-side-only fields that are populated by the stream consumer
from `type` and `data` payloads (not part of the server schema).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict, Field

from sonzai._generated.models import ChatSSEChunk as _GenChatSSEChunk

if TYPE_CHECKING:
    from sonzai.types import ChatUsage


class ChatStreamEvent(_GenChatSSEChunk):
    """A single SSE event from the chat stream.

    Inherits every spec field from `ChatSSEChunk` (choices, data, error,
    type, side_effects, enriched_context, build_duration_ms,
    used_fast_path, message_index). Adds convenience properties for the
    common "get content" / "is this the last frame" checks, plus a set
    of client-side extension fields that the stream consumer in
    `sonzai/_http.py` populates from `data` / `type` payloads for
    ergonomic access.
    """

    # Client-side extensions — populated from `data` / `type` frames by
    # the stream reader, never present on the wire as top-level fields.
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

    # Backward-compat field: not in the spec but used by client-side
    # aggregation code and existing tests.
    # NOTE: ChatUsage is imported only under TYPE_CHECKING to avoid a
    # circular import (chat.py → sonzai.types → _customizations → chat.py).
    # model_rebuild() is called at the bottom of sonzai/types.py once
    # ChatUsage is defined, supplying the concrete type to Pydantic.
    usage: "ChatUsage | None" = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)

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
        # Any non-empty `finish_reason` is a terminal frame:
        # "stop" (natural end), "length" (max tokens), "content_filter"
        # (safety), "tool_calls"/"function_call" (OpenAI-style). Matching
        # only "stop" would leave stream readers spinning past the others.
        return bool(self.choices and self.choices[0].finish_reason)
