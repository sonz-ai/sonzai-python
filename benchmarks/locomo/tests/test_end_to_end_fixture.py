"""End-to-end LoCoMo run test using the mini fixture and fake clients.

No real Sonzai or mem0 API calls — we stub AsyncSonzai.agents.chat,
memory.search, workbench.advance_time, and the /process raw transport.
This asserts that the runner plumbs the backend result through scoring
and judge correctly.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from benchmarks.locomo import run as run_mod
from benchmarks.locomo.dataset import load_samples

FIXTURE = Path(__file__).parent / "fixtures" / "mini_locomo.json"


@pytest.mark.asyncio
async def test_sonzai_pipeline_writes_expected_rows(tmp_path: Path, monkeypatch):
    samples = load_samples(path=FIXTURE)
    assert samples

    # Stub the Sonzai backend entirely — we're testing the orchestration layer
    fake_br = MagicMock()
    fake_br.speaker_a_memories = []
    fake_br.speaker_b_memories = []
    fake_br.agent_answer = "data scientist"
    fake_br.retrieved_session_ids = ["session_1"]
    fake_br.extra = {}

    async def fake_ingest(*args, **kwargs):
        return {"process_calls": 4, "facts_extracted": 7, "advance_time_calls": 1, "advance_time_failures": 0}  # noqa: E501

    async def fake_answer_one(*args, **kwargs):
        return fake_br

    async def fake_ensure_agent(client):
        return ("agent-xyz", False)

    class _FakeVerdict:
        label = "CORRECT"

    async def fake_judge_locomo(*args, **kwargs):
        return _FakeVerdict()

    async def fake_close():
        return None

    fake_client = MagicMock()
    fake_client.close = fake_close

    with patch("benchmarks.locomo.backends.sonzai.ingest_sample", fake_ingest), \
         patch("benchmarks.locomo.backends.sonzai.answer_one_qa", fake_answer_one), \
         patch("sonzai.benchmarks.ensure_benchmark_agent_async", fake_ensure_agent), \
         patch("benchmarks.locomo.run.judge_locomo_async", fake_judge_locomo), \
         patch("benchmarks.locomo.run.AsyncSonzai", return_value=fake_client):
        judge = MagicMock()

        rows = await run_mod._run_sonzai(
            samples,
            concurrency=1, mode="both", judge=judge,
            top_k=30, ingest_batch_size=2, skip_advance_time=True,
            include_adversarial=False, reuse_agents_path=None, clear_reused_memory=False,
        )

    # Two non-adversarial QAs in the fixture (categories 1 and 3)
    assert len(rows) == 2
    assert all(r["backend"] == "sonzai" for r in rows)
    assert all(r["llm_correct"] is True for r in rows)
    # First QA's expected Recall@1 = 1 because retrieved_session_ids = ["session_1"]
    # and evidence = ["D1:3"] → session_1.
    first = next(r for r in rows if r["qa_index"] == 0)
    assert first["retrieval"]["recall_any@1"] == 1.0
    # Second QA's evidence is D2:4 → session_2; retrieved is session_1 → miss.
    second = next(r for r in rows if r["qa_index"] == 1)
    assert second["retrieval"]["recall_any@10"] == 0.0


def test_write_jsonl_round_trip(tmp_path: Path):
    rows = [{"a": 1}, {"b": [1, 2, 3]}]
    out = tmp_path / "x.jsonl"
    run_mod._write_jsonl(rows, out)
    loaded = [json.loads(line) for line in out.read_text().splitlines()]
    assert loaded == rows
