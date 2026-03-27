from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .._http import HTTPClient, AsyncHTTPClient
from ..types import (
    InventoryUpdateResponse,
    InventoryQueryResponse,
    InventoryBatchImportResponse,
    InventoryDirectUpdateResponse,
    ListAllFactsResponse,
)


class Inventory:
    """Inventory/asset tracking operations scoped to an agent + user."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def update(
        self,
        agent_id: str,
        user_id: str,
        *,
        action: str,
        item_type: str,
        description: str | None = None,
        kb_node_id: str | None = None,
        properties: dict[str, Any] | None = None,
        project_id: str | None = None,
        instance_id: str | None = None,
    ) -> InventoryUpdateResponse:
        """Add, update, or remove an inventory item."""
        body: dict[str, Any] = {"action": action, "item_type": item_type}
        if description is not None:
            body["description"] = description
        if kb_node_id is not None:
            body["kb_node_id"] = kb_node_id
        if properties is not None:
            body["properties"] = properties
        if project_id is not None:
            body["project_id"] = project_id
        params: dict[str, str] | None = None
        if instance_id is not None:
            params = {"instance_id": instance_id}
        return InventoryUpdateResponse.model_validate(
            self._http.post(
                f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/inventory",
                json_data=body,
                params=params,
            )
        )

    def query(
        self,
        agent_id: str,
        user_id: str,
        *,
        mode: str | None = None,
        item_type: str | None = None,
        query: str | None = None,
        project_id: str | None = None,
        aggregations: str | None = None,
        group_by: str | None = None,
        limit: int | None = None,
        instance_id: str | None = None,
    ) -> InventoryQueryResponse:
        """Query a user's inventory with optional valuations and aggregation."""
        params: dict[str, str] = {}
        if mode is not None:
            params["mode"] = mode
        if item_type is not None:
            params["item_type"] = item_type
        if query is not None:
            params["query"] = query
        if project_id is not None:
            params["project_id"] = project_id
        if aggregations is not None:
            params["aggregations"] = aggregations
        if group_by is not None:
            params["group_by"] = group_by
        if limit is not None:
            params["limit"] = str(limit)
        if instance_id is not None:
            params["instance_id"] = instance_id
        return InventoryQueryResponse.model_validate(
            self._http.get(
                f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/inventory",
                params=params,
            )
        )

    def batch_import(
        self,
        agent_id: str,
        user_id: str,
        *,
        items: list[dict[str, Any]],
        project_id: str | None = None,
        instance_id: str | None = None,
    ) -> InventoryBatchImportResponse:
        """Batch-import inventory items (up to 1000)."""
        body: dict[str, Any] = {"items": items}
        if project_id is not None:
            body["project_id"] = project_id
        params: dict[str, str] | None = None
        if instance_id is not None:
            params = {"instance_id": instance_id}
        return InventoryBatchImportResponse.model_validate(
            self._http.post(
                f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/inventory/batch",
                json_data=body,
                params=params,
            )
        )

    def direct_update(
        self,
        agent_id: str,
        user_id: str,
        fact_id: str,
        *,
        properties: dict[str, Any],
        instance_id: str | None = None,
    ) -> InventoryDirectUpdateResponse:
        """Directly update an inventory fact's properties by fact ID."""
        path = f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/inventory/{quote(fact_id, safe='')}"
        if instance_id is not None:
            path += f"?instance_id={quote(instance_id, safe='')}"
        return InventoryDirectUpdateResponse.model_validate(
            self._http.put(path, json_data={"properties": properties})
        )

    def direct_delete(
        self,
        agent_id: str,
        user_id: str,
        fact_id: str,
        *,
        instance_id: str | None = None,
    ) -> InventoryDirectUpdateResponse:
        """Directly delete an inventory item by fact ID."""
        params: dict[str, str] | None = None
        if instance_id is not None:
            params = {"instance_id": instance_id}
        return InventoryDirectUpdateResponse.model_validate(
            self._http.delete(
                f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/inventory/{quote(fact_id, safe='')}",
                params=params,
            )
        )

    def list_all_facts(
        self,
        agent_id: str,
        user_id: str,
        *,
        has_metadata: bool = False,
        item_type: str | None = None,
        limit: int | None = None,
        instance_id: str | None = None,
    ) -> ListAllFactsResponse:
        """List all active facts for an agent+user pair."""
        params: dict[str, str] = {}
        if has_metadata:
            params["has_metadata"] = "true"
        if item_type is not None:
            params["metadata.item_type"] = item_type
        if limit is not None:
            params["limit"] = str(limit)
        if instance_id is not None:
            params["instance_id"] = instance_id
        return ListAllFactsResponse.model_validate(
            self._http.get(
                f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/facts",
                params=params,
            )
        )


