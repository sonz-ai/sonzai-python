"""Markdown failure-report generator for LongMemEval bench runs.

Consumes ``failures.json`` written by ``aggregate.py`` and produces a
human-readable markdown report grouped by subtype → failure bucket →
individual question. Supports optional ``--subtype`` and ``--bucket``
filters so a reviewer can focus on one slice without re-aggregating.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def format_report(
    failures: list[dict],
    *,
    subtype: str | None = None,
    bucket: str | None = None,
) -> str:
    """Format the failure list as markdown.

    Grouping: subtype → bucket → individual failure entry. Optional
    filters drop entries that don't match; the header is always present
    even when no entries remain.
    """
    filtered = [
        f for f in failures
        if (subtype is None or f.get("question_type") == subtype)
        and (bucket is None or f.get("bucket") == bucket)
    ]

    lines: list[str] = []
    lines.append("# LongMemEval Failure Report")
    lines.append("")
    lines.append(f"Total failures: **{len(filtered)}**"
                 + (f" (filtered from {len(failures)})" if len(filtered) != len(failures) else ""))
    lines.append("")

    # Group.
    by_subtype: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for f in filtered:
        by_subtype[f.get("question_type", "unknown")][f.get("bucket", "unknown")].append(f)

    for st in sorted(by_subtype):
        lines.append(f"### {st}")
        lines.append("")
        for bk in sorted(by_subtype[st]):
            entries = by_subtype[st][bk]
            lines.append(f"#### {bk} ({len(entries)} failures)")
            lines.append("")
            for f in entries:
                lines.extend(_format_entry(f))
                lines.append("")
        lines.append("")

    return "\n".join(lines)


def _format_entry(f: dict) -> list[str]:
    qid = f.get("question_id", "?")
    question = f.get("question", "")
    expected = f.get("answer", "")
    agent = f.get("agent_answer", "")
    rationale = f.get("qa_rationale", "")
    expected_sessions = f.get("expected_sessions", [])
    top10 = f.get("retrieved_top10", [])
    hit_ranks = f.get("hit_ranks", [])
    hit_str = f"[{', '.join(str(r) for r in hit_ranks)}]" if hit_ranks else "NONE"

    return [
        f"##### Q: `{qid}` — \"{question}\"",
        f"- **Expected:** {expected}",
        f"- **Agent said:** {agent}",
        f"- **Judge:** {rationale}",
        f"- **Expected sessions:** {expected_sessions}",
        f"- **Top-10 retrieved sessions:** {top10}",
        f"- **Hit ranks:** {hit_str}",
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Render LongMemEval bench failures as markdown")
    p.add_argument("--failures", default="failures.json",
                   help="Path to failures.json written by aggregate (default: ./failures.json)")
    p.add_argument("--output", default="report.md",
                   help="Path to write markdown report (default: ./report.md)")
    p.add_argument("--subtype", default=None, help="Filter to one subtype")
    p.add_argument("--bucket", default=None, help="Filter to one bucket")
    args = p.parse_args(argv)

    failures = json.loads(Path(args.failures).read_text())
    md = format_report(failures, subtype=args.subtype, bucket=args.bucket)
    Path(args.output).write_text(md)
    print(f"wrote {args.output} ({len(failures)} failures, filtered subtype={args.subtype} bucket={args.bucket})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
