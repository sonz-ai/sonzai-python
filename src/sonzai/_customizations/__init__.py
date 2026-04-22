"""Hand-written enhancements layered on top of spec-generated models.

Pattern:
    from sonzai._generated.models import Foo as _GenFoo

    class Foo(_GenFoo):
        '''Docstring for public Foo.'''

        @property
        def convenience(self) -> str:
            return self.some_field or ""

Every class here is subclassed from `sonzai._generated.models`. The
re-export below is what `sonzai/__init__.py` imports from.

Types with no spec counterpart (e.g., client-side aggregations like
`ChatUsage` built from SSE frames) stay in `sonzai.types` — they are not
in scope for this package.
"""

from .agents import AgentCapabilities
from .chat import ChatStreamEvent
from .memory import StoredFact

__all__ = [
    "AgentCapabilities",
    "ChatStreamEvent",
    "StoredFact",
]
