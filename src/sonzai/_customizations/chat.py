"""Chat streaming event, renamed from the spec's ChatSSEChunk."""

from sonzai._generated.models import ChatSSEChunk as _GenChatSSEChunk


class ChatStreamEvent(_GenChatSSEChunk):
    """A single SSE event from the chat stream.

    Renamed from spec's `ChatSSEChunk` for SDK readability. Adds
    convenience properties for the common "get content" / "is this the
    last frame" checks that would otherwise require reaching into
    `.choices[0].delta`.
    """

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
