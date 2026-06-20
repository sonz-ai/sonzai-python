"""Tests for the Sonzai ML & RL resource (``client.ml``).

Pins URL path + HTTP method + request body + response decode for all seven
methods — ``train_scoring``, ``predict_score``, ``decide_nba``, ``learn_nba``,
``evaluate_ope``, ``simulate_rounds``, ``record_feedback`` — on both the sync
and async clients, plus the long-running per-request timeout applied to
``train_scoring`` and ``simulate_rounds``. Follows the ``test_builtin_agents``
respx pattern. Mirrors the Go SDK's ``ml.go`` shapes.
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai
from sonzai.resources.ml import DEFAULT_ML_LONG_TIMEOUT_SECONDS
from sonzai.types import (
    DecideNBAResult,
    EvaluateOPEResult,
    LearnNBAResult,
    PredictScoreResult,
    RecordFeedbackResult,
    SimulateRoundsResult,
    TrainScoringResult,
)


@pytest.fixture
def base_url() -> str:
    return "https://api.test.sonz.ai"


@pytest.fixture
def client(base_url: str) -> Sonzai:
    c = Sonzai(api_key="test-key", base_url=base_url)
    yield c
    c.close()


@pytest.fixture
def async_client(base_url: str) -> AsyncSonzai:
    return AsyncSonzai(api_key="test-key", base_url=base_url)


# ---------------------------------------------------------------------------
# Canonical response bodies (snake_case, mirrors ml.go json tags)
# ---------------------------------------------------------------------------

TRAIN_RESULT = {
    "auc": 0.91,
    "logloss": 0.32,
    "brier": 0.11,
    "brier_uncalibrated": 0.18,
    "brier_baseline": 0.25,
    "ece": 0.04,
    "n": 1200,
    "importances": [
        {"name": "budget", "gain": 0.62},
        {"name": "intent", "gain": 0.38},
    ],
    "best_params": {"depth": 6, "learning_rate": 0.05},
    "calibration_method": "isotonic",
    "trials": 40,
    "model_version": 7,
}

PREDICT_RESULT = {
    "score": 0.83,
    "raw": 0.77,
    "model_version": 7,
    "served_from": "live",
    "calibration_method": "isotonic",
}

DECIDE_RESULT = {
    "action_id": "call_now",
    "propensity": 0.55,
    "scores": [
        {"action_id": "call_now", "score": 0.71, "propensity": 0.55},
        {"action_id": "send_sms", "score": 0.42, "propensity": 0.45},
    ],
    "explore": False,
    "model_n": 318,
}

LEARN_RESULT = {"ok": True, "n": 319}

OPE_RESULT = {
    "ips": 0.61,
    "snips": 0.59,
    "dr": 0.6,
    "ci_low": 0.52,
    "ci_high": 0.68,
    "n": 500,
    "ess": 213.4,
    "estimator_ci": "dr",
}

SIMULATE_RESULT = {
    "scenario": "real_estate",
    "action_labels": {"call_now": "Call now", "send_sms": "Send SMS"},
    "series": [
        {
            "round": 0,
            "n": 100,
            "auc": 0.74,
            "nba_value": 0.31,
            "nba_reward": 0.28,
            "ope_dr": 0.30,
            "ci_low": 0.22,
            "ci_high": 0.38,
        },
        {
            "round": 1,
            "n": 200,
            "auc": 0.86,
            "nba_value": 0.49,
            "nba_reward": 0.47,
            "ope_dr": 0.48,
            "ci_low": 0.41,
            "ci_high": 0.55,
        },
    ],
    "model": {
        "auc": 0.86,
        "brier": 0.12,
        "ece": 0.05,
        "n": 200,
        "calibration_method": "isotonic",
        "best_params": {"depth": 5},
        "importances": [{"name": "intent", "gain": 0.71}],
    },
    "policy": [
        {
            "segment": "high_intent",
            "recommended_action": "call_now",
            "recommended_label": "Call now",
            "scores": [
                {"action_id": "call_now", "score": 0.71, "label": "Call now"},
                {"action_id": "send_sms", "score": 0.40, "label": "Send SMS"},
            ],
        }
    ],
    "ope": {"dr": 0.48, "ci_low": 0.41, "ci_high": 0.55},
}

FEEDBACK_RESULT = {
    "ok": True,
    "use_case": "lead_score",
    "converted": True,
    "outcome_recorded": True,
    "bandit_updated": True,
    "bandit_n": 42,
    "message": "outcome recorded; bandit taught",
}


# ---------------------------------------------------------------------------
# 1. scoring/train  (LONG-RUNNING)
# ---------------------------------------------------------------------------


class TestTrainScoring:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/scoring/train"
        ).mock(return_value=httpx.Response(200, json=TRAIN_RESULT))

        result = client.ml.train_scoring(
            "lead_score",
            rows=[
                {"features": {"budget": 5_000_000, "intent": 0.8}, "label": 1},
                {"features": {"budget": 200_000, "intent": 0.1}, "label": 0},
            ],
            optimize_budget=50,
        )

        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "rows": [
                {"features": {"budget": 5_000_000, "intent": 0.8}, "label": 1},
                {"features": {"budget": 200_000, "intent": 0.1}, "label": 0},
            ],
            "optimize_budget": 50,
        }

        assert isinstance(result, TrainScoringResult)
        assert result.auc == 0.91
        assert result.brier_uncalibrated == 0.18
        assert result.model_version == 7
        assert result.best_params == {"depth": 6, "learning_rate": 0.05}
        assert result.importances[0].name == "budget"
        assert result.importances[0].gain == 0.62

    @respx.mock
    def test_optimize_budget_omitted_when_none(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/scoring/train"
        ).mock(return_value=httpx.Response(200, json=TRAIN_RESULT))

        client.ml.train_scoring("lead_score", rows=[{"features": {}, "label": 1}])

        assert json.loads(route.calls.last.request.content) == {
            "rows": [{"features": {}, "label": 1}]
        }

    @respx.mock
    def test_uses_long_read_timeout(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/scoring/train"
        ).mock(return_value=httpx.Response(200, json=TRAIN_RESULT))

        client.ml.train_scoring("lead_score", rows=[{"features": {}, "label": 1}])

        timeout = route.calls.last.request.extensions["timeout"]
        assert timeout["read"] == DEFAULT_ML_LONG_TIMEOUT_SECONDS == 900.0
        assert timeout["connect"] == 10.0

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/scoring/train"
        ).mock(return_value=httpx.Response(200, json=TRAIN_RESULT))
        try:
            result = await async_client.ml.train_scoring(
                "lead_score", rows=[{"features": {"x": 1}, "label": 1}]
            )
            assert isinstance(result, TrainScoringResult)
            assert result.model_version == 7
            assert route.calls.last.request.extensions["timeout"]["read"] == 900.0
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# 2. scoring/predict
# ---------------------------------------------------------------------------


class TestPredictScore:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/scoring/predict"
        ).mock(return_value=httpx.Response(200, json=PREDICT_RESULT))

        result = client.ml.predict_score(
            "lead_score", features={"budget": 3_000_000, "intent": 0.7}
        )

        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "features": {"budget": 3_000_000, "intent": 0.7}
        }

        assert isinstance(result, PredictScoreResult)
        assert result.score == 0.83
        assert result.raw == 0.77
        assert result.served_from == "live"
        assert result.calibration_method == "isotonic"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/scoring/predict"
        ).mock(return_value=httpx.Response(200, json=PREDICT_RESULT))
        try:
            result = await async_client.ml.predict_score("lead_score", features={"x": 1})
            assert isinstance(result, PredictScoreResult)
            assert result.score == 0.83
            assert json.loads(route.calls.last.request.content) == {"features": {"x": 1}}
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# 3. nba/decide
# ---------------------------------------------------------------------------


class TestDecideNBA:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/nba/decide"
        ).mock(return_value=httpx.Response(200, json=DECIDE_RESULT))

        result = client.ml.decide_nba(
            "lead_score",
            context={"segment": "high_intent"},
            actions=[
                {"id": "call_now", "features": {"cost": 2}},
                {"id": "send_sms", "features": {"cost": 1}},
            ],
            explore=True,
        )

        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "context": {"segment": "high_intent"},
            "actions": [
                {"id": "call_now", "features": {"cost": 2}},
                {"id": "send_sms", "features": {"cost": 1}},
            ],
            "explore": True,
        }

        assert isinstance(result, DecideNBAResult)
        assert result.action_id == "call_now"
        assert result.propensity == 0.55
        assert result.model_n == 318
        assert result.scores[1].action_id == "send_sms"
        assert result.scores[1].score == 0.42

    @respx.mock
    def test_explore_omitted_when_none(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/nba/decide"
        ).mock(return_value=httpx.Response(200, json=DECIDE_RESULT))

        client.ml.decide_nba(
            "lead_score",
            context={"a": 1},
            actions=[{"id": "x", "features": {}}],
        )

        assert json.loads(route.calls.last.request.content) == {
            "context": {"a": 1},
            "actions": [{"id": "x", "features": {}}],
        }

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/builtin-agents/ml/lead_score/nba/decide").mock(
            return_value=httpx.Response(200, json=DECIDE_RESULT)
        )
        try:
            result = await async_client.ml.decide_nba(
                "lead_score", context={}, actions=[{"id": "x", "features": {}}]
            )
            assert isinstance(result, DecideNBAResult)
            assert result.action_id == "call_now"
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# 4. nba/learn
# ---------------------------------------------------------------------------


class TestLearnNBA:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/nba/learn"
        ).mock(return_value=httpx.Response(200, json=LEARN_RESULT))

        result = client.ml.learn_nba(
            "lead_score",
            action_id="call_now",
            reward=1.0,
            context={"segment": "high_intent"},
            action_features={"cost": 2},
            propensity=0.55,
        )

        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "action_id": "call_now",
            "reward": 1.0,
            "context": {"segment": "high_intent"},
            "action_features": {"cost": 2},
            "propensity": 0.55,
        }

        assert isinstance(result, LearnNBAResult)
        assert result.ok is True
        assert result.n == 319

    @respx.mock
    def test_optional_fields_omitted(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/nba/learn"
        ).mock(return_value=httpx.Response(200, json=LEARN_RESULT))

        client.ml.learn_nba("lead_score", action_id="x", reward=0.0)

        assert json.loads(route.calls.last.request.content) == {
            "action_id": "x",
            "reward": 0.0,
        }

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/builtin-agents/ml/lead_score/nba/learn").mock(
            return_value=httpx.Response(200, json=LEARN_RESULT)
        )
        try:
            result = await async_client.ml.learn_nba(
                "lead_score", action_id="call_now", reward=1.0
            )
            assert isinstance(result, LearnNBAResult)
            assert result.n == 319
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# 5. ope/evaluate
# ---------------------------------------------------------------------------


class TestEvaluateOPE:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/ope/evaluate"
        ).mock(return_value=httpx.Response(200, json=OPE_RESULT))

        logged = [
            {
                "context": {"segment": "high_intent"},
                "action_id": "call_now",
                "propensity": 0.55,
                "reward": 1.0,
            },
            {
                "context": {"segment": "low_intent"},
                "action_id": "send_sms",
                "propensity": 0.45,
                "reward": 0.0,
            },
        ]
        result = client.ml.evaluate_ope("lead_score", logged=logged)

        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content) == {"logged": logged}

        assert isinstance(result, EvaluateOPEResult)
        assert result.ips == 0.61
        assert result.snips == 0.59
        assert result.dr == 0.6
        assert result.ci_low == 0.52
        assert result.ci_high == 0.68
        assert result.ess == 213.4
        assert result.estimator_ci == "dr"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/builtin-agents/ml/lead_score/ope/evaluate").mock(
            return_value=httpx.Response(200, json=OPE_RESULT)
        )
        try:
            result = await async_client.ml.evaluate_ope("lead_score", logged=[])
            assert isinstance(result, EvaluateOPEResult)
            assert result.dr == 0.6
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# 6. simulate-rounds  (LONG-RUNNING)
# ---------------------------------------------------------------------------


class TestSimulateRounds:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/simulate-rounds"
        ).mock(return_value=httpx.Response(200, json=SIMULATE_RESULT))

        result = client.ml.simulate_rounds(
            "lead_score", scenario="real_estate", rounds=2, seed=7
        )

        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "scenario": "real_estate",
            "rounds": 2,
            "seed": 7,
        }

        assert isinstance(result, SimulateRoundsResult)
        assert result.scenario == "real_estate"
        assert result.action_labels == {"call_now": "Call now", "send_sms": "Send SMS"}
        assert len(result.series) == 2
        assert result.series[1].round == 1
        assert result.series[1].auc == 0.86
        assert result.series[1].ope_dr == 0.48
        assert result.model is not None
        assert result.model.auc == 0.86
        assert result.model.importances[0].name == "intent"
        assert result.policy[0].segment == "high_intent"
        assert result.policy[0].recommended_action == "call_now"
        assert result.policy[0].scores[0].label == "Call now"
        assert result.ope is not None
        assert result.ope.dr == 0.48
        assert result.ope.ci_high == 0.55

    @respx.mock
    def test_all_fields_omitted_when_none(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/simulate-rounds"
        ).mock(return_value=httpx.Response(200, json=SIMULATE_RESULT))

        client.ml.simulate_rounds("lead_score")

        assert json.loads(route.calls.last.request.content) == {}

    @respx.mock
    def test_uses_long_read_timeout(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/simulate-rounds"
        ).mock(return_value=httpx.Response(200, json=SIMULATE_RESULT))

        client.ml.simulate_rounds("lead_score")

        timeout = route.calls.last.request.extensions["timeout"]
        assert timeout["read"] == 900.0
        assert timeout["connect"] == 10.0

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/simulate-rounds"
        ).mock(return_value=httpx.Response(200, json=SIMULATE_RESULT))
        try:
            result = await async_client.ml.simulate_rounds("lead_score", rounds=2)
            assert isinstance(result, SimulateRoundsResult)
            assert len(result.series) == 2
            assert route.calls.last.request.extensions["timeout"]["read"] == 900.0
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# 7. feedback  (the unified call)
# ---------------------------------------------------------------------------


class TestRecordFeedback:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/feedback"
        ).mock(return_value=httpx.Response(200, json=FEEDBACK_RESULT))

        result = client.ml.record_feedback(
            "lead_score",
            subject_id="lead-42",
            features={"budget": 3_000_000, "intent": 0.7},
            converted=True,
            predicted_score=82,
            note="closed-won",
            action_id="call_now",
            context={"segment": "high_intent"},
            action_features={"cost": 2},
            propensity=0.55,
            reward=1.0,
        )

        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "converted": True,
            "subject_id": "lead-42",
            "features": {"budget": 3_000_000, "intent": 0.7},
            "predicted_score": 82,
            "note": "closed-won",
            "action_id": "call_now",
            "context": {"segment": "high_intent"},
            "action_features": {"cost": 2},
            "propensity": 0.55,
            "reward": 1.0,
        }

        assert isinstance(result, RecordFeedbackResult)
        assert result.ok is True
        assert result.use_case == "lead_score"
        assert result.converted is True
        assert result.outcome_recorded is True
        assert result.bandit_updated is True
        assert result.bandit_n == 42
        assert result.message == "outcome recorded; bandit taught"

    @respx.mock
    def test_minimal_only_converted_required(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/feedback"
        ).mock(return_value=httpx.Response(200, json=FEEDBACK_RESULT))

        client.ml.record_feedback("lead_score", converted=False)

        # Only the required `converted` flag is sent; every other field omitted.
        assert json.loads(route.calls.last.request.content) == {"converted": False}

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/builtin-agents/ml/lead_score/feedback"
        ).mock(return_value=httpx.Response(200, json=FEEDBACK_RESULT))
        try:
            result = await async_client.ml.record_feedback(
                "lead_score", subject_id="lead-9", converted=True
            )
            assert isinstance(result, RecordFeedbackResult)
            assert result.bandit_updated is True
            assert json.loads(route.calls.last.request.content) == {
                "converted": True,
                "subject_id": "lead-9",
            }
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# Client wiring
# ---------------------------------------------------------------------------


class TestWiring:
    def test_ml_wired_on_sync_client(self, client: Sonzai) -> None:
        from sonzai.resources.ml import ML

        assert isinstance(client.ml, ML)

    def test_ml_wired_on_async_client(self, async_client: AsyncSonzai) -> None:
        from sonzai.resources.ml import AsyncML

        assert isinstance(async_client.ml, AsyncML)
