# Step 3 A.4: Typed Streaming Events Design

**Goal:** Turn `ChatStreamEvent` from a union-of-all-possible-fields into a discriminated union of concrete event classes. Today users write `if event.type == "side_effects": ...` and reach into `event.data` as a dict. After this change, they `isinstance(event, ChatSideEffectsEvent)` and IDE autocompletion narrows the available fields.

**Architecture:** Keep `ChatStreamEvent` as the public type annotation, but internally it becomes a union: `ChatDeltaEvent | ChatContextReadyEvent | ChatSideEffectsEvent | ChatMessageBoundaryEvent | ChatCompleteEvent | ChatErrorEvent`. The stream reader in `_http.py` parses each SSE frame's `type` field and constructs the right subclass. Users still receive one thing from the iterator, but it's typed.

**Tech Stack:** pydantic v2 discriminated unions (`Annotated[Union[...], Field(discriminator="type")]`). No new runtime deps.

---

## Current pain

```python
for event in client.agents.chat(..., stream=True):
    if event.type == "side_effects":
        facts = event.data.get("facts", [])  # data is dict[str, Any]
    elif event.type == "context_ready":
        latency = event.build_duration_ms  # optional int, may be 0
    elif event.is_finished:
        content = event.full_content        # client-side aggregated
```

Every branch reaches into a free-form `data` dict or checks optional fields that only make sense for specific frame types. Typo-prone, no IDE help.

## What users get

```python
from sonzai import (
    ChatStreamEvent,            # the union type
    ChatDeltaEvent,
    ChatContextReadyEvent,
    ChatSideEffectsEvent,
    ChatMessageBoundaryEvent,
    ChatCompleteEvent,
    ChatErrorEvent,
)

for event in client.agents.chat(..., stream=True):
    if isinstance(event, ChatDeltaEvent):
        print(event.content, end="")                       # str
    elif isinstance(event, ChatSideEffectsEvent):
        for fact in event.side_effects.facts:              # typed list[ExtractionFact]
            print(fact.content)
    elif isinstance(event, ChatContextReadyEvent):
        print(f"Context built in {event.build_duration_ms}ms")
    elif isinstance(event, ChatCompleteEvent):
        print(f"\nFinal: {event.full_content}")            # aggregated content
```

Match-statement style also works (Python 3.11+):
```python
match event:
    case ChatDeltaEvent(content=c):
        print(c, end="")
    case ChatSideEffectsEvent(side_effects=se):
        handle(se)
```

## Event class hierarchy

Each subclass inherits from a shared `_ChatStreamEventBase` (internal, not exported) to preserve fields common to every frame (`choices`, `error` fallback, provenance).

| Class | `type` discriminator | Added typed fields |
| --- | --- | --- |
| `ChatDeltaEvent` | *absent or empty* | `content: str` (property over `choices[0].delta.content`) |
| `ChatContextReadyEvent` | `"context_ready"` | `build_duration_ms: int`, `used_fast_path: bool`, `enriched_context: ContextPayload \| None` |
| `ChatSideEffectsEvent` | `"side_effects"` | `side_effects: ProcessSideEffects` (typed), `external_tool_calls: list[ExternalToolCall]` |
| `ChatMessageBoundaryEvent` | `"message_boundary"` | `message_index: int`, `is_follow_up: bool` |
| `ChatCompleteEvent` | *terminal frame* | `full_content: str`, `finish_reason: str`, `continuation_token: str`, `response_cookie: str`, `message_count: int`, `usage: ChatUsage \| None` |
| `ChatErrorEvent` | *from error field* | `error_message: str`, `error_code: str`, `is_token_error: bool` |

`ChatStreamEvent = Annotated[Union[ChatDeltaEvent, ChatContextReadyEvent, ..., ChatErrorEvent], Field(discriminator="type")]` — the public `ChatStreamEvent` is this Annotated alias, so `sonzai.ChatStreamEvent` still imports and type-checks.

## Classifier (in `_http.py`)

Existing stream reader in `_http.py` currently yields `ChatStreamEvent.model_validate(frame)`. New classifier function:

```python
def _classify_chat_frame(frame: dict) -> ChatStreamEvent:
    if frame.get("error"):
        return ChatErrorEvent.model_validate(frame)
    match frame.get("type"):
        case "context_ready":
            return ChatContextReadyEvent.model_validate(frame)
        case "side_effects":
            return ChatSideEffectsEvent.model_validate(frame)
        case "message_boundary":
            return ChatMessageBoundaryEvent.model_validate(frame)
    if frame.get("finish_reason") or frame.get("full_content"):
        return ChatCompleteEvent.model_validate(frame)
    return ChatDeltaEvent.model_validate(frame)
```

Pydantic's discriminator doesn't quite work here because some frames lack a `type` field — we distinguish by shape (`error` present, `finish_reason` present). Hand-classify.

## Backwards compat

- `sonzai.ChatStreamEvent` still importable; now a union alias rather than a single class. `isinstance(x, ChatStreamEvent)` works via `typing.get_args(ChatStreamEvent)` / pydantic TypeAdapter — but most users don't do that. Provide a compatibility helper if needed: `isinstance(x, get_args(ChatStreamEvent))`.
- Old access patterns (`event.content`, `event.is_finished`, `event.full_content`) still work — each subclass exposes the right fields as properties where applicable.
- The old `ChatStreamEvent` class becomes `ChatDeltaEvent` (same fields + properties). Callers using `ChatStreamEvent(...)` to *construct* an event manually (rare) need to pick a concrete subclass.

## Testing

Canonical recordings of real SSE streams in `tests/fixtures/stream_*.jsonl` feed into `_classify_chat_frame` tests. For each expected class, a test:
- `_classify_chat_frame({side_effects frame dict})` → `isinstance(result, ChatSideEffectsEvent)`
- Field access works typed: `result.side_effects.facts` returns a `list[ExtractionFact]`.

Plus integration: `respx` stubs an SSE stream with mixed frames; the iterator yields the right class per frame; narrowing in `isinstance` / `match` branches populates typed attributes.

## Scope check

New: ~6 event subclasses, 1 classifier function, ~15 tests. Modifications: `_customizations/chat.py` (turn `ChatStreamEvent` into an alias), `_http.py` (swap validator for classifier), `sonzai/__init__.py` (export the new subclasses). One plan, ~4 batch tasks.

## Out of scope

- Voice streaming events (separate `VoiceStreamEvent`). Same pattern applies but different event shapes — do as a follow-up (A.4.1?) once chat streaming lands and the pattern is proven.
- SSE reconnection / resume (uses `continuation_token`). That's a distinct feature; not covered here.
