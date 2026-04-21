"""SOTOPIA scenario loader.

Pulls scenarios from the canonical ``cmu-lti/sotopia`` HuggingFace dataset on
first run. Falls back to a small bundled seed set if ``datasets`` is
unavailable or the network is cold.

For the longitudinal extension we filter to scenarios that make sense to
repeat with the same pair of characters (cooperative, relationship-building,
or persistently-evaluated interactions).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Character:
    name: str
    background: str = ""
    goal: str = ""
    secret: str = ""


@dataclass
class Scenario:
    scenario_id: str
    codename: str
    setting: str
    agent: Character  # Sonzai plays this side
    partner: Character  # Gemini plays this side
    max_turns: int = 12
    tags: list[str] = field(default_factory=list)


# Hand-picked seed scenarios — used when HuggingFace isn't available, and as
# the tags source for filtering the full dataset.
_SEED_SCENARIOS: list[Scenario] = [
    Scenario(
        scenario_id="seed-mentorship",
        codename="Weekly mentorship check-in",
        setting=(
            "A mentor and mentee meet for a weekly 1:1. Over many sessions they "
            "should build trust, review progress, and adapt their collaboration style."
        ),
        agent=Character(
            name="Mika",
            background="Senior engineer who mentors juniors on their team.",
            goal="Help the mentee grow while respecting their autonomy.",
            secret="Mika was passed over for promotion last quarter.",
        ),
        partner=Character(
            name="Alex",
            background="Junior engineer two months into their first role.",
            goal="Get unblocked on the project and feel supported.",
            secret="Alex is secretly interviewing elsewhere.",
        ),
        max_turns=12,
        tags=["cooperative", "longitudinal"],
    ),
    Scenario(
        scenario_id="seed-therapy",
        codename="Weekly therapy session",
        setting=(
            "A therapist sees a returning client. Over sessions they should build "
            "rapport, revisit past discussions, and guide progress."
        ),
        agent=Character(
            name="Dr. Yuen",
            background="Licensed clinical psychologist specializing in CBT.",
            goal="Help the client make sustained progress on their stated issues.",
            secret="Dr. Yuen is dealing with burnout and is cutting their caseload.",
        ),
        partner=Character(
            name="Jordan",
            background="Client working through work-related anxiety.",
            goal="Feel heard and leave each session with an actionable idea.",
            secret="Jordan has been avoiding a conversation with their partner.",
        ),
        max_turns=14,
        tags=["cooperative", "longitudinal", "emotional"],
    ),
    Scenario(
        scenario_id="seed-language-tutor",
        codename="Weekly Spanish lesson",
        setting=(
            "A language tutor works with a returning student. Over sessions they "
            "adapt to the student's progress and preferences."
        ),
        agent=Character(
            name="Profesora Elena",
            background="Native Spanish speaker, 10 years tutoring experience.",
            goal="Move the student one level up in fluency over the term.",
            secret="Elena doubles her rate in a month.",
        ),
        partner=Character(
            name="Sam",
            background="Adult learner preparing for a trip to Madrid.",
            goal="Be conversational before the trip; enjoy the process.",
            secret="Sam finds grammar drills demotivating but hasn't said so.",
        ),
        max_turns=10,
        tags=["cooperative", "longitudinal", "knowledge-transfer"],
    ),
    Scenario(
        scenario_id="seed-fitness-coach",
        codename="Fitness coaching check-in",
        setting=(
            "A personal trainer checks in with their client each week, adjusting "
            "the program based on progress, mood, and schedule."
        ),
        agent=Character(
            name="Coach Dev",
            background="Personal trainer, 8 years experience with beginners.",
            goal="Help the client hit their 6-month strength goal without injury.",
            secret="Dev has started a side business and has less time.",
        ),
        partner=Character(
            name="Taylor",
            background="Desk worker starting strength training for the first time.",
            goal="See real progress without hating the process.",
            secret="Taylor occasionally skips sessions and fibs about it.",
        ),
        max_turns=10,
        tags=["cooperative", "longitudinal"],
    ),
]


def _load_hf_scenarios(tag_filter: list[str]) -> list[Scenario]:
    try:
        from datasets import load_dataset  # type: ignore[import-not-found]
    except ImportError:
        logger.warning("`datasets` not installed — falling back to seed scenarios")
        return []

    try:
        ds = load_dataset("cmu-lti/sotopia", split="test")
    except Exception as e:
        logger.warning("failed to load cmu-lti/sotopia: %s", e)
        return []

    scenarios: list[Scenario] = []
    for i, row in enumerate(ds):
        try:
            agents = row.get("agent_goals") or row.get("goals") or []
            chars = row.get("agent_names") or row.get("agents") or ["Agent1", "Agent2"]
            if len(chars) < 2 or len(agents) < 2:
                continue
            scenarios.append(
                Scenario(
                    scenario_id=row.get("episode_id", f"sotopia-{i}"),
                    codename=row.get("codename", f"sotopia-{i}"),
                    setting=row.get("scenario", ""),
                    agent=Character(
                        name=chars[0],
                        background=(row.get("agent_backgrounds") or [""])[0] or "",
                        goal=agents[0],
                        secret=(row.get("agent_private_info") or [""])[0] or "",
                    ),
                    partner=Character(
                        name=chars[1],
                        background=(row.get("agent_backgrounds") or ["", ""])[1] or "",
                        goal=agents[1],
                        secret=(row.get("agent_private_info") or ["", ""])[1] or "",
                    ),
                    max_turns=int(row.get("max_turns", 12)),
                    tags=list(row.get("relationships", []) or []) + ["sotopia-canon"],
                )
            )
        except Exception as e:
            logger.debug("skipped SOTOPIA row %d: %s", i, e)

    if tag_filter:
        scenarios = [s for s in scenarios if any(t in s.tags for t in tag_filter)]
    return scenarios


def load_scenarios(*, limit: int, prefer_hf: bool = True) -> list[Scenario]:
    """Load scenarios suitable for longitudinal (repeated-session) evaluation."""
    scenarios: list[Scenario] = []
    if prefer_hf:
        scenarios = _load_hf_scenarios(tag_filter=["cooperative", "longitudinal"])
    if not scenarios:
        logger.info("using %d bundled seed scenarios", len(_SEED_SCENARIOS))
        scenarios = list(_SEED_SCENARIOS)
    if limit and limit > 0:
        scenarios = scenarios[:limit]
    return scenarios
