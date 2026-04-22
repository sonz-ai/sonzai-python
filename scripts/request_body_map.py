#!/usr/bin/env python3
"""Audit every resource method's POST/PUT/PATCH call and pair it with
the matching spec input body class.

Output: CSV at repo_root/REQUEST_BODY_MAP.csv
Columns: resource_file, method_name, http_verb, path, input_body_class

Usage:
    uv run --extra dev python scripts/request_body_map.py
"""

from __future__ import annotations

import ast
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESOURCES = REPO / "src/sonzai/resources"
SPEC = REPO / "openapi.json"
OUT = REPO / "REQUEST_BODY_MAP.csv"


def normalize(path: str) -> str:
    p = path.split("?", 1)[0]
    if p.startswith("/api/v1"):
        p = p[len("/api/v1"):]
    p = re.sub(r"\{[^}]+\}", "{param}", p)
    return p.rstrip("/") or "/"


def load_spec_bodies() -> dict[tuple[str, str], str | None]:
    spec = json.loads(SPEC.read_text())
    out: dict[tuple[str, str], str | None] = {}
    for path, ops in spec.get("paths", {}).items():
        for verb, op in ops.items():
            if verb.upper() not in ("POST", "PUT", "PATCH"):
                continue
            key = (verb.upper(), normalize(path))
            body = op.get("requestBody", {}).get("content", {})
            ref = None
            for content_type, content in body.items():
                schema = content.get("schema", {})
                ref = schema.get("$ref")
                if ref:
                    break
            if ref:
                out[key] = ref.rsplit("/", 1)[-1]
            else:
                out[key] = None
    return out


def extract_path(node: ast.AST, class_vars: dict[str, str]) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        out = ""
        for v in node.values:
            if isinstance(v, ast.Constant):
                out += str(v.value)
            elif isinstance(v, ast.FormattedValue):
                out += "{param}"
        return out
    if isinstance(node, ast.Name) and node.id in class_vars:
        return class_vars[node.id]
    return None


def audit_resource(path: Path, spec_bodies: dict) -> list[dict]:
    tree = ast.parse(path.read_text())
    results: list[dict] = []
    for cls in ast.walk(tree):
        if not isinstance(cls, ast.ClassDef):
            continue
        for func in [n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            for call in ast.walk(func):
                if not isinstance(call, ast.Call):
                    continue
                f = call.func
                if not isinstance(f, ast.Attribute):
                    continue
                if f.attr not in ("post", "put", "patch"):
                    continue
                if call.args:
                    path_node = call.args[0]
                    literal_path = extract_path(path_node, {})
                    if literal_path:
                        key = (f.attr.upper(), normalize(literal_path))
                        body_cls = spec_bodies.get(key)
                        results.append({
                            "resource_file": path.name,
                            "method_name": func.name,
                            "http_verb": f.attr.upper(),
                            "path": literal_path,
                            "input_body_class": body_cls or "",
                        })
    return results


def main() -> int:
    spec_bodies = load_spec_bodies()
    rows: list[dict] = []
    for rf in sorted(RESOURCES.glob("*.py")):
        if rf.name == "__init__.py":
            continue
        rows.extend(audit_resource(rf, spec_bodies))
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["resource_file", "method_name", "http_verb", "path", "input_body_class"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} with {len(rows)} rows")
    missing = [r for r in rows if not r["input_body_class"]]
    if missing:
        print(f"{len(missing)} call(s) without a spec input body class:")
        for m in missing[:10]:
            print(f"  {m['resource_file']}:{m['method_name']} {m['http_verb']} {m['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
