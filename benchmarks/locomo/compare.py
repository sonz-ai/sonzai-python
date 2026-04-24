"""Head-to-head JSONL diff for LoCoMo runs.

Usage (from run.py --compare): load each JSONL file, compute per-category
accuracy + token-F1 + R@K, render a markdown table with one column per file.

Column order = argv order so the caller controls which backend appears on
the left.
"""

from __future__ import annotations

import json
from pathlib import Path

from .scoring import KS, aggregate_rows


def load_jsonl(path: str | Path) -> list[dict]:
    rows: list[dict] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _label_for(path: str | Path, rows: list[dict]) -> str:
    # Prefer explicit "backend" tag; fall back to filename stem.
    if rows and "backend" in rows[0]:
        return str(rows[0]["backend"])
    return Path(path).stem


def render_table(per_file: dict[str, list[dict]]) -> str:
    if len(per_file) < 2:
        raise ValueError("compare needs at least 2 files")

    labels = list(per_file.keys())
    aggs = {k: aggregate_rows(v) for k, v in per_file.items()}
    categories = sorted({c for a in aggs.values() for c in a["per_category"].keys()})

    lines: list[str] = []
    header = "| Category |" + "".join(f" {lbl} (J) | {lbl} (F1) |" for lbl in labels)
    sep = "|---|" + "".join(["---:|"] * (2 * len(labels)))
    lines.append(header)
    lines.append(sep)
    for cat in categories:
        row = [f"| {cat} |"]
        for lbl in labels:
            m = aggs[lbl]["per_category"].get(cat, {})
            row.append(f" {m.get('llm_accuracy', 0):.3f} |")
            row.append(f" {m.get('token_f1', 0):.3f} |")
        lines.append("".join(row))
    # Overall row
    overall_row = ["| **Overall** |"]
    for lbl in labels:
        o = aggs[lbl]["overall"]
        overall_row.append(f" **{o.get('llm_accuracy', 0):.3f}** |")
        overall_row.append(f" {o.get('token_f1', 0):.3f} |")
    lines.append("".join(overall_row))

    lines.append("")
    lines.append("### Retrieval (session-level, any-hit recall)")
    rheader = "| k |" + "".join(f" {lbl} R@k | {lbl} NDCG@k |" for lbl in labels)
    rsep = "|---|" + "".join(["---:|"] * (2 * len(labels)))
    lines.append(rheader)
    lines.append(rsep)
    for k in KS:
        row = [f"| {k} |"]
        for lbl in labels:
            o = aggs[lbl]["overall"]
            row.append(f" {o.get(f'recall_any@{k}', 0):.3f} |")
            row.append(f" {o.get(f'ndcg_any@{k}', 0):.3f} |")
        lines.append("".join(row))

    return "\n".join(lines)


def main(paths: list[str]) -> int:
    per_file: dict[str, list[dict]] = {}
    for path in paths:
        rows = load_jsonl(path)
        label = _label_for(path, rows)
        if label in per_file:
            label = f"{label} ({Path(path).stem})"
        per_file[label] = rows
    print(render_table(per_file))
    return 0
