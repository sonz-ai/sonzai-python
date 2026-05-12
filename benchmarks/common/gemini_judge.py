"""Gemini 3.1 Flash Lite judge — neutral third-party grader.

Keeping the judge outside the Anthropic and OpenAI ecosystems lets us compare
memory systems that internally depend on either provider without accusations of
judge-bias. One model, one rubric, both systems.
"""

from __future__ import annotations

import os
from typing import TypeVar

from google import genai
from google.genai import types as gt
from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)

DEFAULT_MODEL = "gemini-3.1-flash-lite"


class GeminiJudge:
    """Structured-output wrapper over Gemini for scoring benchmarks."""

    def __init__(
        self,
        *,
        model: str = DEFAULT_MODEL,
        api_key: str | None = None,
    ) -> None:
        self._client = genai.Client(api_key=api_key or os.environ["GEMINI_API_KEY"])
        self._model = model

    def grade(self, prompt: str, schema: type[T]) -> T:
        resp = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config=gt.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.0,
            ),
        )
        text = resp.text
        if text is None:
            raise RuntimeError("Gemini judge returned no text")
        return schema.model_validate_json(text)

    async def grade_async(self, prompt: str, schema: type[T]) -> T:
        resp = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=gt.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.0,
            ),
        )
        text = resp.text
        if text is None:
            raise RuntimeError("Gemini judge returned no text")
        return schema.model_validate_json(text)


# ---------------------------------------------------------------------------
# LongMemEval QA rubric (adapted from Wu et al., 2024)
# ---------------------------------------------------------------------------


class QAVerdict(BaseModel):
    correct: bool
    rationale: str


_QA_PROMPT = """You are grading whether an AI assistant's answer to a question is correct.

Question:
{question}

Ground-truth answer:
{ground_truth}

Assistant's answer:
{agent_answer}

The assistant's answer is CORRECT if it conveys the same factual content as the
ground truth. Minor phrasing differences, reasonable paraphrases, and equivalent
units are acceptable (e.g. "3 days" == "72 hours"; "John's sister" == "his sister
John").

For COUNT and NUMERIC questions ("how many X", "how much $", "how many days"),
the ONLY thing that matters is whether the NUMBER matches the ground-truth
number. If the ground truth is "5" and the assistant's stated total is also
"5", that is CORRECT — period. Ignore any item names, specific quantities
per item, or other details the assistant lists alongside the number; those
are supplementary, not the answer. The user asked "how many", they got the
right count, that's a pass. Only mark INCORRECT when the ASSISTANT'S TOTAL
NUMBER is wrong (e.g. ground truth "5", assistant says "3" or "8").

Examples for count questions:
  GOLD: "5"  PRED: "5 model kits: 2 B-29s, 2 Camaros, 1 Spitfire" -> CORRECT
  GOLD: "5"  PRED: "5 model kits: a Spitfire, a Mustang"          -> CORRECT
  GOLD: "5"  PRED: "5 — including the Tamiya kit and others"      -> CORRECT
  GOLD: "5"  PRED: "I have 3 model kits"                          -> INCORRECT
  GOLD: "5"  PRED: "8 model kits"                                  -> INCORRECT

For non-numeric factual questions, the answer is INCORRECT if it
contradicts the ground truth, omits the key fact, or fabricates details
that contradict it. (Extra correct context is fine; extra contradictory
context is not.)

Respond with JSON matching this schema:
{{"correct": <bool>, "rationale": "<one short sentence>"}}
"""


def judge_qa(
    judge: GeminiJudge, *, question: str, ground_truth: str, agent_answer: str
) -> QAVerdict:
    return judge.grade(
        _QA_PROMPT.format(
            question=question.strip(),
            ground_truth=ground_truth.strip(),
            agent_answer=agent_answer.strip() or "[no answer]",
        ),
        QAVerdict,
    )


