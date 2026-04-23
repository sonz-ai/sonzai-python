"""Jinja template rendering for resource modules."""

from __future__ import annotations

from pathlib import Path

import jinja2

from ._parse import Operation

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

    referenced: set[str] = set()
    for op in operations:
        if op.input_body_class:
            referenced.add(op.input_body_class)
        if op.response_class:
            referenced.add(op.response_class)
        if op.pagination_item_type:
            referenced.add(op.pagination_item_type)

    class_base = _to_pascal_case(tag)

    tmpl = env.get_template("resource.py.j2")
    return tmpl.render(
        tag_human=class_base,
        class_base=class_base,
        operations=operations,
        referenced_classes=referenced,
    )


def _to_pascal_case(snake: str) -> str:
    return "".join(part.capitalize() for part in snake.split("_"))
