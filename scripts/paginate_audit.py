#!/usr/bin/env python3
"""Audit list endpoints: map each method to its paging mode + item_key.

Heuristic:
  - GET with `limit` (and `offset` OR `cursor`) query param → paginated.
  - Response schema has ONE $ref-to-array property → that's the item_key.

Output: CSV at repo_root/PAGINATE_MAP.csv
Columns: path, mode, item_key, total_key, operation_id
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPEC = REPO / "openapi.json"
OUT = REPO / "PAGINATE_MAP.csv"


def extract(spec: dict) -> list[dict]:
    results: list[dict] = []
    schemas = spec.get("components", {}).get("schemas", {})

    for path, ops in spec.get("paths", {}).items():
        for verb, op in ops.items():
            if verb.upper() != "GET":
                continue
            params = op.get("parameters", [])
            names = {p.get("name") for p in params}
            if "limit" not in names:
                continue

            mode = None
            if "offset" in names:
                mode = "offset"
            elif "cursor" in names or "page_token" in names:
                mode = "cursor"
            else:
                continue

            resp = op.get("responses", {}).get("200", {})
            content = resp.get("content", {}).get("application/json", {})
            schema_ref = content.get("schema", {}).get("$ref")
            if not schema_ref:
                continue
            schema_name = schema_ref.rsplit("/", 1)[-1]
            schema = schemas.get(schema_name, {})
            props = schema.get("properties", {})

            item_key = None
            for name, desc in props.items():
                t = desc.get("type")
                is_array = t == "array" or (isinstance(t, list) and "array" in t)
                if is_array:
                    items = desc.get("items", {})
                    iref = items.get("$ref") or ""
                    if iref:
                        item_key = name
                        break

            if not item_key:
                continue

            total_key = "total" if "total" in props else None

            results.append({
                "path": path,
                "mode": mode,
                "item_key": item_key,
                "total_key": total_key or "",
                "operation_id": op.get("operationId", ""),
            })
    return results


def main() -> int:
    spec = json.loads(SPEC.read_text())
    rows = extract(spec)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["path", "mode", "item_key", "total_key", "operation_id"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} with {len(rows)} paginated endpoints")
    for r in rows[:10]:
        print(f"  {r['path']} ({r['mode']}, items={r['item_key']}, total={r['total_key']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