async def judge_qa_async(
    judge: GeminiJudge, *, question: str, ground_truth: str, agent_answer: str
) -> QAVerdict:
    return await judge.grade_async(
        _QA_PROMPT.format(
            question=question.strip(),
            ground_truth=ground_truth.strip(),
            agent_answer=agent_answer.strip() or "[no answer]",
        ),
        QAVerdict,
    )


# ---------------------------------------------------------------------------
# SOTOPIA 7-dimension rubric (Zhou et al., 2023)
# ---------------------------------------------------------------------------


class SotopiaScore(BaseModel):
    believability: float = Field(ge=0, le=10)
    relationship: float = Field(ge=-5, le=5)
    knowledge: float = Field(ge=0, le=10)
    secret: float = Field(ge=-10, le=0)
    social_rules: float = Field(ge=-10, le=0)
    financial_and_material: float = Field(ge=-5, le=5)
    goal: float = Field(ge=0, le=10)
    # 8th dim — bench-added. 0..10 where 5 = neutral (neither referenced nor
    # contradicted prior sessions), 10 = accurate, natural callbacks, 0 =
    # failed to recall things the partner explicitly referenced. For
    # session 1 (no prior context) the judge is instructed to score 5.0.
    memory_continuity: float = Field(ge=0, le=10, default=5.0)
    overall: float
    rationale: str


_SOTOPIA_PROMPT = """You are grading the social intelligence of an AI-played character
in a roleplay scenario using the SOTOPIA rubric, extended with one memory
continuity dimension for longitudinal benchmarks.

# Scenario
{scenario}

# Character being graded: {agent_name}
Goal: {agent_goal}
Private information (secret): {agent_secret}

# What happened in prior sessions (the partner knows all of this; the agent has their own memory system)
{prior_sessions_summary}

# Transcript (this session only)
{transcript}

Score the character on these eight dimensions. Use the ranges exactly:
- believability (0..10) — how human-like and in-character were they?
- relationship (-5..5) — did they build or damage the relationship?
- knowledge (0..10) — did they gain useful new information?
- secret (-10..0) — how well did they protect their private information? 0 = never leaked; negative = leaked.
- social_rules (-10..0) — 0 = no violations; negative = violated norms.
- financial_and_material (-5..5) — material benefit or loss from the interaction.
- goal (0..10) — did they achieve their stated goal?
- memory_continuity (0..10) — did the agent treat the relationship as continuous with the prior sessions listed above? 10 = made accurate, natural callbacks to specific prior facts/commitments without being prompted. 5 = neutral (didn't reference but didn't contradict). 0 = failed to recall something the partner explicitly referenced, contradicted known facts, or started cold as if the prior sessions never happened. If the prior-sessions section says "(this is the first session)", score this dimension exactly 5.0 (neutral — no opportunity to demonstrate continuity yet).

Then compute `overall` as the unweighted mean of all eight dimensions mapped
into [0..10] (linearly rescale each to [0..10] first: negative-ranged dims
shift up, then scale). Finally write a one-sentence rationale.

Respond with JSON matching the schema exactly.
"""


def judge_sotopia(
    judge: GeminiJudge,
    *,
    scenario: str,
    transcript: str,
    agent_name: str,
    agent_goal: str,
    agent_secret: str,
    prior_sessions_summary: str = "",
) -> SotopiaScore:
    return judge.grade(
        _SOTOPIA_PROMPT.format(
            scenario=scenario.strip(),
            transcript=transcript.strip(),
            agent_name=agent_name,
            agent_goal=agent_goal,
            agent_secret=agent_secret or "(none)",
            prior_sessions_summary=prior_sessions_summary.strip()
            or "(this is the first session)",
        ),
        SotopiaScore,
    )


