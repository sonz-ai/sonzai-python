"""Sonzai ML & RL resource.

The Sonzai ML resource exposes the platform's generalized, multi-tenant /
multi-vertical ML & RL primitives: supervised scoring (train + calibrated
predict), contextual-bandit next-best-action (decide + learn), off-policy
evaluation, an end-to-end learning simulation, and a single unified feedback
call. Every endpoint is keyed by a free-form ``use_case`` string (e.g.
``"lead_score"``, ``"claim_triage"``, ``"churn"``) so a single tenant can run
many independent models. All calls are tenant-scoped server-side by the API
key — no tenant argument is needed.

Endpoints live under ``/api/v1/builtin-agents/ml/{use_case}/...``.

``train_scoring`` and ``simulate_rounds`` are long-running jobs — training on
large batches and the end-to-end simulation both run for tens of seconds to
minutes — so they apply the same 15-minute per-request timeout the built-in
agent invoke surface uses (override via ``timeout=``). The remaining calls are
fast online operations and use the client's default timeout.

These endpoints are not in the committed OpenAPI snapshot yet, so this resource
is fully hand-written (no ``_generated`` base class) — same posture as the
``builtin_agents`` resource. Mirrors the Go SDK's ``ml.go``
(``TrainScoring`` / ``PredictScore`` / ``DecideNBA`` / ``LearnNBA`` /
``EvaluateOPE`` / ``SimulateRounds`` / ``RecordFeedback``).
"""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    DecideNBAResult,
    EvaluateOPEResult,
    LearnNBAResult,
    PredictScoreResult,
    RecordFeedbackResult,
    SimulateRoundsResult,
    TrainScoringResult,
)

# train_scoring and simulate_rounds are long deep-work jobs (auto-tuned
# training, the full closed-loop simulation). 15 minutes matches the built-in
# agent invoke timeout and the platform-side hard cap on a single run.
DEFAULT_ML_LONG_TIMEOUT_SECONDS = 900.0


def _train_scoring_body(
    rows: list[dict[str, Any]], optimize_budget: int | None
) -> dict[str, Any]:
    body: dict[str, Any] = {"rows": rows}
    if optimize_budget is not None:
        body["optimize_budget"] = optimize_budget
    return body


def _learn_nba_body(
    action_id: str,
    reward: float,
    context: dict[str, Any] | None,
    action_features: dict[str, Any] | None,
    propensity: float | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"action_id": action_id, "reward": reward}
    if context is not None:
        body["context"] = context
    if action_features is not None:
        body["action_features"] = action_features
    if propensity is not None:
        body["propensity"] = propensity
    return body


def _decide_nba_body(
    context: dict[str, Any],
    actions: list[dict[str, Any]],
    explore: bool | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"context": context, "actions": actions}
    if explore is not None:
        body["explore"] = explore
    return body


