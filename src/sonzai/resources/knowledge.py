"""Knowledge base resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    CreateOrgNodeOptions,
    KBAnalyticsRule,
    KBAnalyticsRuleListResponse,
    KBBulkUpdateResponse,
    KBConversionsResponse,
    KBDocument,
    KBDocumentListResponse,
    KBEntitySchema,
    KBNode,
    KBNodeDetailResponse,
    KBNodeHistoryResponse,
    KBNodeListResponse,
    KBNodeWithScope,
    KBRecommendationsResponse,
    KBSchemaListResponse,
    KBSearchResponse,
    KBStats,
    KBTrendRankingsResponse,
    KBTrendsResponse,
    InsertFactsResponse,
)


class Knowledge:
    """Sync knowledge base operations (project-scoped)."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    # -- Documents --

    def list_documents(
        self, project_id: str, *, limit: int | None = None
    ) -> KBDocumentListResponse:
        """List documents for a project."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = self._http.get(f"/api/v1/projects/{project_id}/knowledge/documents", params=params)
        return KBDocumentListResponse.model_validate(data)

    def get_document(self, project_id: str, doc_id: str) -> KBDocument:
        """Get a single document."""
        data = self._http.get(f"/api/v1/projects/{project_id}/knowledge/documents/{doc_id}")
        return KBDocument.model_validate(data)

    def delete_document(self, project_id: str, doc_id: str) -> None:
        """Delete a document."""
        self._http.delete(f"/api/v1/projects/{project_id}/knowledge/documents/{doc_id}")

    def upload_document(
        self,
        project_id: str,
        *,
        file_name: str,
        file_data: bytes,
        content_type: str = "application/octet-stream",
    ) -> KBDocument:
        return KBDocument.model_validate(
            self._http.upload_file(
                f"/api/v1/projects/{project_id}/knowledge/documents",
                file_name=file_name,
                file_data=file_data,
                content_type=content_type,
            )
        )

    # -- Facts / Graph --

    def insert_facts(
        self,
        project_id: str,
        *,
        facts: list[dict[str, Any]],
        relationships: list[dict[str, Any]] | None = None,
        source: str | None = None,
    ) -> InsertFactsResponse:
        """Insert entities and relationships into the knowledge graph."""
        body: dict[str, Any] = {"facts": facts}
        if relationships is not None:
            body["relationships"] = relationships
        if source is not None:
            body["source"] = source
        data = self._http.post(f"/api/v1/projects/{project_id}/knowledge/facts", json_data=body)
        return InsertFactsResponse.model_validate(data)

    def list_nodes(
        self,
        project_id: str,
        *,
        node_type: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        properties: dict[str, str] | None = None,
    ) -> KBNodeListResponse:
        """List knowledge graph nodes with filtering, pagination, and sorting."""
        params: dict[str, Any] = {}
        if node_type is not None:
            params["type"] = node_type
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_order is not None:
            params["sort_order"] = sort_order
        if properties is not None:
            for k, v in properties.items():
                params[f"properties.{k}"] = v
        data = self._http.get(f"/api/v1/projects/{project_id}/knowledge/nodes", params=params)
        return KBNodeListResponse.model_validate(data)

    def get_node(
        self, project_id: str, node_id: str, *, include_history: bool = False
    ) -> KBNodeDetailResponse:
        """Get a node with connected edges."""
        params: dict[str, Any] = {}
        if include_history:
            params["history"] = "true"
        data = self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/nodes/{node_id}",
            params=params,
        )
        return KBNodeDetailResponse.model_validate(data)

    def delete_node(self, project_id: str, node_id: str) -> None:
        """Soft-delete a node."""
        self._http.delete(f"/api/v1/projects/{project_id}/knowledge/nodes/{node_id}")

    def get_node_history(
        self, project_id: str, node_id: str, *, limit: int | None = None
    ) -> KBNodeHistoryResponse:
        """Get version history for a node."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/nodes/{node_id}/history",
            params=params,
        )
        return KBNodeHistoryResponse.model_validate(data)

    # -- Search --

    def search(
        self,
        project_id: str,
        *,
        query: str,
        limit: int | None = None,
        include_history: bool = False,
        entity_types: str | None = None,
        filters: str | None = None,
        hops: int | None = None,
    ) -> KBSearchResponse:
        """BM25 search with graph traversal."""
        params: dict[str, Any] = {"q": query}
        if limit is not None:
            params["limit"] = limit
        if include_history:
            params["history"] = "true"
        if entity_types is not None:
            params["type"] = entity_types
        if filters is not None:
            params["filters"] = filters
        if hops is not None:
            params["hops"] = hops
        data = self._http.get(f"/api/v1/projects/{project_id}/knowledge/search", params=params)
        return KBSearchResponse.model_validate(data)

    # -- Schemas --

    def create_schema(
        self,
        project_id: str,
        *,
        entity_type: str,
        fields: list[dict[str, Any]],
        display_name: str | None = None,
        **kwargs: Any,
    ) -> KBEntitySchema:
        """Create an entity type schema."""
        body: dict[str, Any] = {"entity_type": entity_type, "fields": fields}
        if display_name is not None:
            body["display_name"] = display_name
        body.update(kwargs)
        data = self._http.post(f"/api/v1/projects/{project_id}/knowledge/schemas", json_data=body)
        return KBEntitySchema.model_validate(data)

    def list_schemas(self, project_id: str) -> KBSchemaListResponse:
        """List entity schemas."""
        data = self._http.get(f"/api/v1/projects/{project_id}/knowledge/schemas")
        return KBSchemaListResponse.model_validate(data)

    def update_schema(self, project_id: str, schema_id: str, **kwargs: Any) -> KBEntitySchema:
        """Update an entity schema."""
        data = self._http.put(
            f"/api/v1/projects/{project_id}/knowledge/schemas/{schema_id}",
            json_data=kwargs,
        )
        return KBEntitySchema.model_validate(data)

    def delete_schema(self, project_id: str, schema_id: str) -> None:
        """Delete an entity schema."""
        self._http.delete(f"/api/v1/projects/{project_id}/knowledge/schemas/{schema_id}")

    # -- Stats --

    def get_stats(self, project_id: str) -> KBStats:
        """Get knowledge base statistics."""
        data = self._http.get(f"/api/v1/projects/{project_id}/knowledge/stats")
        return KBStats.model_validate(data)

    # -- Analytics Rules --

    def create_analytics_rule(self, project_id: str, **kwargs: Any) -> KBAnalyticsRule:
        """Create an analytics rule."""
        data = self._http.post(
            f"/api/v1/projects/{project_id}/knowledge/analytics/rules",
            json_data=kwargs,
        )
        return KBAnalyticsRule.model_validate(data)

    def list_analytics_rules(self, project_id: str) -> KBAnalyticsRuleListResponse:
        """List analytics rules."""
        data = self._http.get(f"/api/v1/projects/{project_id}/knowledge/analytics/rules")
        return KBAnalyticsRuleListResponse.model_validate(data)

    def get_analytics_rule(self, project_id: str, rule_id: str) -> KBAnalyticsRule:
        """Get a single analytics rule."""
        data = self._http.get(f"/api/v1/projects/{project_id}/knowledge/analytics/rules/{rule_id}")
        return KBAnalyticsRule.model_validate(data)

    def update_analytics_rule(
        self, project_id: str, rule_id: str, **kwargs: Any
    ) -> KBAnalyticsRule:
        """Update an analytics rule."""
        data = self._http.put(
            f"/api/v1/projects/{project_id}/knowledge/analytics/rules/{rule_id}",
            json_data=kwargs,
        )
        return KBAnalyticsRule.model_validate(data)

    def delete_analytics_rule(self, project_id: str, rule_id: str) -> None:
        """Delete an analytics rule."""
        self._http.delete(f"/api/v1/projects/{project_id}/knowledge/analytics/rules/{rule_id}")

    def run_analytics_rule(self, project_id: str, rule_id: str) -> None:
        """Trigger a manual run of an analytics rule."""
        self._http.post(
            f"/api/v1/projects/{project_id}/knowledge/analytics/rules/{rule_id}/run",
            json_data={},
        )

    # -- Analytics Queries --

    def get_recommendations(
        self, project_id: str, *, rule_id: str, source_id: str, limit: int | None = None
    ) -> KBRecommendationsResponse:
        """Get recommendations for a source node."""
        params: dict[str, Any] = {"rule_id": rule_id, "source_id": source_id}
        if limit is not None:
            params["limit"] = limit
        data = self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/analytics/recommendations",
            params=params,
        )
        return KBRecommendationsResponse.model_validate(data)

    def get_trends(self, project_id: str, *, node_id: str) -> KBTrendsResponse:
        """Get trend aggregations for a node."""
        data = self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/analytics/trends",
            params={"node_id": node_id},
        )
        return KBTrendsResponse.model_validate(data)

    def get_trend_rankings(
        self,
        project_id: str,
        *,
        rule_id: str,
        ranking_type: str,
        window: str,
        limit: int | None = None,
    ) -> KBTrendRankingsResponse:
        """Get trend rankings."""
        params: dict[str, Any] = {
            "rule_id": rule_id,
            "type": ranking_type,
            "window": window,
        }
        if limit is not None:
            params["limit"] = limit
        data = self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/analytics/rankings",
            params=params,
        )
        return KBTrendRankingsResponse.model_validate(data)

    def get_conversions(
        self, project_id: str, *, rule_id: str, segment: str | None = None
    ) -> KBConversionsResponse:
        """Get conversion statistics."""
        params: dict[str, Any] = {"rule_id": rule_id}
        if segment is not None:
            params["segment"] = segment
        data = self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/analytics/conversions",
            params=params,
        )
        return KBConversionsResponse.model_validate(data)

    def record_feedback(
        self,
        project_id: str,
        *,
        source_node_id: str,
        target_node_id: str,
        rule_id: str,
        converted: bool,
        score_at_time: float,
    ) -> None:
        """Record recommendation feedback."""
        self._http.post(
            f"/api/v1/projects/{project_id}/knowledge/analytics/feedback",
            json_data={
                "source_node_id": source_node_id,
                "target_node_id": target_node_id,
                "rule_id": rule_id,
                "converted": converted,
                "score_at_time": score_at_time,
            },
        )

    # -- Bulk Update --

    def bulk_update(
        self,
        project_id: str,
        *,
        updates: list[dict[str, Any]],
        source: str | None = None,
        upsert: bool | None = None,
    ) -> KBBulkUpdateResponse:
        """Batch-update KB node properties. Sync for <=100 items; async for larger."""
        body: dict[str, Any] = {"updates": updates}
        if source is not None:
            body["source"] = source
        if upsert is not None:
            body["upsert"] = upsert
        return KBBulkUpdateResponse.model_validate(
            self._http.patch(
                f"/api/v1/projects/{project_id}/knowledge/bulk-update",
                json_data=body,
            )
        )

    # -- Organization-global scope (docs/ORGANIZATION_GLOBAL_KB.md) --

    def create_org_node(
        self,
        tenant_id: str,
        options: CreateOrgNodeOptions | dict[str, Any],
    ) -> KBNode:
        """Create a KB node directly in the organization-global scope.

        Every project under the tenant can read it via cascade / union /
        org_only scope modes. Idempotency is the caller's responsibility —
        look up by label first if duplicates matter.
        """
        if isinstance(options, CreateOrgNodeOptions):
            body = options.model_dump(exclude_defaults=True)
        else:
            body = dict(options)
        return KBNode.model_validate(
            self._http.post(
                f"/api/v1/tenants/{tenant_id}/knowledge/org-nodes",
                json_data=body,
            )
        )

    def promote_node_to_org(
        self,
        project_id: str,
        node_id: str,
        tenant_id: str,
    ) -> KBNodeWithScope:
        """Promote a project-scoped node into the organization-global scope.

        The project copy is preserved — promotion is additive. If an org
        node with the same (node_type, norm_label) already exists, the
        server returns it instead of writing a duplicate.
        """
        return KBNodeWithScope.model_validate(
            self._http.post(
                f"/api/v1/projects/{project_id}/knowledge/nodes/{node_id}/promote-to-org",
                json_data={"tenant_id": tenant_id},
            )
        )


