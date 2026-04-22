"""Evaluation customizations."""

from sonzai._generated.models import EvalRun as _GenEvalRun


class EvalRun(_GenEvalRun):
    """Evaluation run record. Adds a .id alias that returns .run_id for
    backwards compatibility with the SDK's historical shape.
    """

    @property
    def id(self) -> str:
        return self.run_id
