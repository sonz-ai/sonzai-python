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


# Hand-picked seed scenarios with enriched partner personas — the "user" side
# of each conversation carries ~200–300 words of personal history, preferences,
# quirks, and current-life context. Rich latent structure is what lets a
# memory system demonstrate "understanding" (compressing scattered turns into
# a model of the user) beyond "remembering" (verbatim recall of what was said).
#
# Scenario IDs are prefixed ``rich-*`` so runs against these personas get
# fresh pinned agents / fresh palaces rather than bleeding in with state from
# older thin-persona runs against ``seed-*`` IDs.
_SEED_SCENARIOS: list[Scenario] = [
    Scenario(
        scenario_id="rich-mentorship",
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
            name="Alex Chen",
            background=(
                "28-year-old junior engineer, two months into their first full-time "
                "software role at a mid-size fintech in Toronto. Grew up in Vancouver, "
                "only child of first-gen Taiwanese immigrants who ran a small bakery; "
                "mom passed in 2024 and the bakery is now leased out. Took a winding "
                "path to engineering — started in structural at UBC, switched to CS "
                "mid-degree after building a scheduler for the bakery POS. Graduated "
                "2025 with side projects in Elm (a tarot-drawing web app) and a "
                "scheduling tool for the local mahjong club. "
                "Communicates with classic early-career patterns: over-apologizes, "
                "hedges with 'I could be wrong, but…', quotes docs verbatim to mask "
                "uncertainty. Gets defensive in 1:1s when feeling judged; lights up "
                "on concrete technical puzzles. Reads fantasy (Sanderson, Jemisin), "
                "plays D&D Fridays (Rogue, never DMs), makes pour-over coffee every "
                "morning as a ritual. Tabby cat named Pickle; long-distance partner "
                "Kai in Vancouver. "
                "Current life: paying down $28k in student loans, quietly considering "
                "a part-time CS MS (hasn't told anyone), feels imposter syndrome as "
                "the only junior on a senior team, loves the work but worries the "
                "pace isn't sustainable. Prefers written feedback, async over sync, "
                "does their best thinking on 6am walks."
            ),
            goal=(
                "Grow as an engineer without burning out; get concrete, actionable "
                "feedback that doesn't feel patronizing."
            ),
            secret=(
                "Secretly interviewing at a larger FAANG-type company for next month; "
                "hasn't decided whether to tell Mika."
            ),
        ),
        max_turns=12,
        tags=["cooperative", "longitudinal"],
    ),
    Scenario(
        scenario_id="rich-therapy",
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
            name="Jordan Rivera",
            background=(
                "34-year-old senior product manager at a mid-size SaaS company in "
                "Oakland, started therapy six months ago for work-related anxiety "
                "that has bled into sleep. Grew up in Sacramento, oldest of three; "
                "parents divorced when Jordan was nine and Jordan became the stable "
                "one — classic 'parentified' older sibling. Bachelor's in psychology "
                "(UC Santa Cruz), unrelated to the current career; drifted into PM "
                "via a startup operations role. "
                "Married to Sam (elementary-school teacher) for four years; two dogs, "
                "Moxie (corgi) and Biscuit (mutt). No kids, both leaning no. "
                "Communicates carefully — uses lots of meta-commentary ('let me try "
                "to say this better…'), rarely cries in session but sometimes goes "
                "quiet mid-sentence. Highly self-aware, reads pop-psych books, uses "
                "therapy vocabulary sometimes defensively. Exercises compulsively "
                "when anxious (morning runs, weekend rock climbing). Strong opinions "
                "about public transit and zoning. Avoids alcohol after watching dad "
                "spiral on it. "
                "Current life: promoted to senior PM in February, inherited a failing "
                "product line, worked 60-hour weeks for three months and is now "
                "crashing. Anxious about the quarterly review in three weeks. Sleep "
                "broken since May. Has started, then stopped, journaling four times. "
                "Favorite comfort: long drives to nowhere with Sam, windows down."
            ),
            goal=(
                "Stop the anxiety from taking over; leave each session with one "
                "concrete idea to try."
            ),
            secret=(
                "Has been mentally rehearsing a 'I quit' conversation with the "
                "manager and feels guilty about it — hasn't told Sam."
            ),
        ),
        max_turns=14,
        tags=["cooperative", "longitudinal", "emotional"],
    ),
    Scenario(
        scenario_id="rich-language-tutor",
        codename="Weekly Spanish lesson",
        setting=(
            "A language tutor works with a returning student. Over sessions they "
            "adapt to the student's progress and preferences."
        ),
        agent=Character(
            name="Profesora Elena",
            background="Native Spanish speaker, 10 years tutoring experience.",
            goal="Move the student one level up in fluency over the term.",
            secret="Elena is doubling her rate next month.",
        ),
        partner=Character(
            name="Sam Okafor",
            background=(
                "42-year-old mechanical engineer at an aerospace supplier in Seattle, "
                "learning Spanish for a three-week family trip to Madrid and "
                "Barcelona in November. Born in Houston to Nigerian immigrants, "
                "raised bilingual English/Igbo at home; high-school French never "
                "really stuck. This is Sam's first serious language attempt as an "
                "adult. "
                "Married to Lena (graphic designer) for eleven years; two kids — "
                "Chioma (9, into soccer) and Adaeze (6, into dinosaurs). The Spain "
                "trip is a belated anniversary celebration and a reconnection after "
                "a rough year — Lena's father passed in March. "
                "Communicates literally: engineer's mind, asks for rules and "
                "patterns, gets frustrated when the language 'just doesn't follow "
                "logic.' Finds grammar drills demotivating but hasn't said so — "
                "keeps showing up for them. Gets embarrassed about pronunciation; "
                "avoids recording spoken homework. Loves sci-fi audiobooks on "
                "commutes; home-brews beer; plays competitive chess at the local "
                "club (1780 Elo, climbing slowly). "
                "Current life: just bought a house in Ballard; two cats and a "
                "spaniel; kids' school drop-off every morning at 7:45; tutors "
                "daughter Chioma in math on Sundays. Quietly proud of the household "
                "he's built. Prefers lessons at 8pm after kids go down; thinks a "
                "30-min daily session is more sustainable than a weekly 60."
            ),
            goal=(
                "Be conversational enough to order food, navigate the city, and "
                "small-talk with Lena's Spanish-speaking relatives on the trip; "
                "not embarrass the family."
            ),
            secret=(
                "Finds grammar drills demotivating and has been quietly considering "
                "switching tutors — doesn't want to hurt Elena's feelings."
            ),
        ),
        max_turns=10,
        tags=["cooperative", "longitudinal", "knowledge-transfer"],
    ),
    Scenario(
        scenario_id="rich-fitness-coach",
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
            name="Taylor Nguyen",
            background=(
                "31-year-old software engineer at a major cloud provider in Austin, "
                "desk worker starting serious strength training for the first time "
                "after a decade of 'I'll get to it.' Daughter of first-gen Vietnamese "
                "refugees, grew up in Houston; older brother Minh is a doctor in "
                "Dallas. Single, lives alone in a South Congress condo with a shiba "
                "inu named Beanie. Dated someone for five years, broke up in 2024; "
                "dating-app fatigue is a recurring theme. "
                "Communicates politely with a self-deprecating edge; makes jokes when "
                "nervous; apologizes for missed sessions by front-loading context "
                "('ugh, okay so what happened was…'). Perfectionist — avoids sharing "
                "numbers until they're 'ready' (shared bodyweight only on week four). "
                "Family history of Type-2 diabetes and cardiovascular disease — the "
                "real reason for starting — but leads with aesthetics because it "
                "feels less heavy. "
                "Preferences: 5:30am workouts, hates running, loves rowing, oddly "
                "into deadlifts. Pickleball with coworkers on weekends. Cooks "
                "Vietnamese food on Sundays for the week. Two cups of coffee, no "
                "alcohol on weekdays. Lifts to lo-fi and '90s R&B. "
                "Current life: promoted six months ago, imposter syndrome about it; "
                "saving for a house; seeing a therapist named Mia every other week; "
                "just got back from a solo trip to Japan. Has a bad left knee from "
                "a 2022 skiing incident and is paranoid about re-injuring it."
            ),
            goal=(
                "Hit the 6-month strength milestones (deadlift 2x bodyweight, squat "
                "1.5x) without getting injured, and do it consistently."
            ),
            secret=(
                "Has skipped two sessions in the last month and told Dev they went "
                "well; feels guilty but doesn't want to lose face."
            ),
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
