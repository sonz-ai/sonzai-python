"""Composio resource for the Sonzai SDK.

Per-agent connected SaaS accounts (Gmail, Calendar, Slack, GitHub,
Linear, Notion, Drive). Gated on the ``Composio`` agent capability.
Deployments without ``COMPOSIO_API_KEY`` return 503 from every
endpoint; the SDK surface stays stable so callers can detect
"not configured" cleanly.
"""

from __future__ import annotations

from .._generated.resources.composio import AsyncComposio as _GenAsyncComposio
from .._generated.resources.composio import Composio as _GenComposio


class Composio(_GenComposio):
    """Sync Composio connection + audit + available-actions operations."""


class AsyncComposio(_GenAsyncComposio):
    """Async Composio connection + audit + available-actions operations."""


__all__ = ["Composio", "AsyncComposio"]