async def judge_sotopia_async(
    judge: GeminiJudge,
    *,
    scenario: str,
    transcript: str,
    agent_name: str,
    agent_goal: str,
    agent_secret: str,
    prior_sessions_summary: str = "",
) -> SotopiaScore:
    return await judge.grade_async(
        _SOTOPIA_PROMPT.format(
            scenario=scenario.strip(),
            transcript=transcript.strip(),
            agent_name=agent_name,
            agent_goal=agent_goal,
            agent_secret=agent_secret or "(none)",
            prior_sessions_summary=prior_sessions_summary.strip()
            or "(this is the first session)",
        ),
        SotopiaScore,
    )


# ---------------------------------------------------------------------------
# SOTOPIA partner — also Gemini so the only variable across session 1→30 is
# Sonzai's side. The partner plays the non-Sonzai character.
# ---------------------------------------------------------------------------


class PartnerTurn(BaseModel):
    content: str
    end_conversation: bool = False


_PARTNER_PROMPT = """You are {partner_name} in a roleplay. Stay in character.

# Scenario
{scenario}

# Your character ({partner_name})
Goal: {partner_goal}
Private information (do not volunteer unprompted): {partner_secret}

# What you remember from prior sessions with {agent_name}
{prior_sessions_summary}

# Conversation so far (this session)
{transcript}

Produce your next turn as {partner_name}. Keep it natural and in-character,
1-3 sentences typically.

IMPORTANT — to make this a real longitudinal conversation, you (as
{partner_name}) DO remember prior sessions. Reference specific things you
said or that {agent_name} said in prior sessions when it would naturally
come up — follow-ups on advice they gave, updates on things you brought up,
callbacks to shared context. Do NOT pretend every session is a fresh start.
If prior sessions listed "(this is the first session)", just open the
conversation naturally with no callbacks.

If the conversation has reached a clear ending point, set end_conversation
to true.

Respond with JSON: {{"content": "<your next utterance>", "end_conversation": <bool>}}
"""


def partner_turn(
    judge: GeminiJudge,
    *,
    scenario: str,
    transcript_text: str,
    partner_name: str,
    partner_goal: str,
    partner_secret: str,
    agent_name: str = "the agent",
    prior_sessions_summary: str = "",
) -> PartnerTurn:
    return judge.grade(
        _PARTNER_PROMPT.format(
            scenario=scenario.strip(),
            transcript=transcript_text.strip() or "(no turns yet — you speak first)",
            partner_name=partner_name,
            partner_goal=partner_goal,
            partner_secret=partner_secret or "(none)",
            agent_name=agent_name,
            prior_sessions_summary=prior_sessions_summary.strip()
            or "(this is the first session)",
        ),
        PartnerTurn,
    )


async def partner_turn_async(
    judge: GeminiJudge,
    *,
    scenario: str,
    transcript_text: str,
    partner_name: str,
    partner_goal: str,
    partner_secret: str,
    agent_name: str = "the agent",
    prior_sessions_summary: str = "",
) -> PartnerTurn:
    return await judge.grade_async(
        _PARTNER_PROMPT.format(
            scenario=scenario.strip(),
            transcript=transcript_text.strip() or "(no turns yet — you speak first)",
            partner_name=partner_name,
            partner_goal=partner_goal,
            partner_secret=partner_secret or "(none)",
            agent_name=agent_name,
            prior_sessions_summary=prior_sessions_summary.strip()
            or "(this is the first session)",
        ),
        PartnerTurn,
    )


# ---------------------------------------------------------------------------
# Session summarizer — compresses one transcript into 2-3 sentences so the
# partner (and judge) can reference it when grading subsequent sessions. One
# call per session-end, reused across all later sessions' prompts.
# ---------------------------------------------------------------------------


class SessionSummary(BaseModel):
    summary: str


_SUMMARY_PROMPT = """You are condensing one conversation between {agent_name} and {partner_name}
so later sessions in this relationship can reference it.

# Transcript
{transcript}

Write a crisp 50-100 word summary. Include:
- what {partner_name} brought to the conversation (question, issue, update)
- what {agent_name} advised, revealed, or committed to
- any concrete next steps, deadlines, or emotional beats worth remembering

No meta-commentary, no "in this session". Past tense. Present only what's
worth carrying into the next conversation.

Respond with JSON: {{"summary": "<50-100 word summary>"}}
"""


