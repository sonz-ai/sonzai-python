"""Chat streaming event, renamed from the spec's ChatSSEChunk.

Adds client-side-only fields that are populated by the stream consumer
from `type` and `data` payloads (not part of the server schema).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from sonzai._generated.models import ChatSSEChunk as _GenChatSSEChunk


class ChatUsage(BaseModel):
    """Token-usage counters attached to SSE stream events.

    Not part of the ChatSSEChunk spec; populated by the stream consumer
    from usage frames emitted by the server and preserved here for
    backward compatibility with existing callers.
    """

    model_config = ConfigDict(populate_by_name=True)

    prompt_tokens: int = Field(alias="promptTokens", default=0)
    completion_tokens: int = Field(alias="completionTokens", default=0)
    total_tokens: int = Field(alias="totalTokens", default=0)


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
    usage: ChatUsage | None = None

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
        return bool(self.choices and self.choices[0].finish_reason == "stop")
