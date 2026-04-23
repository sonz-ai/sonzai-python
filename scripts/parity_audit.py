#!/usr/bin/env python3
"""Parity audit: compare OpenAPI paths to SDK method paths.

Walks every resource file under ``src/sonzai/resources/`` and
``src/sonzai/_generated/resources/`` (plus ``_client.py``) with the AST
module, tracks every call to ``self._http.<verb>(...)`` (and ``stream_sse`` /
``upload_file`` / ``request``), recovers the URL path literal via f-string
reconstruction and local/class-wide variable tracking, then cross-references
the result with the operations declared in ``openapi.json``.

An endpoint is "covered" if it's bound in either the hand-written or the
generated resource — hand-written wrappers subclass the generated ones, so
methods missing from the hand-written file are still reachable on the
public client via inheritance.

Writes ``SDK_PARITY_AUDIT.md`` at the repo root summarizing coverage.
Run via ``just regenerate-sdk`` or directly::

    uv run --extra dev python scripts/parity_audit.py
"""

from __future__ import annotations

import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# This file lives at <repo>/scripts/parity_audit.py.
SDK_ROOT = Path(__file__).resolve().parent.parent
SPEC = SDK_ROOT / "openapi.json"
RESOURCES_DIR = SDK_ROOT / "src/sonzai/resources"
GENERATED_RESOURCES_DIR = SDK_ROOT / "src/sonzai/_generated/resources"
CLIENT_PATH = SDK_ROOT / "src/sonzai/_client.py"


def load_spec_paths() -> list[tuple[str, str]]:
    spec = json.load(open(SPEC))
    out = []
    for path, methods in sorted(spec.get("paths", {}).items()):
        for method in methods:
            if method.lower() in ("get", "post", "put", "delete", "patch"):
                out.append((method.upper(), path))
    return out


def normalize_path(p: str) -> str:
    """Normalize ``/api/v1/x`` → ``/x`` and ``{foo}`` placeholders."""
    p = p.split("?", 1)[0]
    if p.startswith("/api/v1"):
        p = p[len("/api/v1"):]
    p = re.sub(r"\{[^}]+\}", "{param}", p)
    if p.endswith("/") and len(p) > 1:
        p = p[:-1]
    return p


def method_of_call(call: ast.Call) -> str | None:
    """Identify the HTTP method from a ``self._http.<method>(...)`` call."""
    func = call.func
    if isinstance(func, ast.Attribute):
        name = func.attr
        if isinstance(func.value, ast.Attribute) and func.value.attr == "_http":
            if name in (
                "get", "post", "put", "patch", "delete",
                "stream_sse", "upload_file", "request",
            ):
                return name
    return None


