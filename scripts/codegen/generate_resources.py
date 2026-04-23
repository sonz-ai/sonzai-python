#!/usr/bin/env python3
"""Generate src/sonzai/_generated/resources/<tag>.py from openapi.json.

Usage:
    uv run --extra dev python -m scripts.codegen.generate_resources \
        openapi.json src/sonzai/_generated/resources/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from ._emit import emit_module
from ._parse import parse_spec

INIT_CONTENT = '''"""Auto-generated resource modules.

Do NOT edit files in this directory by hand — they are re-emitted on
every `just regenerate-sdk`.
"""
'''


def main(spec_path: Path, out_dir: Path) -> int:
    spec = json.loads(spec_path.read_text())
    by_tag = parse_spec(spec)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "__init__.py").write_text(INIT_CONTENT)

    for tag, ops in by_tag.items():
        source = emit_module(tag, ops)
        (out_dir / f"{tag}.py").write_text(source)

    print(f"wrote {len(by_tag)} resource modules to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
