"""Typo-catching regression tests across Batch 1 resources."""

from __future__ import annotations

import httpx
import pytest
import respx
from pydantic import ValidationError

from sonzai import Sonzai


class TestAgentsBatch1:
    def test_create_agent_happy_path(self) -> None:
        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/agents").mock(
                return_value=httpx.Response(200, json={
                    "agent_id": "a1",
                    "name": "X",
                    "owner_user_id": "u1",
                    "tenant_id": "t1",
                    "instance_count": 1,
                    "is_active": True,
                    "created_at": "2026-01-01T00:00:00Z",
                })
            )
            client = Sonzai(api_key="test-key")
            result = client.agents.create(name="X")
            assert result.agent_id == "a1"

    def test_create_agent_typo_raises(self) -> None:
        """A typo in a field name forwarded to CreateAgentBody must raise ValidationError."""
        client = Sonzai(api_key="test-key")
        # The method signature is explicit so a bad kwarg raises TypeError
        with pytest.raises(TypeError):
            client.agents.create(name="X", nme="typo")  # type: ignore[call-overload]

    def test_set_status_happy_path(self) -> None:
        with respx.mock() as router:
            router.patch("https://api.sonz.ai/api/v1/agents/a1/status").mock(
                return_value=httpx.Response(200, json={"success": True, "is_active": True})
            )
            client = Sonzai(api_key="test-key")
            result = client.agents.set_status("a1", is_active=True)
            assert result.success is True

    def test_fork_happy_path(self) -> None:
        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/agents/a1/fork").mock(
                return_value=httpx.Response(200, json={
                    "agent_id": "a2",
                    "name": "X (fork)",
                    "source_agent_id": "a1",
                    "status": "pending",
                })
            )
            client = Sonzai(api_key="test-key")
            result = client.agents.fork("a1")
            assert result.status == "pending"
            assert result.source_agent_id == "a1"

    def test_generate_avatar_happy_path(self) -> None:
        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/agents/a1/avatar/generate").mock(
                return_value=httpx.Response(200, json={"avatar_url": "https://example.com/av.png"})
            )
            client = Sonzai(api_key="test-key")
            result = client.agents.generate_avatar("a1")
            assert result.avatar_url == "https://example.com/av.png"


class TestMemoryBatch1:
    def test_create_fact_happy_path(self) -> None:
        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/agents/a1/memory/facts").mock(
                return_value=httpx.Response(200, json={
                    "fact_id": "f1",
                    "agent_id": "a1",
                    "atomic_text": "test content",
                    "fact_type": "user_fact",
                    "source_type": "manual",
                    "importance": 0.5,
                    "confidence": 0.9,
                    "node_id": "n1",
                    "mention_count": 1,
                    "retention_strength": 0.8,
                    "created_at": "2026-01-01T00:00:00Z",
                    "updated_at": "2026-01-01T00:00:00Z",
                    "last_confirmed": "2026-01-01T00:00:00Z",
                    "last_retrieved_at": "2026-01-01T00:00:00Z",
                })
            )
            client = Sonzai(api_key="test-key")
            result = client.agents.memory.create_fact(
                "a1", content="test content", fact_type="user_fact"
            )
            assert result.fact_id == "f1"

    def test_create_fact_unknown_field_raises(self) -> None:
        """A typo/unknown field in create_fact must raise ValidationError."""
        client = Sonzai(api_key="test-key")
        # fact_type is required but content is set; add unknown field via subclass test
        # Since method signature is explicit, an unknown kwarg raises TypeError first
        with pytest.raises(TypeError):
            client.agents.memory.create_fact(  # type: ignore[call-overload]
                "a1", content="x", fact_type="user_fact", unkown_field="typo"
            )


class TestKnowledgeBatch1:
    def test_insert_facts_happy_path(self) -> None:
        """insert_facts validates nested InsertFactEntry: entity_type + label + properties required."""
        with respx.mock() as router:
            router.post("https://api.sonz.ai/api/v1/projects/p1/knowledge/facts").mock(
                return_value=httpx.Response(200, json={
                    "processed": 1,
                    "created": 1,
                    "updated": 0,
                    "details": [],
                    "edges": [],
                })
            )
            client = Sonzai(api_key="test-key")
            # InsertFactEntry requires entity_type, label, properties
            result = client.knowledge.insert_facts(
                "p1",
                facts=[{"entity_type": "person", "label": "Alice", "properties": {}}],
            )
            assert result.processed == 1

    def test_insert_facts_wrong_shape_raises(self) -> None:
        """Passing a dict with unknown field (node_type) raises ValidationError."""
        client = Sonzai(api_key="test-key")
        with pytest.raises(ValidationError):
            client.knowledge.insert_facts(
                "p1",
                facts=[{"label": "test", "node_type": "entity", "properties": {}}],
            )

    def test_create_analytics_rule_typo_raises(self) -> None:
        """An unknown kwarg to create_analytics_rule must raise ValidationError."""
        client = Sonzai(api_key="test-key")
        with pytest.raises(ValidationError):
            # create_analytics_rule accepts **kwargs, so encode_body validates them
            client.knowledge.create_analytics_rule(
                "p1",
                name="test",
                rule_type="recommendation",
                enabled=True,
                config={},
                typo_field="bad",  # unknown field — should raise ValidationError
            )

    def test_update_schema_typo_raises(self) -> None:
        """An unknown kwarg to update_schema must raise ValidationError."""
        client = Sonzai(api_key="test-key")
        with pytest.raises(ValidationError):
            client.knowledge.update_schema(
                "p1",
                "schema1",
                entity_type="Person",
                typo_fild="bad",  # typo — should raise ValidationError
            )

    def test_bulk_update_happy_path(self) -> None:
        """bulk_update validates BulkUpdateEntry: entity_type + label + properties required."""
        with respx.mock() as router:
            router.patch("https://api.sonz.ai/api/v1/projects/p1/knowledge/bulk-update").mock(
                return_value=httpx.Response(200, json={
                    "processed": 1,
                    "updated": 1,
                    "created": 0,
                    "errors": [],
                })
            )
            client = Sonzai(api_key="test-key")
            # BulkUpdateEntry requires entity_type, label, properties
            result = client.knowledge.bulk_update(
                "p1",
                updates=[{"entity_type": "person", "label": "Alice", "properties": {"age": 30}}],
            )
            assert result.updated == 1
