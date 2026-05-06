"""SSE chunked-payload helpers.

When a JSON payload exceeds *max_chunk_size* bytes, the producer splits it into
multiple SSE ``data:`` frames, each wrapped in a ``__chunk`` envelope::

    data: {"__chunk":{"index":0,"total":3},"data":"...partial json..."}
    data: {"__chunk":{"index":1,"total":3},"data":"...partial json..."}
    data: {"__chunk":{"index":2,"total":3},"data":"...partial json..."}

The consumer detects the ``__chunk`` key, buffers fragments, and when all
chunks have arrived it concatenates the ``data`` strings, parses the result
as JSON, and delivers the reassembled object as a single event.

Non-chunked events pass through unchanged (backward compatible).
"""

from __future__ import annotations

import json
import math
from typing import Any

DEFAULT_MAX_CHUNK_SIZE: int = 256 * 1024  # 256 KiB


def chunk_payload(
    payload: dict[str, Any],
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
) -> list[str]:
    """Serialize *payload* into one or more SSE ``data:`` frames.

    If the JSON representation fits within *max_chunk_size* bytes, a single
    un-enveloped frame is returned.  Otherwise the JSON string is split into
    *max_chunk_size*-sized pieces and each piece is wrapped in a ``__chunk``
    envelope so the consumer can reassemble them.

    Returns a list of ready-to-send SSE strings, each ending with ``\\n\\n``.
    """
    raw = json.dumps(payload, separators=(",", ":"))

    if len(raw.encode("utf-8")) <= max_chunk_size:
        return [f"data: {raw}\n\n"]

    # Split the raw JSON string into chunks.
    # We need to account for the envelope overhead when sizing each piece.
    # Envelope template: {"__chunk":{"index":N,"total":N},"data":""}
    # A conservative upper bound for envelope overhead (index/total can be
    # multi-digit, but are always tiny relative to the payload).
    envelope_overhead = 100  # bytes, generous
    piece_size = max(1, max_chunk_size - envelope_overhead)
    total = math.ceil(len(raw) / piece_size)

    frames: list[str] = []
    for i in range(total):
        piece = raw[i * piece_size : (i + 1) * piece_size]
        envelope = json.dumps(
            {"__chunk": {"index": i, "total": total}, "data": piece},
            separators=(",", ":"),
        )
        frames.append(f"data: {envelope}\n\n")

    return frames