class AsyncKnowledge:
    """Async knowledge base operations (project-scoped)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list_documents(
        self, project_id: str, *, limit: int | None = None
    ) -> KBDocumentListResponse:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/documents", params=params
        )
        return KBDocumentListResponse.model_validate(data)

    async def get_document(self, project_id: str, doc_id: str) -> KBDocument:
        data = await self._http.get(f"/api/v1/projects/{project_id}/knowledge/documents/{doc_id}")
        return KBDocument.model_validate(data)

    async def delete_document(self, project_id: str, doc_id: str) -> None:
        await self._http.delete(f"/api/v1/projects/{project_id}/knowledge/documents/{doc_id}")

    async def upload_document(
        self,
        project_id: str,
        *,
        file_name: str,
        file_data: bytes,
        content_type: str = "application/octet-stream",
    ) -> KBDocument:
        data = await self._http.upload_file(
            f"/api/v1/projects/{project_id}/knowledge/documents",
            file_name=file_name,
            file_data=file_data,
            content_type=content_type,
        )
        return KBDocument.model_validate(data)

    async def insert_facts(
        self,
        project_id: str,
        *,
        facts: list[dict[str, Any]],
        relationships: list[dict[str, Any]] | None = None,
        source: str | None = None,
    ) -> InsertFactsResponse:
        body: dict[str, Any] = {"facts": facts}
        if relationships is not None:
            body["relationships"] = relationships
        if source is not None:
            body["source"] = source
        data = await self._http.post(
            f"/api/v1/projects/{project_id}/knowledge/facts", json_data=body
        )
        return InsertFactsResponse.model_validate(data)

    async def list_nodes(
        self,
        project_id: str,
        *,
        node_type: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        properties: dict[str, str] | None = None,
    ) -> KBNodeListResponse:
        params: dict[str, Any] = {}
        if node_type is not None:
            params["type"] = node_type
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_order is not None:
            params["sort_order"] = sort_order
        if properties is not None:
            for k, v in properties.items():
                params[f"properties.{k}"] = v
        data = await self._http.get(f"/api/v1/projects/{project_id}/knowledge/nodes", params=params)
        return KBNodeListResponse.model_validate(data)

    async def get_node(
        self, project_id: str, node_id: str, *, include_history: bool = False
    ) -> KBNodeDetailResponse:
        params: dict[str, Any] = {}
        if include_history:
            params["history"] = "true"
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/nodes/{node_id}", params=params
        )
        return KBNodeDetailResponse.model_validate(data)

    async def delete_node(self, project_id: str, node_id: str) -> None:
        await self._http.delete(f"/api/v1/projects/{project_id}/knowledge/nodes/{node_id}")

    async def get_node_history(
        self, project_id: str, node_id: str, *, limit: int | None = None
    ) -> KBNodeHistoryResponse:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/nodes/{node_id}/history",
            params=params,
        )
        return KBNodeHistoryResponse.model_validate(data)

    async def search(
        self,
        project_id: str,
        *,
        query: str,
        limit: int | None = None,
        include_history: bool = False,
        entity_types: str | None = None,
        filters: str | None = None,
        hops: int | None = None,
    ) -> KBSearchResponse:
        params: dict[str, Any] = {"q": query}
        if limit is not None:
            params["limit"] = limit
        if include_history:
            params["history"] = "true"
        if entity_types is not None:
            params["type"] = entity_types
        if filters is not None:
            params["filters"] = filters
        if hops is not None:
            params["hops"] = hops
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/search", params=params
        )
        return KBSearchResponse.model_validate(data)

    # -- Schemas --

    async def create_schema(
        self,
        project_id: str,
        *,
        entity_type: str,
        fields: list[dict[str, Any]],
        display_name: str | None = None,
        **kwargs: Any,
    ) -> KBEntitySchema:
        body: dict[str, Any] = {"entity_type": entity_type, "fields": fields}
        if display_name is not None:
            body["display_name"] = display_name
        body.update(kwargs)
        data = await self._http.post(
            f"/api/v1/projects/{project_id}/knowledge/schemas", json_data=body
        )
        return KBEntitySchema.model_validate(data)

    async def list_schemas(self, project_id: str) -> KBSchemaListResponse:
        data = await self._http.get(f"/api/v1/projects/{project_id}/knowledge/schemas")
        return KBSchemaListResponse.model_validate(data)

    async def update_schema(self, project_id: str, schema_id: str, **kwargs: Any) -> KBEntitySchema:
        data = await self._http.put(
            f"/api/v1/projects/{project_id}/knowledge/schemas/{schema_id}",
            json_data=kwargs,
        )
        return KBEntitySchema.model_validate(data)

    async def delete_schema(self, project_id: str, schema_id: str) -> None:
        await self._http.delete(f"/api/v1/projects/{project_id}/knowledge/schemas/{schema_id}")

    async def get_stats(self, project_id: str) -> KBStats:
        data = await self._http.get(f"/api/v1/projects/{project_id}/knowledge/stats")
        return KBStats.model_validate(data)

    # -- Analytics Rules --

    async def create_analytics_rule(self, project_id: str, **kwargs: Any) -> KBAnalyticsRule:
        data = await self._http.post(
            f"/api/v1/projects/{project_id}/knowledge/analytics/rules",
            json_data=kwargs,
        )
        return KBAnalyticsRule.model_validate(data)

    async def list_analytics_rules(self, project_id: str) -> KBAnalyticsRuleListResponse:
        data = await self._http.get(f"/api/v1/projects/{project_id}/knowledge/analytics/rules")
        return KBAnalyticsRuleListResponse.model_validate(data)

    async def get_analytics_rule(self, project_id: str, rule_id: str) -> KBAnalyticsRule:
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/analytics/rules/{rule_id}"
        )
        return KBAnalyticsRule.model_validate(data)

    async def update_analytics_rule(
        self, project_id: str, rule_id: str, **kwargs: Any
    ) -> KBAnalyticsRule:
        data = await self._http.put(
            f"/api/v1/projects/{project_id}/knowledge/analytics/rules/{rule_id}",
            json_data=kwargs,
        )
        return KBAnalyticsRule.model_validate(data)

    async def delete_analytics_rule(self, project_id: str, rule_id: str) -> None:
        await self._http.delete(
            f"/api/v1/projects/{project_id}/knowledge/analytics/rules/{rule_id}"
        )

    async def run_analytics_rule(self, project_id: str, rule_id: str) -> None:
        await self._http.post(
            f"/api/v1/projects/{project_id}/knowledge/analytics/rules/{rule_id}/run",
            json_data={},
        )

    # -- Analytics Queries --

    async def get_recommendations(
        self, project_id: str, *, rule_id: str, source_id: str, limit: int | None = None
    ) -> KBRecommendationsResponse:
        params: dict[str, Any] = {"rule_id": rule_id, "source_id": source_id}
        if limit is not None:
            params["limit"] = limit
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/analytics/recommendations",
            params=params,
        )
        return KBRecommendationsResponse.model_validate(data)

    async def get_trends(self, project_id: str, *, node_id: str) -> KBTrendsResponse:
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/analytics/trends",
            params={"node_id": node_id},
        )
        return KBTrendsResponse.model_validate(data)

    async def get_trend_rankings(
        self,
        project_id: str,
        *,
        rule_id: str,
        ranking_type: str,
        window: str,
        limit: int | None = None,
    ) -> KBTrendRankingsResponse:
        params: dict[str, Any] = {
            "rule_id": rule_id,
            "type": ranking_type,
            "window": window,
        }
        if limit is not None:
            params["limit"] = limit
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/analytics/rankings",
            params=params,
        )
        return KBTrendRankingsResponse.model_validate(data)

    async def get_conversions(
        self, project_id: str, *, rule_id: str, segment: str | None = None
    ) -> KBConversionsResponse:
        params: dict[str, Any] = {"rule_id": rule_id}
        if segment is not None:
            params["segment"] = segment
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/knowledge/analytics/conversions",
            params=params,
        )
        return KBConversionsResponse.model_validate(data)

    async def record_feedback(
        self,
        project_id: str,
        *,
        source_node_id: str,
        target_node_id: str,
        rule_id: str,
        converted: bool,
        score_at_time: float,
    ) -> None:
        await self._http.post(
            f"/api/v1/projects/{project_id}/knowledge/analytics/feedback",
            json_data={
                "source_node_id": source_node_id,
                "target_node_id": target_node_id,
                "rule_id": rule_id,
                "converted": converted,
                "score_at_time": score_at_time,
            },
        )

    # -- Bulk Update --

    async def bulk_update(
        self,
        project_id: str,
        *,
        updates: list[dict[str, Any]],
        source: str | None = None,
        upsert: bool | None = None,
    ) -> KBBulkUpdateResponse:
        """Batch-update KB node properties. Sync for <=100 items; async for larger."""
        body: dict[str, Any] = {"updates": updates}
        if source is not None:
            body["source"] = source
        if upsert is not None:
            body["upsert"] = upsert
        return KBBulkUpdateResponse.model_validate(
            await self._http.patch(
                f"/api/v1/projects/{project_id}/knowledge/bulk-update",
                json_data=body,
            )
        )

    # -- Organization-global scope (docs/ORGANIZATION_GLOBAL_KB.md) --

    async def create_org_node(
        self,
        tenant_id: str,
        options: CreateOrgNodeOptions | dict[str, Any],
    ) -> KBNode:
        """Create a KB node directly in the organization-global scope."""
        if isinstance(options, CreateOrgNodeOptions):
            body = options.model_dump(exclude_defaults=True)
        else:
            body = dict(options)
        return KBNode.model_validate(
            await self._http.post(
                f"/api/v1/tenants/{tenant_id}/knowledge/org-nodes",
                json_data=body,
            )
        )

    async def promote_node_to_org(
        self,
        project_id: str,
        node_id: str,
        tenant_id: str,
    ) -> KBNodeWithScope:
        """Promote a project-scoped node into the organization-global scope."""
        return KBNodeWithScope.model_validate(
            await self._http.post(
                f"/api/v1/projects/{project_id}/knowledge/nodes/{node_id}/promote-to-org",
                json_data={"tenant_id": tenant_id},
            )
        )
