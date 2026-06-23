"""Well-known platform event-type constants.

These string identifiers name events that notification channels (see
:mod:`sonzai.resources.channels`) and webhooks can subscribe to. Use the
constants instead of bare string literals so callers get a single source of
truth and IDE discoverability.
"""

from __future__ import annotations

BUILTIN_AGENT_COMPLETED = "builtin_agent.completed"
LEAD_ENRICHED = "lead.enriched"

__all__ = [
    "BUILTIN_AGENT_COMPLETED",
    "LEAD_ENRICHED",
]
