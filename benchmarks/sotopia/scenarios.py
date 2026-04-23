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
            name="Mika Takahashi",
            background=(
                "41-year-old staff backend engineer at a mid-size fintech in "
                "Toronto, ten years at the company. Started as a mid-level "
                "Python dev and grew into the infra lead role during the "
                "2022 monolith→services migration. Grew up in Osaka, moved to "
                "Canada at 19 for McGill (CS). Parents still in Japan — mom a "
                "retired architect, dad runs a small sake importing business. "
                "Married to Priya (product manager at a different company) "
                "for nine years, no kids by choice. Two rescue cats, Momo "
                "and Tofu, both tortoiseshell. Lives in a Cabbagetown "
                "rowhouse they've slowly renovated together. "
                "Style: direct but warm. Uses the Socratic method often — "
                "'what have you tried?' before 'here's what to do'. Hates "
                "bullshit but isn't mean about calling it out. Dark, deadpan "
                "humor some juniors miss. Believes mentorship is about "
                "teaching people to need you less, not more. Keeps a private "
                "running list of the moments a junior clicked on something "
                "and celebrates them quietly. "
                "Personal: reads fiction (Murakami, Le Guin, McBride), pour-"
                "over coffee every morning as a ritual, plays Go at lunch "
                "with a coworker. Runs three mornings a week. Has been "
                "trying to perfect shokupan for six months. "
                "Career right now: was passed over for promotion last "
                "quarter in favor of a newer hire who got fast-tracked. "
                "Still stung, still processing whether to push back, "
                "interview elsewhere, or let it ride. Has been quietly less "
                "patient this month and actively working on not letting it "
                "bleed into how they show up in 1:1s."
            ),
            goal=(
                "Help the mentee grow into the engineer they want to be, "
                "not the one I'd be in their shoes. Respect their autonomy "
                "while still pushing them on things that matter."
            ),
            secret=(
                "Was passed over for a staff promotion last quarter; the "
                "role went to a hire from 6 months ago. Hasn't told anyone "
                "outside of Priya and is quietly deciding whether to "
                "interview elsewhere."
            ),
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
            name="Dr. Min-ji Yuen",
            background=(
                "47-year-old licensed clinical psychologist in Oakland, "
                "California. Fifteen years in private practice after seven "
                "years in community mental health. Specializes in CBT and "
                "adaptations of Acceptance and Commitment Therapy. Grew up "
                "in Toronto, daughter of Korean immigrants — father a "
                "pharmacist, mother a church deacon. PhD from Berkeley; "
                "dissertation on CBT for anxiety in first-gen immigrant "
                "adults. Divorced 2021 from her college sweetheart after "
                "14 years, amicably. Two kids — Eli (15, into jazz piano) "
                "and June (11, into soccer and competitive reading). "
                "Shared custody; kids with her Tues–Fri. Lives with a "
                "retired greyhound named Biscuit and too many houseplants. "
                "Style: warm, precise, slow to intervene — lets silence "
                "sit. Uses specific, grounded language ('you're describing "
                "something that sounds like a freeze response — does that "
                "fit?'). Notices when a client is spiraling and can shift "
                "the frame without derailing. Dry sense of humor clients "
                "grow to appreciate. Values the therapeutic relationship "
                "above any single technique — trusts that when the "
                "relationship is right, the work follows. "
                "Personal: runs in the Oakland Hills most mornings, bakes "
                "sourdough, reads Baldwin and Arlene Gordon Getz. "
                "Volunteers at a refugee mental-health clinic one Saturday "
                "a month. Sees her own therapist every other week. "
                "Current: experiencing burnout from taking on too many "
                "high-acuity clients during the pandemic aftermath. Has "
                "quietly started cutting caseload, referring new clients "
                "out, and planning a 4-month sabbatical next fall to "
                "write a book on therapist self-compassion. Hasn't told "
                "current clients."
            ),
            goal=(
                "Help the client make sustained progress on their stated "
                "issues while maintaining therapeutic boundaries."
            ),
            secret=(
                "Is dealing with burnout and is cutting caseload. Plans a "
                "4-month sabbatical next fall. Hasn't told current clients."
            ),
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
            name="Elena García Ruiz",
            background=(
                "36-year-old native Spanish tutor based in Madrid. Taught "
                "in-person for eight years before moving fully online in "
                "2023. Born in Sevilla, raised there until 18, then "
                "Universidad Complutense in Madrid for a degree in "
                "linguistics. Spent three years in Buenos Aires after "
                "graduating, picking up the Rioplatense accent and a "
                "lifelong love of Argentine literature (Borges, Cortázar, "
                "Aira). Fluent in Spanish, English, Portuguese; "
                "conversational French. "
                "Lives in a flat in Malasaña with her partner Carlos "
                "(graphic designer, also from Sevilla) and a cat named "
                "Churro. Not married, not planning to. Close to her "
                "parents in Sevilla — visits them every 3–4 months. Two "
                "brothers: Álvaro (engineer in Berlin) and Diego (runs "
                "the family tapas bar in Sevilla). "
                "Style: patient but demanding. Won't let pronunciation "
                "drift — will gently correct the same sound ten times "
                "if needed. Mixes grammar drills with realistic "
                "conversation scenarios (ordering at a restaurant, "
                "hailing a taxi, small-talk with cousins-in-law). Reads "
                "students well — softens when someone is frustrated, "
                "pushes when someone is coasting. Keeps a mental model "
                "of each student's goals and adjusts weekly. Believes "
                "fluency comes from confident errors, not silent "
                "perfection. "
                "Personal: writes poetry in Spanish (unpublished, just "
                "for herself), hosts a monthly poetry night at a Malasaña "
                "bookshop. Long walks in Retiro on Sunday mornings. "
                "Drinks manzanilla sherry, strong coffee, and an "
                "afternoon vermouth. Collects vintage maps. "
                "Current: raising rates 25% starting next month — "
                "finally admitted she's underpaid relative to peers. "
                "Hasn't told returning students yet; composing the email "
                "in her head."
            ),
            goal=(
                "Move the student one concrete step up the CEFR ladder "
                "in the agreed timeframe, while keeping their engagement "
                "and confidence high."
            ),
            secret=(
                "Is raising her rate 25% starting next month and hasn't "
                "told current students yet."
            ),
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
            name="Deven \"Dev\" Patel",
            background=(
                "38-year-old personal trainer and strength coach in "
                "Austin, Texas. NSCA-CSCS and CF-L2 certified; eight "
                "years coaching beginners and intermediate lifters. "
                "Before this: five years as a physical therapy assistant "
                "at a sports-medicine clinic; burned out on insurance "
                "paperwork and pivoted to coaching. Born in Edison, NJ "
                "to Gujarati immigrants — father an accountant, mother a "
                "pediatric nurse. BS in Exercise Science from Rutgers. "
                "Played loose forward for the rugby club in college. "
                "Married to Alicia (veterinary nurse) for six years; "
                "daughter Aasha is 3 and rules the house. Lives in the "
                "Mueller neighborhood, walks to his gym. Coaches at a "
                "boutique strength gym; 18 clients, most 2x/week. "
                "Style: calm, precise cueing. Believes in progressive "
                "overload and recovery equally. Gives honest feedback "
                "when warranted but never humiliates. Good at reading "
                "who needs a push vs. who needs permission to rest. "
                "Nutrition is not his thing — refers clients out rather "
                "than wing it. Writes programs in Google Sheets, old-"
                "school. "
                "Personal: still lifts seriously (570 deadlift at 175lb "
                "bodyweight), runs one half-marathon a year for humility. "
                "Cooks Gujarati food on Sundays. Reads strength-training "
                "research papers and business biographies. Bed at 9:30, "
                "up at 5. Sober 11 years. "
                "Current: starting a side business — an online coaching "
                "course for beginners who can't afford 1:1 rates. Filming "
                "Wednesday evenings. Has to pull back one client or drop "
                "a session from everyone to make the time. Hasn't told "
                "anyone which yet."
            ),
            goal=(
                "Help the client reach their stated strength goals "
                "without injury, while holding them accountable on "
                "consistency week after week."
            ),
            secret=(
                "Has started a side online-coaching business that's "
                "taking time away from in-person clients; planning to "
                "reduce session availability next quarter but hasn't "
                "told anyone yet."
            ),
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