def _simulate_rounds_body(
    scenario: str | None, rounds: int | None, seed: int | None
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if scenario is not None:
        body["scenario"] = scenario
    if rounds is not None:
        body["rounds"] = rounds
    if seed is not None:
        body["seed"] = seed
    return body


def _record_feedback_body(
    converted: bool,
    subject_id: str | None,
    features: dict[str, Any] | None,
    predicted_score: int | None,
    note: str | None,
    action_id: str | None,
    context: dict[str, Any] | None,
    action_features: dict[str, Any] | None,
    propensity: float | None,
    reward: float | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"converted": converted}
    if subject_id is not None:
        body["subject_id"] = subject_id
    if features is not None:
        body["features"] = features
    if predicted_score is not None:
        body["predicted_score"] = predicted_score
    if note is not None:
        body["note"] = note
    if action_id is not None:
        body["action_id"] = action_id
    if context is not None:
        body["context"] = context
    if action_features is not None:
        body["action_features"] = action_features
    if propensity is not None:
        body["propensity"] = propensity
    if reward is not None:
        body["reward"] = reward
    return body


class ML:
    """Sync operations on the Sonzai ML & RL surface.

    Generalized, use-case-keyed scoring, contextual-bandit next-best-action,
    off-policy evaluation, learning simulation, and unified feedback.

    Example::

        # Train a calibrated scoring model for the "lead_score" use case.
        result = client.ml.train_scoring(
            "lead_score",
            rows=[
                {"features": {"budget": 5_000_000, "intent": 0.8}, "label": 1},
                {"features": {"budget": 200_000, "intent": 0.1}, "label": 0},
            ],
        )
        print(result.auc, result.model_version)

        # Score a single lead.
        pred = client.ml.predict_score("lead_score", features={"budget": 3_000_000})
        print(pred.score)

        # Teach the platform from one realized outcome (the unified call).
        client.ml.record_feedback(
            "lead_score",
            subject_id="lead-42",
            features={"budget": 3_000_000, "intent": 0.7},
            converted=True,
        )
    """

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def train_scoring(
        self,
        use_case: str,
        *,
        rows: list[dict[str, Any]],
        optimize_budget: int | None = None,
        timeout: float = DEFAULT_ML_LONG_TIMEOUT_SECONDS,
    ) -> TrainScoringResult:
        """Train (or retrain) the calibrated scoring model for ``use_case``.

        Returns held-out metrics, the chosen hyperparameters, and the new model
        version. Training can run for a while on large batches — hence the
        15-minute default ``timeout``.

        Args:
            use_case: Free-form use-case key (e.g. ``"lead_score"``).
            rows: Labeled training examples, each ``{"features": {...},
                "label": 0|1}``.
            optimize_budget: Optional cap on the hyperparameter-search trial
                budget. Omit for the platform default.
            timeout: HTTP timeout in seconds for this (long-running) call.
        """
        data = self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/scoring/train",
            json_data=_train_scoring_body(rows, optimize_budget),
            timeout=timeout,
        )
        return TrainScoringResult.model_validate(data)

    def predict_score(
        self, use_case: str, *, features: dict[str, Any]
    ) -> PredictScoreResult:
        """Return the calibrated score for a single example.

        Uses the use case's current scoring model.

        Args:
            use_case: Free-form use-case key.
            features: The example's feature map.
        """
        data = self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/scoring/predict",
            json_data={"features": features},
        )
        return PredictScoreResult.model_validate(data)

    def decide_nba(
        self,
        use_case: str,
        *,
        context: dict[str, Any],
        actions: list[dict[str, Any]],
        explore: bool | None = None,
    ) -> DecideNBAResult:
        """Choose the next best action among a candidate slate.

        Returns the chosen action and the full scored slate. Record the
        returned ``propensity`` and pass it back to :meth:`learn_nba` when the
        reward is realized.

        Args:
            use_case: Free-form use-case key.
            context: The decision context shared across candidate actions.
            actions: Candidate actions, each ``{"id": str, "features": {...}}``.
            explore: Force exploration on/off; omit to let the policy decide.
        """
        data = self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/nba/decide",
            json_data=_decide_nba_body(context, actions, explore),
        )
        return DecideNBAResult.model_validate(data)

    def learn_nba(
        self,
        use_case: str,
        *,
        action_id: str,
        reward: float,
        context: dict[str, Any] | None = None,
        action_features: dict[str, Any] | None = None,
        propensity: float | None = None,
    ) -> LearnNBAResult:
        """Record the realized reward of a previously taken action.

        Updates the use case's bandit policy.

        Args:
            use_case: Free-form use-case key.
            action_id: The action that was taken.
            reward: The realized reward for the taken action.
            context: The decision context that was used.
            action_features: The taken action's feature map.
            propensity: The probability the policy assigned the taken action at
                decision time (from :attr:`DecideNBAResult.propensity`); pass it
                for unbiased off-policy learning.
        """
        data = self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/nba/learn",
            json_data=_learn_nba_body(
                action_id, reward, context, action_features, propensity
            ),
        )
        return LearnNBAResult.model_validate(data)

    def evaluate_ope(
        self, use_case: str, *, logged: list[dict[str, Any]]
    ) -> EvaluateOPEResult:
        """Run off-policy evaluation against a batch of logged decisions.

        Returns IPS / SNIPS / DR value estimates with a confidence interval and
        the effective sample size.

        Args:
            use_case: Free-form use-case key.
            logged: Logged decisions, each ``{"context": {...}, "action_id":
                str, "propensity": float, "reward": float}``.
        """
        data = self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/ope/evaluate",
            json_data={"logged": logged},
        )
        return EvaluateOPEResult.model_validate(data)

    def simulate_rounds(
        self,
        use_case: str,
        *,
        scenario: str | None = None,
        rounds: int | None = None,
        seed: int | None = None,
        timeout: float = DEFAULT_ML_LONG_TIMEOUT_SECONDS,
    ) -> SimulateRoundsResult:
        """Run the entire self-learning loop end-to-end in one call.

        The platform repeatedly accrues outcomes, retrains the auto-tuned
        scoring model, runs the contextual bandit (decide → reward → learn),
        and off-policy-evaluates the policy on a built-in synthetic scenario,
        then returns the per-round learning curve plus the final model and
        learned policy. Runs for tens of seconds — hence the 15-minute default
        ``timeout``. Self-contained, reproducible (pass ``seed``), and scoped to
        an ephemeral model that never touches production models.

        Args:
            use_case: Free-form use-case key for the ephemeral model.
            scenario: Built-in synthetic world to learn; omit for the default.
            rounds: How many learning rounds to run; omit for the default.
            seed: Make the run reproducible; omit for a fresh cold-start.
            timeout: HTTP timeout in seconds for this (long-running) call.
        """
        data = self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/simulate-rounds",
            json_data=_simulate_rounds_body(scenario, rounds, seed),
            timeout=timeout,
        )
        return SimulateRoundsResult.model_validate(data)

    def record_feedback(
        self,
        use_case: str,
        *,
        converted: bool,
        subject_id: str | None = None,
        features: dict[str, Any] | None = None,
        predicted_score: int | None = None,
        note: str | None = None,
        action_id: str | None = None,
        context: dict[str, Any] | None = None,
        action_features: dict[str, Any] | None = None,
        propensity: float | None = None,
        reward: float | None = None,
    ) -> RecordFeedbackResult:
        """Teach the platform from one realized outcome — the unified call.

        ONE operator call: persists the labeled outcome (scoring retrains on the
        platform schedule) and, when ``action_id`` is given, immediately teaches
        the bandit the realized reward. ``reward`` defaults to
        ``1 if converted else 0``. Prefer this over composing the scoring-outcome
        and :meth:`learn_nba` calls by hand.

        Args:
            use_case: Free-form use-case key.
            converted: The realized binary outcome (``True`` = positive). Required.
            subject_id: Identifies the subject of the outcome (e.g. the lead).
            features: The subject's feature map at decision time; provide it to
                persist a fully-labeled scoring example.
            predicted_score: The score the model predicted, for calibration
                tracking.
            note: Free-form annotation for the outcome.
            action_id: The action that was taken; when set, the bandit is taught.
            context: The bandit decision context that was used.
            action_features: The taken action's feature map.
            propensity: The probability the policy assigned the taken action.
            reward: The realized reward; omit to default to ``converted ? 1 : 0``.
        """
        data = self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/feedback",
            json_data=_record_feedback_body(
                converted,
                subject_id,
                features,
                predicted_score,
                note,
                action_id,
                context,
                action_features,
                propensity,
                reward,
            ),
        )
        return RecordFeedbackResult.model_validate(data)


