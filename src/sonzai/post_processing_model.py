"""Shared types and helpers for the post-processing model resolver.

Used by both :mod:`sonzai.resources.project_config` and
:mod:`sonzai.resources.account_config` to read/write the
``post_processing_model_map`` config key defined by the server — see
``sonzai-ai-monolith-ts/docs/post-processing-model-mapping.md``.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


POST_PROCESSING_MODEL_MAP_KEY = "post_processing_model_map"
"""Config key under which the chat-model → post-processing-model map is
stored at both the project and account scope. All cascade layers read the
same key."""


POST_PROCESSING_WILDCARD_KEY = "*"
"""Per-layer wildcard. Entries keyed on ``"*"`` apply to any chat model
that has no explicit entry at the same layer."""


class PostProcessingModelEntry(BaseModel):
    """One entry in a post-processing model map.

    The cheaper model that latency-insensitive batch work routes to when
    the agent's chat turn uses a particular model. Sampling
    (``temperature``, ``max_tokens``) is intentionally omitted — the server
    inherits it from the chat ``ModelConfig``.
    """

    provider: str
    model: str


# A PostProcessingModelMap is a plain dict chat_model → entry. Pydantic
# could wrap it in a container, but staying dict-shaped means callers
# can write map literals without constructing envelope classes.
PostProcessingModelMap = dict[str, PostProcessingModelEntry]


def decode_post_processing_map(value: Any) -> PostProcessingModelMap | None:
    """Decode a raw config value into a typed :data:`PostProcessingModelMap`.

    Returns ``None`` when the value is missing or cannot be interpreted as a
    map — callers should treat both cases as ""no map configured"".

    The parse is defensive: entries with missing or empty ``provider`` /
    ``model`` are dropped rather than raising, so a partially-corrupt config
    doesn't prevent the rest from resolving.
    """
    if value is None:
        return None
    if not isinstance(value, dict):
        return None

    out: PostProcessingModelMap = {}
    for chat_model, entry in value.items():
        if not isinstance(entry, dict):
            continue
        provider = entry.get("provider")
        model = entry.get("model")
        if not isinstance(provider, str) or not isinstance(model, str):
            continue
        if not model:
            continue
        out[chat_model] = PostProcessingModelEntry(
            provider=provider, model=model
        )
    return out