async def summarize_session_async(
    judge: GeminiJudge,
    *,
    transcript_text: str,
    agent_name: str,
    partner_name: str,
) -> SessionSummary:
    """Compress a session transcript into a short summary for cross-session context."""
    return await judge.grade_async(
        _SUMMARY_PROMPT.format(
            transcript=transcript_text.strip() or "(empty transcript)",
            agent_name=agent_name,
            partner_name=partner_name,
        ),
        SessionSummary,
    )


class AgentTurn(BaseModel):
    content: str


_AGENT_PROMPT = """You are {agent_name} in a roleplay. Stay in character.

# Scenario
{scenario}

# Your character ({agent_name})
Background: {agent_background}
Goal in interactions with {partner_name}: {agent_goal}
Private information (do not volunteer unprompted): {agent_secret}

# What you remember from past sessions with {partner_name}
{retrieved_memories}

# Current conversation with {partner_name}
{transcript}

Produce your next turn as {agent_name}. Stay consistent with what you remember
from past sessions — you and {partner_name} know each other. Keep it natural and
in-character, 1-3 sentences typically.

Respond with JSON: {{"content": "<your next utterance>"}}
"""


async def agent_turn_async(
    judge: GeminiJudge,
    *,
    scenario: str,
    transcript_text: str,
    agent_name: str,
    agent_background: str,
    agent_goal: str,
    agent_secret: str,
    partner_name: str,
    retrieved_memories: str,
) -> AgentTurn:
    """Generate an agent-role turn via Gemini, conditioned on retrieved memory.

    Used by memory-system adapters that don't ship their own chat handler
    (e.g. the MemPalace SOTOPIA backend pairs MemPalace retrieval with this
    generator so both sides speak with the same LLM — the apples-to-apples
    comparison isolates the memory layer, not the generator).
    """
    return await judge.grade_async(
        _AGENT_PROMPT.format(
            scenario=scenario.strip(),
            transcript=transcript_text.strip() or "(no turns yet — partner speaks first)",
            agent_name=agent_name,
            agent_background=agent_background or "(none)",
            agent_goal=agent_goal or "(none)",
            agent_secret=agent_secret or "(none)",
            partner_name=partner_name,
            retrieved_memories=retrieved_memories.strip() or "(no relevant prior memories)",
        ),
        AgentTurn,
    )


__all__ = [
    "BEL_EXTENDED_CHECKPOINTS",
    "DEFAULT_MODEL",
    "AgentTurn",
    "BelExtScore",
    "GeminiJudge",
    "LocomoVerdict",
    "PartnerTurn",
    "QAVerdict",
    "SessionSummary",
    "SotopiaScore",
    "agent_turn_async",
    "bel_extended_value",
    "judge_bel_extended_async",
    "judge_locomo_async",
    "judge_qa",
    "judge_qa_async",
    "judge_sotopia",
    "judge_sotopia_async",
    "partner_turn",
    "partner_turn_async",
    "summarize_session_async",
]


# ---------------------------------------------------------------------------
# LoCoMo judge — mirrors mem0's LLM-judge binary CORRECT/WRONG rubric.
# The prompt is ported verbatim in benchmarks/locomo/prompts.py. Kept here
# (not in locomo/) because common/gemini_judge.py is the hub for all
# structured-output grading wrappers.
# ---------------------------------------------------------------------------


class LocomoVerdict(BaseModel):
    """Binary verdict matching mem0's llm_judge output schema."""
    label: str  # "CORRECT" or "WRONG"


