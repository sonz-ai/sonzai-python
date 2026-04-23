"""Tests for the resource code generator."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.codegen._emit import emit_module
from scripts.codegen._parse import Operation, Parameter, parse_spec

FIXTURES = Path(__file__).resolve().parent.parent / "scripts/codegen/fixtures"


class TestSpecParse:
    def test_groups_operations_by_tag(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        assert set(by_tag.keys()) == {"memory"}
        assert len(by_tag["memory"]) == 2

    def test_list_operation_detected_as_paginated(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        list_op = next(o for o in by_tag["memory"] if o.operation_id == "listAllFacts")
        assert list_op.is_paginated is True
        assert list_op.pagination_mode == "offset"
        assert list_op.pagination_item_key == "facts"
        assert list_op.pagination_item_type == "StoredFact"
        assert list_op.pagination_total_key == "total"

    def test_post_operation_has_input_body(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        add_op = next(o for o in by_tag["memory"] if o.operation_id == "addFact")
        assert add_op.is_paginated is False
        assert add_op.input_body_class == "AddFactInputBody"
        assert add_op.response_class == "StoredFact"

    def test_path_params_extracted(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        add_op = next(o for o in by_tag["memory"] if o.operation_id == "addFact")
        assert [p.name for p in add_op.path_params] == ["agent_id"]
        assert add_op.path_params[0].required is True

    def test_query_params_have_defaults(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        list_op = next(o for o in by_tag["memory"] if o.operation_id == "listAllFacts")
        limit = next(p for p in list_op.query_params if p.name == "limit")
        assert limit.default == 50


class TestEmit:
    def test_memory_tag_matches_golden(self) -> None:
        spec = json.loads((FIXTURES / "mini_spec.json").read_text())
        by_tag = parse_spec(spec)
        output = emit_module("memory", by_tag["memory"])
        expected = (FIXTURES / "expected_memory.py").read_text()
        assert output.rstrip() == expected.rstrip()
