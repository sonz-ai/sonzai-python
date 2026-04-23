"""Skills resource for the Sonzai SDK.

Project-scoped markdown playbooks the agent loads on demand via the
``sonzai_load_skill`` tool. Developers manage the library at the project
level; each agent opts into individual skills via the enablement surface.
The ``AutoLearnSkills`` capability lets the agent author its own skills
at runtime via ``sonzai_create_skill``.
"""

from __future__ import annotations

from .._generated.resources.skills import AsyncSkills as _GenAsyncSkills
from .._generated.resources.skills import Skills as _GenSkills


class Skills(_GenSkills):
    """Sync skill library + per-agent enablement operations."""


class AsyncSkills(_GenAsyncSkills):
    """Async skill library + per-agent enablement operations."""


__all__ = ["Skills", "AsyncSkills"]
