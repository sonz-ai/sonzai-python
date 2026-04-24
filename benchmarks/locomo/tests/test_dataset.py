"""Tests for the LoCoMo dataset loader."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from benchmarks.locomo.dataset import (
    load_qa,
    load_samples,
    parse_locomo_datetime,
)

FIXTURE = Path(__file__).parent / "fixtures" / "mini_locomo.json"


def test_load_samples_shape():
    samples = load_samples(path=FIXTURE)
    assert len(samples) == 1
    sample = samples[0]
    assert sample.sample_id == "fixture-sample-0"
    assert sample.speaker_a == "Alice"
    assert sample.speaker_b == "Bob"
    assert len(sample.sessions) == 2
    assert len(sample.qa) == 3


def test_load_samples_sessions_are_sorted_chronologically():
    samples = load_samples(path=FIXTURE)
    sessions = samples[0].sessions
    assert sessions[0].index == 1
    assert sessions[1].index == 2
    assert sessions[0].parsed_date_time < sessions[1].parsed_date_time


def test_load_samples_turns_preserve_dia_ids():
    samples = load_samples(path=FIXTURE)
    turns = samples[0].sessions[0].turns
    assert [t.dia_id for t in turns] == ["D1:1", "D1:2", "D1:3", "D1:4"]
    assert turns[0].speaker == "Alice"
    assert turns[0].text == "Hi Bob!"


def test_load_samples_limit_truncates():
    samples = load_samples(path=FIXTURE, limit=1)
    assert len(samples) == 1


def test_load_qa_filters_adversarial_by_default():
    samples = load_samples(path=FIXTURE)
    pairs = load_qa(samples)
    categories = [qa.category for _, qa in pairs]
    assert 5 not in categories
    assert len(pairs) == 2


def test_load_qa_include_adversarial():
    samples = load_samples(path=FIXTURE)
    pairs = load_qa(samples, include_adversarial=True)
    assert len(pairs) == 3
    assert any(qa.category == 5 for _, qa in pairs)


def test_parse_locomo_datetime_standard_format():
    dt = parse_locomo_datetime("1:00 pm on 8 May, 2023")
    assert dt == datetime(2023, 5, 8, 13, 0)


def test_parse_locomo_datetime_morning():
    dt = parse_locomo_datetime("9:00 am on 12 May, 2023")
    assert dt == datetime(2023, 5, 12, 9, 0)


def test_parse_locomo_datetime_fallback_on_unparseable():
    """Unparseable strings return datetime.min so callers can fall back to index order."""
    dt = parse_locomo_datetime("nonsense")
    assert dt == datetime.min
