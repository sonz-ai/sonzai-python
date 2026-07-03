"""Well-known platform event-type constants.

These string identifiers name events that notification channels (see
:mod:`sonzai.resources.channels`) and webhooks can subscribe to. Use the
constants instead of bare string literals so callers get a single source of
truth and IDE discoverability.
"""

from __future__ import annotations

BUILTIN_AGENT_COMPLETED = "builtin_agent.completed"
CONVERSATION_MESSAGE = "conversation.message"
CONVERSATION_MESSAGE_FAILED = "conversation.message.failed"
CONVERSATION_STARTED = "conversation.started"
CONVERSATION_TAKEOVER_RELEASED = "conversation.takeover.released"
CONVERSATION_TAKEOVER_STARTED = "conversation.takeover.started"
CONVERSATION_UNROUTED = "conversation.unrouted"
LEAD_ENRICHED = "lead.enriched"

__all__ = [
    "BUILTIN_AGENT_COMPLETED",
    "CONVERSATION_MESSAGE",
    "CONVERSATION_MESSAGE_FAILED",
    "CONVERSATION_STARTED",
    "CONVERSATION_TAKEOVER_RELEASED",
    "CONVERSATION_TAKEOVER_STARTED",
    "CONVERSATION_UNROUTED",
    "LEAD_ENRICHED",
]
