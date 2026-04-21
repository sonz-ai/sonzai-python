"""LongMemEval dataset loader with on-demand download.

Source: https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned

Each question has a ``haystack`` of prior chat sessions and a question that must
be answered from memory alone. We evaluate retrieval (does the top-k contain an
answer-bearing session?) and end-to-end QA (does the agent's answer match the
ground truth?).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime

from ..common.dataset_cache import ensure_file

DATASET_URL = (
    "https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/"
    "resolve/main/longmemeval_s_cleaned.json"
)
DATASET_FILE = "longmemeval_s_cleaned.json"

# LongMemEval dates look like "2023/05/20 (Sat) 09:46".
_DATE_FORMAT = "%Y/%m/%d (%a) %H:%M"


@dataclass
class Turn:
    role: str
    content: str
    has_answer: bool = False


@dataclass
class Session:
    session_id: str
    date: str
    turns: list[Turn]

    @property
    def parsed_date(self) -> datetime:
        return datetime.strptime(self.date, _DATE_FORMAT)


@dataclass
class LongMemEvalQuestion:
    question_id: str
    question_type: str
    question: str
    answer: str
    question_date: str
    sessions: list[Session]
    answer_session_ids: list[str]


def _build_question(raw: dict) -> LongMemEvalQuestion:
    haystack = raw["haystack_sessions"]
    ids = raw["haystack_session_ids"]
    dates = raw["haystack_dates"]
    sessions = [
        Session(
            session_id=sid,
            date=date,
            turns=[
                Turn(
                    role=t["role"],
                    content=t["content"],
                    has_answer=bool(t.get("has_answer", False)),
                )
                for t in turns
            ],
        )
        for sid, date, turns in zip(ids, dates, haystack, strict=True)
    ]
    # LongMemEval haystacks are already in chronological order but sort defensively.
    sessions.sort(key=lambda s: s.parsed_date)

    return LongMemEvalQuestion(
        question_id=raw["question_id"],
        question_type=raw["question_type"],
        question=raw["question"],
        answer=raw["answer"],
        question_date=raw.get("question_date", ""),
        sessions=sessions,
        answer_session_ids=list(raw.get("answer_session_ids", [])),
    )


def load_questions(*, limit: int = 0) -> list[LongMemEvalQuestion]:
    """Load LongMemEval questions, auto-downloading the dataset on first run.

    ``limit=0`` returns all 500 questions.
    """
    path = ensure_file(DATASET_URL, DATASET_FILE)
    with open(path) as f:
        raw = json.load(f)
    questions = [_build_question(q) for q in raw]
    if limit and limit > 0:
        questions = questions[:limit]
    return questions


def hours_between(earlier: Session, later: Session) -> float:
    delta = later.parsed_date - earlier.parsed_date
    return delta.total_seconds() / 3600.0