async def judge_locomo_async(
    judge: GeminiJudge,
    *,
    question: str,
    gold_answer: str,
    generated_answer: str,
) -> LocomoVerdict:
    """Grade a LoCoMo answer against the gold using mem0's ACCURACY_PROMPT.

    Prompt is imported from benchmarks.locomo.prompts to keep the single
    source of truth there (alongside ANSWER_PROMPT).
    """
    from benchmarks.locomo.prompts import ACCURACY_PROMPT

    prompt = ACCURACY_PROMPT.format(
        question=question.strip(),
        gold_answer=gold_answer.strip(),
        generated_answer=generated_answer.strip() or "[no answer]",
    )
    return await judge.grade_async(prompt, LocomoVerdict)


# ---------------------------------------------------------------------------
# ConvoMem abstention rubric — "correct iff the agent declines to answer"
# ---------------------------------------------------------------------------

_ABSTENTION_PROMPT = """You are grading whether an AI assistant CORRECTLY ABSTAINED
from answering a question. The question is designed to be UNANSWERABLE from the
conversation history — no evidence has been provided.

Question:
{question}

Assistant's answer:
{agent_answer}

The assistant's answer is CORRECT if it clearly declines to answer, says it
doesn't have the information, says the topic was not mentioned, or otherwise
acknowledges the absence of relevant context. Examples of correct abstention:

- "I don't have that information."
- "You didn't mention that in our conversation."
- "I'm not sure — I don't recall a prior discussion of this."
- "I can't answer that without more context."

The answer is INCORRECT if it fabricates details, guesses, or invents a
specific answer as though it were known.

Respond with JSON matching this schema:
{{"correct": <bool>, "rationale": "<one short sentence>"}}
"""


def judge_abstention(
    judge: GeminiJudge, *, question: str, agent_answer: str
) -> QAVerdict:
    return judge.grade(
        _ABSTENTION_PROMPT.format(
            question=question.strip(),
            agent_answer=agent_answer.strip() or "[no answer]",
        ),
        QAVerdict,
    )


async def judge_abstention_async(
    judge: GeminiJudge, *, question: str, agent_answer: str
) -> QAVerdict:
    return await judge.grade_async(
        _ABSTENTION_PROMPT.format(
            question=question.strip(),
            agent_answer=agent_answer.strip() or "[no answer]",
        ),
        QAVerdict,
    )


# ---------------------------------------------------------------------------
# LIFELONG-SOTOPIA — BelievabilityExtended (8-checkpoint believability)
#
# The paper (Goel & Zhu 2025, https://arxiv.org/abs/2506.12666) describes
# BelExt as an 8-item checklist on top of the standard SOTOPIA Believability
# score, with the formula:
#
#     BelExt = max(Believability - 5 * checkpoints_failed, 0)
#
# The paper does not publish the exact checkpoint set verbatim; the eight
# below are a faithful reading of the failure modes the paper names
# (repetition, character drift, stalling, mode collapse, emotional register,
# secret leakage, scenario-change acknowledgement, agent-voice stability).
# Editorial note: callers wanting to argue with the list should do so by
# editing this constant — the formula and trajectory remain meaningful
# regardless.
# ---------------------------------------------------------------------------


BEL_EXTENDED_CHECKPOINTS: tuple[str, ...] = (
    "no_verbatim_repetition",
    "character_consistency",
    "no_stalling",
    "no_mode_collapse",
    "appropriate_emotional_register",
    "no_unprompted_secret_disclosure",
    "acknowledges_scenario_change",
    "stays_in_agent_voice",
)


class BelExtScore(BaseModel):
    """8-checkpoint extended believability + the source ``believability`` score.

    Each checkpoint is True iff the agent PASSED that checkpoint; the formula
    in :func:`bel_extended_value` subtracts 5 per False.
    """

    believability: float = Field(ge=0, le=10)
    no_verbatim_repetition: bool
    character_consistency: bool
    no_stalling: bool
    no_mode_collapse: bool
    appropriate_emotional_register: bool
    no_unprompted_secret_disclosure: bool
    acknowledges_scenario_change: bool
    stays_in_agent_voice: bool
    rationale: str

    def failures(self) -> list[str]:
        return [c for c in BEL_EXTENDED_CHECKPOINTS if not getattr(self, c)]


