"""On-demand dataset download with a user-level cache.

Datasets live under ``~/.cache/sonzai-bench/`` so repeat runs don't re-download.
"""

from __future__ import annotations

import os
import shutil
import urllib.request
from pathlib import Path

from tqdm import tqdm


def cache_root() -> Path:
    override = os.environ.get("SONZAI_BENCH_CACHE")
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / ".cache" / "sonzai-bench"


def ensure_file(url: str, filename: str) -> Path:
    """Download ``url`` to ``cache_root() / filename`` if missing. Returns the path."""
    target = cache_root() / filename
    if target.exists() and target.stat().st_size > 0:
        return target

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".part")

    with urllib.request.urlopen(url) as resp:  # noqa: S310 — trusted HF URL
        total = int(resp.headers.get("Content-Length", 0)) or None
        with open(tmp, "wb") as f, tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            desc=f"Downloading {filename}",
        ) as bar:
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
                bar.update(len(chunk))

    shutil.move(str(tmp), str(target))
    return target