class AsyncInventory:
    """Async inventory/asset tracking operations scoped to an agent + user."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def update(
        self,
        agent_id: str,
        user_id: str,
        *,
        action: str,
        item_type: str,
        description: str | None = None,
        kb_node_id: str | None = None,
        properties: dict[str, Any] | None = None,
        project_id: str | None = None,
        instance_id: str | None = None,
    ) -> InventoryUpdateResponse:
        """Add, update, or remove an inventory item."""
        body: dict[str, Any] = {"action": action, "item_type": item_type}
        if description is not None:
            body["description"] = description
        if kb_node_id is not None:
            body["kb_node_id"] = kb_node_id
        if properties is not None:
            body["properties"] = properties
        if project_id is not None:
            body["project_id"] = project_id
        params: dict[str, str] | None = None
        if instance_id is not None:
            params = {"instance_id": instance_id}
        return InventoryUpdateResponse.model_validate(
            await self._http.post(
                f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/inventory",
                json_data=body,
                params=params,
            )
        )

    async def query(
        self,
        agent_id: str,
        user_id: str,
        *,
        mode: str | None = None,
        item_type: str | None = None,
        query: str | None = None,
        project_id: str | None = None,
        aggregations: str | None = None,
        group_by: str | None = None,
        limit: int | None = None,
        instance_id: str | None = None,
    ) -> InventoryQueryResponse:
        """Query a user's inventory with optional valuations and aggregation."""
        params: dict[str, str] = {}
        if mode is not None:
            params["mode"] = mode
        if item_type is not None:
            params["item_type"] = item_type
        if query is not None:
            params["query"] = query
        if project_id is not None:
            params["project_id"] = project_id
        if aggregations is not None:
            params["aggregations"] = aggregations
        if group_by is not None:
            params["group_by"] = group_by
        if limit is not None:
            params["limit"] = str(limit)
        if instance_id is not None:
            params["instance_id"] = instance_id
        return InventoryQueryResponse.model_validate(
            await self._http.get(
                f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/inventory",
                params=params,
            )
        )

    async def batch_import(
        self,
        agent_id: str,
        user_id: str,
        *,
        items: list[dict[str, Any]],
        project_id: str | None = None,
        instance_id: str | None = None,
    ) -> InventoryBatchImportResponse:
        """Batch-import inventory items (up to 1000)."""
        body: dict[str, Any] = {"items": items}
        if project_id is not None:
            body["project_id"] = project_id
        params: dict[str, str] | None = None
        if instance_id is not None:
            params = {"instance_id": instance_id}
        return InventoryBatchImportResponse.model_validate(
            await self._http.post(
                f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/inventory/batch",
                json_data=body,
                params=params,
            )
        )

    async def direct_update(
        self,
        agent_id: str,
        user_id: str,
        fact_id: str,
        *,
        properties: dict[str, Any],
        instance_id: str | None = None,
    ) -> InventoryDirectUpdateResponse:
        """Directly update an inventory fact's properties by fact ID."""
        path = f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/inventory/{quote(fact_id, safe='')}"
        if instance_id is not None:
            path += f"?instance_id={quote(instance_id, safe='')}"
        return InventoryDirectUpdateResponse.model_validate(
            await self._http.put(path, json_data={"properties": properties})
        )

    async def direct_delete(
        self,
        agent_id: str,
        user_id: str,
        fact_id: str,
        *,
        instance_id: str | None = None,
    ) -> InventoryDirectUpdateResponse:
        """Directly delete an inventory item by fact ID."""
        params: dict[str, str] | None = None
        if instance_id is not None:
            params = {"instance_id": instance_id}
        return InventoryDirectUpdateResponse.model_validate(
            await self._http.delete(
                f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/inventory/{quote(fact_id, safe='')}",
                params=params,
            )
        )

    async def list_all_facts(
        self,
        agent_id: str,
        user_id: str,
        *,
        has_metadata: bool = False,
        item_type: str | None = None,
        limit: int | None = None,
        instance_id: str | None = None,
    ) -> ListAllFactsResponse:
        """List all active facts for an agent+user pair."""
        params: dict[str, str] = {}
        if has_metadata:
            params["has_metadata"] = "true"
        if item_type is not None:
            params["metadata.item_type"] = item_type
        if limit is not None:
            params["limit"] = str(limit)
        if instance_id is not None:
            params["instance_id"] = instance_id
        return ListAllFactsResponse.model_validate(
            await self._http.get(
                f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/facts",
                params=params,
            )
        )
