"""LoCoMo dataset loader.

Dataset source:
    https://raw.githubusercontent.com/snap-research/locomo/main/data/locomo10.json

Each sample has:
- conversation.speaker_a / speaker_b: the two participants' display names
- conversation.session_N: list of turn dicts (speaker, dia_id, text)
- conversation.session_N_date_time: human-readable timestamp string
- qa: list of {question, answer, evidence: [dia_id...], category: 1..5}

Category 5 is adversarial (unanswerable); filtered by default — matches
mem0's published methodology so our numbers compare directly.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from ..common.dataset_cache import ensure_file

DATASET_URL = (
    "https://raw.githubusercontent.com/snap-research/locomo/main/data/locomo10.json"
)
DATASET_FILE = "locomo10.json"

# LoCoMo dates look like: "1:00 pm on 8 May, 2023"
_LOCOMO_DT_RE = re.compile(
    r"^\s*(\d{1,2}):(\d{2})\s*(am|pm)\s+on\s+(\d{1,2})\s+([A-Za-z]+),?\s+(\d{4})\s*$",
    re.IGNORECASE,
)
_MONTH_MAP = {
    m.lower(): i for i, m in enumerate(
        ["", "January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"],
        start=0,
    ) if i > 0
}


@dataclass
class LocomoTurn:
    speaker: str
    dia_id: str
    text: str
    img_url: str = ""
    blip_caption: str = ""


@dataclass
class LocomoSession:
    index: int
    date_time: str
    turns: list[LocomoTurn]

    @property
    def parsed_date_time(self) -> datetime:
        return parse_locomo_datetime(self.date_time)


@dataclass
class LocomoQA:
    question: str
    answer: str
    category: int
    evidence: list[str] = field(default_factory=list)
    adversarial_answer: str = ""


@dataclass
class LocomoSample:
    sample_id: str
    speaker_a: str
    speaker_b: str
    sessions: list[LocomoSession]
    qa: list[LocomoQA]


def parse_locomo_datetime(raw: str) -> datetime:
    """Parse LoCoMo's "1:00 pm on 8 May, 2023" format.

    Returns datetime.min on parse failure so callers can sort by index order
    as a fallback without raising. This is intentional — the dataset is hand-
    annotated and string formats drift slightly between samples.
    """
    m = _LOCOMO_DT_RE.match(raw or "")
    if not m:
        return datetime.min
    hour, minute, ampm, day, month_name, year = m.groups()
    month = _MONTH_MAP.get(month_name.lower())
    if month is None:
        return datetime.min
    h = int(hour) % 12
    if ampm.lower() == "pm":
        h += 12
    try:
        return datetime(int(year), month, int(day), h, int(minute))
    except ValueError:
        return datetime.min


def _build_turns(raw_turns: list[dict]) -> list[LocomoTurn]:
    out: list[LocomoTurn] = []
    for t in raw_turns:
        out.append(
            LocomoTurn(
                speaker=str(t.get("speaker") or ""),
                dia_id=str(t.get("dia_id") or ""),
                text=str(t.get("text") or ""),
                img_url=str(t.get("img_url") or ""),
                blip_caption=str(t.get("blip_caption") or ""),
            )
        )
    return out


def _build_sample(raw: dict, sample_id_fallback: str) -> LocomoSample:
    conv = raw.get("conversation") or {}
    speaker_a = str(conv.get("speaker_a") or "")
    speaker_b = str(conv.get("speaker_b") or "")

    sessions: list[LocomoSession] = []
    for key in conv.keys():
        if not key.startswith("session_") or key.endswith("_date_time"):
            continue
        if key in ("speaker_a", "speaker_b"):
            continue
        try:
            idx = int(key.split("_", 1)[1])
        except (ValueError, IndexError):
            continue
        raw_turns = conv.get(key) or []
        if not isinstance(raw_turns, list):
            continue
        dt_key = f"{key}_date_time"
        sessions.append(
            LocomoSession(
                index=idx,
                date_time=str(conv.get(dt_key) or ""),
                turns=_build_turns(raw_turns),
            )
        )

    # Sort by parsed date_time; on ties or unparseable dates, fall back to index.
    sessions.sort(key=lambda s: (s.parsed_date_time, s.index))

    qa_list: list[LocomoQA] = []
    for qa in raw.get("qa") or []:
        qa_list.append(
            LocomoQA(
                question=str(qa.get("question") or ""),
                answer=str(qa.get("answer") or ""),
                category=int(qa.get("category") or 0),
                evidence=[str(e) for e in (qa.get("evidence") or [])],
                adversarial_answer=str(qa.get("adversarial_answer") or ""),
            )
        )

    return LocomoSample(
        sample_id=str(raw.get("sample_id") or sample_id_fallback),
        speaker_a=speaker_a,
        speaker_b=speaker_b,
        sessions=sessions,
        qa=qa_list,
    )


def load_samples(*, limit: int = 0, path: "str | Path | None" = None) -> list[LocomoSample]:
    """Load LoCoMo samples, auto-downloading the dataset on first run.

    ``limit=0`` returns all samples. ``path`` overrides the cached default —
    pass a fixture path for tests.
    """
    target = Path(path) if path else ensure_file(DATASET_URL, DATASET_FILE)
    with open(target) as f:
        raw = json.load(f)
    samples = [
        _build_sample(item, sample_id_fallback=f"locomo-{i}")
        for i, item in enumerate(raw)
    ]
    if limit and limit > 0:
        samples = samples[:limit]
    return samples


def load_qa(
    samples: list[LocomoSample], *, include_adversarial: bool = False,
) -> list[tuple[LocomoSample, LocomoQA]]:
    """Flatten samples into (sample, qa) pairs. Category 5 filtered by default."""
    out: list[tuple[LocomoSample, LocomoQA]] = []
    for s in samples:
        for qa in s.qa:
            if qa.category == 5 and not include_adversarial:
                continue
            out.append((s, qa))
    return out
