"""Wisdom resource for the Sonzai SDK.

Attributed-wisdom operations — the cross-user, agent-scoped knowledge
tier gated by the ``WisdomPublicSharing`` capability. Writes go through
a privacy-floor blocklist + an SP1-routed semantic validator so
sensitive categories (compensation, health, politics, etc.) never
persist regardless of provenance. Includes CRUD, directed relations,
bulk import, and a disclosure audit surface.
"""

from __future__ import annotations

from .._generated.resources.wisdom import AsyncWisdom as _GenAsyncWisdom
from .._generated.resources.wisdom import Wisdom as _GenWisdom


class Wisdom(_GenWisdom):
    """Sync attributed-wisdom operations."""


class AsyncWisdom(_GenAsyncWisdom):
    """Async attributed-wisdom operations."""


__all__ = ["Wisdom", "AsyncWisdom"]