class AsyncML:
    """Async operations on the Sonzai ML & RL surface.

    Mirror of :class:`ML`; see that class for usage examples.
    """

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def train_scoring(
        self,
        use_case: str,
        *,
        rows: list[dict[str, Any]],
        optimize_budget: int | None = None,
        timeout: float = DEFAULT_ML_LONG_TIMEOUT_SECONDS,
    ) -> TrainScoringResult:
        """Train (or retrain) the calibrated scoring model for ``use_case``."""
        data = await self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/scoring/train",
            json_data=_train_scoring_body(rows, optimize_budget),
            timeout=timeout,
        )
        return TrainScoringResult.model_validate(data)

    async def predict_score(
        self, use_case: str, *, features: dict[str, Any]
    ) -> PredictScoreResult:
        """Return the calibrated score for a single example."""
        data = await self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/scoring/predict",
            json_data={"features": features},
        )
        return PredictScoreResult.model_validate(data)

    async def decide_nba(
        self,
        use_case: str,
        *,
        context: dict[str, Any],
        actions: list[dict[str, Any]],
        explore: bool | None = None,
    ) -> DecideNBAResult:
        """Choose the next best action among a candidate slate."""
        data = await self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/nba/decide",
            json_data=_decide_nba_body(context, actions, explore),
        )
        return DecideNBAResult.model_validate(data)

    async def learn_nba(
        self,
        use_case: str,
        *,
        action_id: str,
        reward: float,
        context: dict[str, Any] | None = None,
        action_features: dict[str, Any] | None = None,
        propensity: float | None = None,
    ) -> LearnNBAResult:
        """Record the realized reward of a previously taken action."""
        data = await self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/nba/learn",
            json_data=_learn_nba_body(
                action_id, reward, context, action_features, propensity
            ),
        )
        return LearnNBAResult.model_validate(data)

    async def evaluate_ope(
        self, use_case: str, *, logged: list[dict[str, Any]]
    ) -> EvaluateOPEResult:
        """Run off-policy evaluation against a batch of logged decisions."""
        data = await self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/ope/evaluate",
            json_data={"logged": logged},
        )
        return EvaluateOPEResult.model_validate(data)

    async def simulate_rounds(
        self,
        use_case: str,
        *,
        scenario: str | None = None,
        rounds: int | None = None,
        seed: int | None = None,
        timeout: float = DEFAULT_ML_LONG_TIMEOUT_SECONDS,
    ) -> SimulateRoundsResult:
        """Run the entire self-learning loop end-to-end in one call."""
        data = await self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/simulate-rounds",
            json_data=_simulate_rounds_body(scenario, rounds, seed),
            timeout=timeout,
        )
        return SimulateRoundsResult.model_validate(data)

    async def record_feedback(
        self,
        use_case: str,
        *,
        converted: bool,
        subject_id: str | None = None,
        features: dict[str, Any] | None = None,
        predicted_score: int | None = None,
        note: str | None = None,
        action_id: str | None = None,
        context: dict[str, Any] | None = None,
        action_features: dict[str, Any] | None = None,
        propensity: float | None = None,
        reward: float | None = None,
    ) -> RecordFeedbackResult:
        """Teach the platform from one realized outcome — the unified call."""
        data = await self._http.post(
            f"/api/v1/builtin-agents/ml/{use_case}/feedback",
            json_data=_record_feedback_body(
                converted,
                subject_id,
                features,
                predicted_score,
                note,
                action_id,
                context,
                action_features,
                propensity,
                reward,
            ),
        )
        return RecordFeedbackResult.model_validate(data)


__all__ = [
    "DEFAULT_ML_LONG_TIMEOUT_SECONDS",
    "ML",
    "AsyncML",
]
