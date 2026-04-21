"""Curated Big5 presets for the Personality Shift Demo.

Each preset ships a one-line description and a full Big5 block on the 0-1
scale the Platform stores natively. When applied via the SDK, the backend
automatically re-derives the derived Dimensions (Politeness, Compassion,
Assertiveness, etc.) so prompt-layer behavior updates on the next turn.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Big5:
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float

    def as_dict(self) -> dict[str, float]:
        return {
            "openness": self.openness,
            "conscientiousness": self.conscientiousness,
            "extraversion": self.extraversion,
            "agreeableness": self.agreeableness,
            "neuroticism": self.neuroticism,
        }


@dataclass(frozen=True)
class Preset:
    name: str
    description: str
    big5: Big5


PRESETS: list[Preset] = [
    Preset(
        name="Agreeable",
        description="Warm, cooperative, eager to please. Validates feelings before offering advice.",
        big5=Big5(openness=0.55, conscientiousness=0.50, extraversion=0.72, agreeableness=0.90, neuroticism=0.40),
    ),
    Preset(
        name="Blunt",
        description="Direct, confrontational, willing to disagree. Keeps responses short and dismissive.",
        big5=Big5(openness=0.55, conscientiousness=0.50, extraversion=0.72, agreeableness=0.10, neuroticism=0.50),
    ),
    Preset(
        name="Confident",
        description="Assertive, decisive, takes charge. Makes strong recommendations without hedging.",
        big5=Big5(openness=0.55, conscientiousness=0.70, extraversion=0.90, agreeableness=0.40, neuroticism=0.20),
    ),
    Preset(
        name="Anxious",
        description="Reactive, worried, second-guesses everything. Asks for reassurance.",
        big5=Big5(openness=0.55, conscientiousness=0.50, extraversion=0.30, agreeableness=0.60, neuroticism=0.90),
    ),
    Preset(
        name="Curious",
        description="Inquisitive, exploratory, asks lots of follow-up questions.",
        big5=Big5(openness=0.95, conscientiousness=0.50, extraversion=0.70, agreeableness=0.70, neuroticism=0.30),
    ),
    Preset(
        name="Reserved",
        description="Quiet, thoughtful, minimal words. Speaks only when necessary.",
        big5=Big5(openness=0.55, conscientiousness=0.60, extraversion=0.10, agreeableness=0.60, neuroticism=0.50),
    ),
    Preset(
        name="Volatile",
        description="Emotionally reactive, mood shifts fast, says what's on their mind.",
        big5=Big5(openness=0.55, conscientiousness=0.30, extraversion=0.70, agreeableness=0.30, neuroticism=0.85),
    ),
]


def find_preset(name: str) -> Preset | None:
    for p in PRESETS:
        if p.name == name:
            return p
    return None