def extract_string(node: ast.AST) -> str | None:
    """Reconstruct a path string from a literal or JoinedStr (f-string)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        out = ""
        for v in node.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                out += v.value
            elif isinstance(v, ast.FormattedValue):
                out += "{param}"
            else:
                out += "{?}"
        return out
    return None


def extract_string_arg(call: ast.Call) -> str | None:
    if not call.args:
        return None
    return extract_string(call.args[0])


def _local_string_bindings(fn: ast.AST) -> dict[str, str]:
    """Extract local ``name = <string-ish>`` bindings from a function body."""
    out: dict[str, str] = {}
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            tgt = node.targets[0]
            if isinstance(tgt, ast.Name):
                s = extract_string(node.value)
                if s:
                    out[tgt.id] = s
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            if isinstance(node.target, ast.Name):
                s = extract_string(node.value)
                if s:
                    out[node.target.id] = s
    return out


def resolve_string(node: ast.AST, locals_: dict[str, str]) -> str | None:
    s = extract_string(node)
    if s is not None:
        return s
    if isinstance(node, ast.Name) and node.id in locals_:
        return locals_[node.id]
    return None


def resolve_strings(
    node: ast.AST,
    locals_: dict[str, str],
    class_bindings: dict[str, list[str]],
) -> list[str]:
    """Like :func:`resolve_string` but returns all possible values for a Name."""
    s = extract_string(node)
    if s is not None:
        return [s]
    if isinstance(node, ast.Name):
        if node.id in locals_:
            return [locals_[node.id]]
        if node.id in class_bindings:
            return list(class_bindings[node.id])
    return []


def _class_wide_string_bindings(cls: ast.ClassDef) -> dict[str, list[str]]:
    """Collect every ``name = <string-ish>`` across all methods in the class.

    This is what lets us track a ``path`` local that gets built in
    ``agents.chat(...)`` and then handed to ``_stream_chat(path, body)``.
    """
    out: dict[str, list[str]] = defaultdict(list)
    for fn in cls.body:
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                tgt = node.targets[0]
                if isinstance(tgt, ast.Name):
                    s = extract_string(node.value)
                    if s:
                        out[tgt.id].append(s)
    return out


def scan_resources() -> list[dict]:
    records: list[dict] = []
    # Scan hand-written resources plus generated resources. Hand-written files
    # override or add to the generated ones via inheritance — an endpoint is
    # "covered" if either file binds it.
    resource_files = list(RESOURCES_DIR.glob("*.py"))
    if GENERATED_RESOURCES_DIR.exists():
        resource_files.extend(GENERATED_RESOURCES_DIR.glob("*.py"))
    for py in sorted(resource_files):
        if py.name == "__init__.py":
            continue
        tree = ast.parse(py.read_text())
        for cls in ast.walk(tree):
            if not isinstance(cls, ast.ClassDef):
                continue
            class_bindings = _class_wide_string_bindings(cls)
            for fn in cls.body:
                if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                locals_ = _local_string_bindings(fn)
                param_names = {a.arg for a in fn.args.args}
                for pname in param_names:
                    if pname not in locals_ and class_bindings.get(pname):
                        locals_[pname] = class_bindings[pname][0]
                for node in ast.walk(fn):
                    if not isinstance(node, ast.Call):
                        continue
                    m = method_of_call(node)
                    if not m:
                        continue
                    if m == "request":
                        if len(node.args) >= 2:
                            http_method = resolve_string(node.args[0], locals_) or "REQ"
                            for path in resolve_strings(node.args[1], locals_, class_bindings):
                                records.append({
                                    "file": py.name,
                                    "class": cls.name,
                                    "method": fn.name,
                                    "http_method": http_method.upper(),
                                    "path": path,
                                })
                    elif m in ("get", "post", "put", "patch", "delete", "upload_file"):
                        paths = (
                            resolve_strings(node.args[0], locals_, class_bindings)
                            if node.args else []
                        )
                        http_method = m.upper() if m != "upload_file" else "POST"
                        for path in paths:
                            records.append({
                                "file": py.name,
                                "class": cls.name,
                                "method": fn.name,
                                "http_method": http_method,
                                "path": path,
                            })
                    elif m == "stream_sse":
                        if len(node.args) >= 2:
                            http_method = resolve_string(node.args[0], locals_) or "POST"
                            for path in resolve_strings(node.args[1], locals_, class_bindings):
                                records.append({
                                    "file": py.name,
                                    "class": cls.name,
                                    "method": fn.name,
                                    "http_method": http_method.upper(),
                                    "path": path,
                                    "stream": True,
                                })

    # Top-level client methods (e.g., Sonzai.list_models).
    tree = ast.parse(CLIENT_PATH.read_text())
    for cls in ast.walk(tree):
        if not isinstance(cls, ast.ClassDef):
            continue
        for fn in cls.body:
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for node in ast.walk(fn):
                if not isinstance(node, ast.Call):
                    continue
                m = method_of_call(node)
                if m and m in ("get", "post", "put", "patch", "delete"):
                    path = extract_string_arg(node)
                    if path:
                        records.append({
                            "file": "_client.py",
                            "class": cls.name,
                            "method": fn.name,
                            "http_method": m.upper(),
                            "path": path,
                        })
    return records


def main() -> int:
    spec_ops = [(m, normalize_path(p)) for m, p in load_spec_paths()]
    records = scan_resources()

    sdk_map: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in records:
        key = (r["http_method"], normalize_path(r["path"]))
        sdk_map[key].append(r)

    missing: list[tuple[str, str]] = []
    covered: list[tuple[str, str, list[dict]]] = []
    for m, p in spec_ops:
        key = (m, p)
        if key in sdk_map:
            covered.append((m, p, sdk_map[key]))
        else:
            missing.append((m, p))

    spec_keys = set(spec_ops)
    extras: list[tuple[str, str, list[dict]]] = []
    for k, v in sorted(sdk_map.items()):
        if k not in spec_keys:
            extras.append((k[0], k[1], v))

    print(f"Spec operations: {len(spec_ops)}")
    print(f"SDK-bound operations (covered): {len(covered)}")
    print(f"Missing (spec but not SDK): {len(missing)}")
    print(f"Extras (SDK but not spec): {len(extras)}")

    out = ["# SDK Parity Audit", ""]
    out.append(
        "Generated by `scripts/parity_audit.py` — re-run with `just regenerate-sdk` "
        "or `uv run --extra dev python scripts/parity_audit.py`."
    )
    out.append("")
    out.append(f"- Spec operations: **{len(spec_ops)}**")
    out.append(f"- SDK-bound (covered): **{len(covered)}**")
    out.append(f"- Missing: **{len(missing)}**")
    out.append(f"- Extras (in SDK not spec): **{len(extras)}**")
    out.append("")
    out.append("## Missing (declared in OpenAPI, not bound in either hand-written or generated SDK)")
    out.append("")
    if missing:
        out.append("| Method | Path |")
        out.append("|---|---|")
        for m, p in missing:
            out.append(f"| `{m}` | `{p}` |")
    else:
        out.append("_None — full parity._")
    out.append("")

    out.append("## Covered (spec path → SDK binding)")
    out.append("")
    out.append("| Method | Path | Binding |")
    out.append("|---|---|---|")
    for m, p, binds in covered:
        bind_str = "; ".join(f"{b['class']}.{b['method']}" for b in binds)
        out.append(f"| `{m}` | `{p}` | {bind_str} |")
    out.append("")

    if extras:
        out.append("## Extras (SDK binding with no matching spec path)")
        out.append("")
        out.append("| Method | Path | Binding |")
        out.append("|---|---|---|")
        for m, p, binds in extras:
            bind_str = "; ".join(f"{b['class']}.{b['method']}" for b in binds)
            out.append(f"| `{m}` | `{p}` | {bind_str} |")
        out.append("")

    mdpath = SDK_ROOT / "SDK_PARITY_AUDIT.md"
    mdpath.write_text("\n".join(out) + "\n")
    print(f"wrote {mdpath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
