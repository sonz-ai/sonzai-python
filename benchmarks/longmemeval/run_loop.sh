#!/usr/bin/env bash
# run_loop.sh — sequential multi-run bench driver for LongMemEval error analysis.
#
# Usage:
#   ./run_loop.sh [N] [extra bench args...]
#
# Example:
#   ./run_loop.sh 5 --limit 100
#
# Produces N timestamped JSONL files under results/, named
#   sonzai_YYYYMMDD-HHMMSS_runK.jsonl
# so they can be passed to `python -m benchmarks.longmemeval.aggregate results/sonzai_*.jsonl`.
#
# Never passes --reuse-agents: agent reuse corrupts multi-run variance measurements.
set -euo pipefail

N="${1:-5}"
shift || true

# Guard: caller must not have forwarded --reuse-agents. Agent pollution across
# runs invalidates the whole premise of multi-run CI tightening.
for arg in "$@"; do
  if [ "$arg" = "--reuse-agents" ]; then
    echo "error: --reuse-agents is incompatible with run_loop.sh" >&2
    echo "       Agent reuse pollutes memory across runs; the multi-run CI" >&2
    echo "       we're producing assumes fresh agents per question per run." >&2
    exit 2
  fi
done

# Canonical results directory (relative to this script's parent).
here="$(cd "$(dirname "$0")" && pwd)"
out_dir="$here/results"
mkdir -p "$out_dir"

# python -m benchmarks.longmemeval needs the repo root on sys.path.
repo_root="$(cd "$here/../.." && pwd)"
cd "$repo_root"

# One timestamp for the whole batch so all N files sort together.
ts="$(date +%Y%m%d-%H%M%S)"

echo "run_loop: starting $N sequential runs, timestamp=$ts"
for i in $(seq 1 "$N"); do
  out="$out_dir/sonzai_${ts}_run${i}.jsonl"
  echo "---"
  echo "run $i/$N  ->  $out"
  echo "---"
  python -m benchmarks.longmemeval --output "$out" "$@"
done

echo
echo "run_loop: $N runs complete. Aggregate with:"
echo "  python -m benchmarks.longmemeval.aggregate $out_dir/sonzai_${ts}_run*.jsonl"
