"""Sonzai backend for LIFELONG-SOTOPIA.

One Sonzai agent per pair, stable user_id per pair. The agent's memory layer
*is* the memory under test — no `--memory` flag needed. Across episodes the
scenario varies (sampled per relationship type); the (agent_id, user_id) pair
stays constant so Sonzai sees a continuous relationship history.

Per episode:
1. ``sessions.start`` with a fresh session_id keyed on (pair_id, episode_index).
2. Alternate turns: Gemini generates the partner via ``partner_turn_async``;
   the agent replies via ``client.agents.chat`` (Sonzai handles its own
   retrieval / personality / continuity).
3. ``sessions.end`` to flush.
4. Score with judge_sotopia_async + judge_bel_extended_async.
5. Optionally ``advance_time(25h)`` between episodes so consolidation /
   diary fire — same convention as the existing sotopia bench.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Sequence

from sonzai import AsyncSonzai

from benchmarks.common.gemini_judge import (
    GeminiJudge,
    bel_extended_value,
    judge_bel_extended_async,
    judge_sotopia_async,
    partner_turn_async,
    summarize_session_async,
)
from benchmarks.common.sdk_extras import (
    async_sessions,
    ensure_bench_agent_async,
)
from benchmarks.common.workbench_compat import advance_time_chunked_async

from ..scenarios import CorpusBundle, Episode, Pair, plan_episodes
from ..scoring import EpisodeRun, EpisodeScore

logger = logging.getLogger("benchmarks.lifelong_sotopia.sonzai")

MIN_GAP_HOURS = 25.0


def _render_transcript(transcript: list[dict[str, str]]) -> str:
    return "\n".join(
        f"{'Agent' if t['role'] == 'assistant' else 'Partner'}: {t['content']}"
        for t in transcript
    )


async def _simulate_episode_sonzai(
    *,
    client: AsyncSonzai,
    pair: Pair,
    episode: Episode,
    agent_id: str,
    user_id: str,
    judge: GeminiJudge,
    prior_episodes_summary: str,
    max_turn_pairs: int,
) -> list[dict[str, str]]:
    sc = episode.scenario
    sessions = async_sessions(client)
    session_id = f"ll-{pair.pair_id}-e{episode.episode_index:03d}-{uuid.uuid4().hex[:4]}"
    await sessions.start(agent_id=agent_id, user_id=user_id, session_id=session_id)

    setting_text = sc.setting

    transcript: list[dict[str, str]] = []
    try:
        for _ in range(max_turn_pairs):
            try:
                partner = await partner_turn_async(
                    judge,
                    scenario=setting_text,
                    transcript_text=_render_transcript(transcript),
                    partner_name=pair.char_b.name,
                    partner_goal=sc.partner_goal,
                    partner_secret=sc.partner_secret,
                    agent_name=pair.char_a.name,
                    prior_sessions_summary=prior_episodes_summary,
                )
            except Exception as e:
                logger.warning("partner_turn failed: %s — ending episode early", e)
                break

            transcript.append({"role": "user", "content": partner.content})
            if partner.end_conversation:
                break

            try:
                agent_resp = await client.agents.chat(
                    agent_id=agent_id,
                    user_id=user_id,
                    session_id=session_id,
                    messages=[{"role": "user", "content": partner.content}],
                )
            except Exception as e:
                logger.warning("agents.chat failed: %s — ending episode early", e)
                break

            agent_text = getattr(agent_resp, "content", "") or ""
            transcript.append({"role": "assistant", "content": agent_text})
    finally:
        try:
            await sessions.end(
                agent_id=agent_id,
                user_id=user_id,
                session_id=session_id,
                total_messages=len(transcript),
            )
        except Exception as e:
            logger.warning("sessions.end failed (non-fatal): %s", e)

    return transcript


async def _score_episode(
    *,
    pair: Pair,
    episode: Episode,
    transcript: list[dict[str, str]],
    judge: GeminiJudge,
    prior_episodes_summary: str,
) -> EpisodeScore:
    transcript_text = _render_transcript(transcript)
    sc = episode.scenario
    sotopia = await judge_sotopia_async(
        judge,
        scenario=sc.setting,
        transcript=transcript_text,
        agent_name=pair.char_a.name,
        agent_goal=sc.agent_goal,
        agent_secret=sc.agent_secret,
        prior_sessions_summary=prior_episodes_summary,
    )
    bel_ext = await judge_bel_extended_async(
        judge,
        scenario=sc.setting,
        transcript=transcript_text,
        agent_name=pair.char_a.name,
        agent_goal=sc.agent_goal,
        agent_secret=sc.agent_secret,
        episode_index=episode.episode_index + 1,
        is_memory_required=episode.is_memory_required,
        prior_episodes_summary=prior_episodes_summary,
    )
    return EpisodeScore(
        believability=sotopia.believability,
        goal=sotopia.goal,
        bel_extended=bel_extended_value(bel_ext),
        checkpoints_failed=bel_ext.failures(),
        judge_rationale=bel_ext.rationale,
    )


async def _run_one_pair_sonzai(
    *,
    client: AsyncSonzai,
    corpus: CorpusBundle,
    pair: Pair,
    n_episodes: int,
    judge: GeminiJudge,
    seed: int,
    include_memory_required: bool,
    max_turn_pairs: int,
    advance_time_between: bool,
) -> list[EpisodeRun]:
    plan = plan_episodes(
        corpus=corpus,
        pair=pair,
        n_episodes=n_episodes,
        seed=seed,
        include_memory_required=include_memory_required,
    )

    description = (
        f"You are {pair.char_a.name}. {pair.char_a.background}. "
        f"Personality: {pair.char_a.personality}. "
        f"Relationship to {pair.char_b.name}: {pair.context}."
    )
    agent_name = f"sonzai-bench-lifelong-{pair.pair_id}"
    agent_id, _existed = await ensure_bench_agent_async(
        client, name=agent_name, description=description
    )
    user_id = f"lifelong-{pair.pair_id[:24]}"

    runs: list[EpisodeRun] = []
    prior_summaries: list[str] = []

    for ep in plan.episodes:
        prior_block = (
            "\n".join(f"- Episode {i+1}: {s}" for i, s in enumerate(prior_summaries))
            if prior_summaries
            else "(this is the first episode)"
        )
        transcript = await _simulate_episode_sonzai(
            client=client,
            pair=pair,
            episode=ep,
            agent_id=agent_id,
            user_id=user_id,
            judge=judge,
            prior_episodes_summary=prior_block,
            max_turn_pairs=max_turn_pairs,
        )

        try:
            score = await _score_episode(
                pair=pair,
                episode=ep,
                transcript=transcript,
                judge=judge,
                prior_episodes_summary=prior_block,
            )
        except Exception:
            logger.exception(
                "scoring failed for pair=%s ep=%d", pair.pair_id, ep.episode_index
            )
            continue

        runs.append(
            EpisodeRun(
                pair_id=pair.pair_id,
                relationship_type=pair.relationship_type,
                episode_index=ep.episode_index,
                scenario_id=ep.scenario.scenario_id,
                is_memory_required=ep.is_memory_required,
                transcript=transcript,
                score=score,
            )
        )

        try:
            s = await summarize_session_async(
                judge,
                transcript_text=_render_transcript(transcript),
                agent_name=pair.char_a.name,
                partner_name=pair.char_b.name,
            )
            prior_summaries.append(s.summary)
        except Exception as e:
            logger.warning("summarize failed (non-fatal): %s", e)
            prior_summaries.append("(summary unavailable)")

        if advance_time_between and ep.episode_index < len(plan.episodes) - 1:
            try:
                await advance_time_chunked_async(
                    client,
                    agent_id=agent_id,
                    user_id=user_id,
                    total_hours=MIN_GAP_HOURS,
                )
            except Exception as e:
                logger.warning("advance_time failed (non-fatal): %s", e)

    return runs


async def run_all_pairs_sonzai(
    *,
    corpus: CorpusBundle,
    pairs: Sequence[Pair],
    n_episodes: int,
    judge: GeminiJudge,
    seed: int = 13,
    include_memory_required: bool = True,
    max_turn_pairs: int = 4,
    pair_concurrency: int = 1,
    advance_time_between: bool = True,
) -> list[EpisodeRun]:
    """Run every pair through ``n_episodes``, Sonzai memory backend."""
    client = AsyncSonzai(timeout=600.0)
    sem = asyncio.Semaphore(max(1, pair_concurrency))

    async def _one(pair: Pair) -> list[EpisodeRun]:
        async with sem:
            try:
                return await _run_one_pair_sonzai(
                    client=client,
                    corpus=corpus,
                    pair=pair,
                    n_episodes=n_episodes,
                    judge=judge,
                    seed=seed,
                    include_memory_required=include_memory_required,
                    max_turn_pairs=max_turn_pairs,
                    advance_time_between=advance_time_between,
                )
            except Exception:
                logger.exception("pair %s failed", pair.pair_id)
                return []

    try:
        grouped = await asyncio.gather(*(_one(p) for p in pairs))
    finally:
        await client.close()

    out: list[EpisodeRun] = []
    for g in grouped:
        out.extend(g)
    return out
