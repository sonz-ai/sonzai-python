"""Jinja template rendering for resource modules."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import jinja2

from ._parse import EXTERNAL_CLASS_IMPORTS, Operation

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def emit_module(tag: str, operations: list[Operation]) -> str:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )

    for op in operations:
        if op.is_paginated:
            op.method_template = "method_list_sync.j2"
            op.async_method_template = "method_list_async.j2"
        else:
            op.method_template = "method_sync.j2"
            op.async_method_template = "method_async.j2"

    # Separate classes into those from _generated.models vs external modules.
    referenced: set[str] = set()
    # external_imports: module_path → sorted list of class names
    external_imports: dict[str, list[str]] = defaultdict(list)

    for op in operations:
        for cls in (op.input_body_class, op.response_class, op.pagination_item_type):
            if not cls:
                continue
            if cls in EXTERNAL_CLASS_IMPORTS:
                mod = EXTERNAL_CLASS_IMPORTS[cls]
                if cls not in external_imports[mod]:
                    external_imports[mod].append(cls)
            else:
                referenced.add(cls)

    class_base = _to_pascal_case(tag)

    tmpl = env.get_template("resource.py.j2")
    return tmpl.render(
        tag_human=class_base,
        class_base=class_base,
        operations=operations,
        referenced_classes=referenced,
        external_imports={mod: sorted(names) for mod, names in external_imports.items()},
    )


def _to_pascal_case(snake: str) -> str:
    return "".join(part.capitalize() for part in snake.split("_"))