def bel_extended_value(score: BelExtScore) -> float:
    """Compute ``BelExt = max(Bel - 5 * failed_checkpoints, 0)``."""
    failed = len(score.failures())
    return max(score.believability - 5.0 * failed, 0.0)


_BEL_EXTENDED_PROMPT = """You are grading the EXTENDED BELIEVABILITY of an AI-played
character across one episode of a multi-episode social interaction. This is
the LIFELONG-SOTOPIA benchmark (Goel & Zhu 2025).

# Scenario (this episode)
{scenario}

# Character being graded: {agent_name}
Goal this episode: {agent_goal}
Private information: {agent_secret}
Episode index in this multi-episode arc: {episode_index} (1-based)
Is this scenario explicitly memory-required (references a prior episode)? {is_memory_required}

# Prior episodes (concise summaries the partner can reference)
{prior_episodes_summary}

# Transcript (this episode only)
{transcript}

Score the agent on these eight pass/fail checkpoints AND the SOTOPIA
believability dimension (0..10):

1. **no_verbatim_repetition** — Did the agent avoid repeating verbatim phrases
   from prior episodes or from earlier in this episode? PASS if no obvious
   verbatim repeats (paraphrased recall is fine and welcome).
2. **character_consistency** — Did the agent stay consistent with their
   stated background/personality and with facts established in prior
   episodes? PASS if no contradictions surface.
3. **no_stalling** — Did every turn move the conversation forward in some
   way (information, decision, emotional beat)? PASS if the agent did NOT
   stall with empty filler / acknowledgements over multiple turns.
4. **no_mode_collapse** — Did the agent's response shape vary appropriately
   (some short, some long; questions and statements; not always the same
   formula)? PASS if there is no obvious single-template repetition.
5. **appropriate_emotional_register** — Did the agent's tone match what the
   scenario calls for (warm in mentorship, direct in negotiation, gentle in
   emotional moments)? PASS if the register fits.
6. **no_unprompted_secret_disclosure** — Did the agent avoid volunteering
   their stated private information when not asked / not strategically
   appropriate? PASS if the secret was not leaked unprompted.
7. **acknowledges_scenario_change** — If this is NOT the first episode, did
   the agent treat this episode's scenario as the present one (rather than
   reusing the prior episode's premise / agenda)? For episode 1 always PASS.
8. **stays_in_agent_voice** — Did the agent stay in {agent_name}'s voice and
   not slip into the partner's persona, into the narrator's, or into a meta
   "as an AI" frame? PASS if the voice held.

Then the standalone:
- **believability** (0..10) — the standard SOTOPIA Bel rubric: how human-like
  and in-character was the agent overall?

Finally a one-sentence rationale.

Respond with JSON matching the schema exactly. The eight checkpoints are
booleans (true = passed).
"""


async def judge_bel_extended_async(
    judge: GeminiJudge,
    *,
    scenario: str,
    transcript: str,
    agent_name: str,
    agent_goal: str,
    agent_secret: str,
    episode_index: int,
    is_memory_required: bool,
    prior_episodes_summary: str = "",
) -> BelExtScore:
    return await judge.grade_async(
        _BEL_EXTENDED_PROMPT.format(
            scenario=scenario.strip(),
            transcript=transcript.strip(),
            agent_name=agent_name,
            agent_goal=agent_goal,
            agent_secret=agent_secret or "(none)",
            episode_index=episode_index,
            is_memory_required="yes" if is_memory_required else "no",
            prior_episodes_summary=prior_episodes_summary.strip() or "(this is episode 1)",
        ),
        BelExtScore,
    )
