from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.inventory_read_response import InventoryReadResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,
    *,
    instance_id: str | Unset = UNSET,
    mode: str | Unset = 'list',
    item_type: str | Unset = UNSET,
    query: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    aggregations: str | Unset = UNSET,
    group_by: str | Unset = UNSET,
    limit: int | Unset = 1000,
    offset: int | Unset = 0,
    cursor: str | Unset = UNSET,
    filters: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = 'asc',

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["instance_id"] = instance_id

    params["mode"] = mode

    params["item_type"] = item_type

    params["query"] = query

    params["project_id"] = project_id

    params["aggregations"] = aggregations

    params["group_by"] = group_by

    params["limit"] = limit

    params["offset"] = offset

    params["cursor"] = cursor

    params["filters"] = filters

    params["sort_by"] = sort_by

    params["sort_order"] = sort_order


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/users/{user_id}/inventory".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | InventoryReadResponse:
    if response.status_code == 200:
        response_200 = InventoryReadResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | InventoryReadResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    mode: str | Unset = 'list',
    item_type: str | Unset = UNSET,
    query: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    aggregations: str | Unset = UNSET,
    group_by: str | Unset = UNSET,
    limit: int | Unset = 1000,
    offset: int | Unset = 0,
    cursor: str | Unset = UNSET,
    filters: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = 'asc',

) -> Response[ErrorModel | InventoryReadResponse]:
    """ Query user inventory

     Lists, values, or aggregates a user's inventory items. Supports filtering by item_type, free-text
    search, metadata filters, pagination, and sorting. In 'value' or 'aggregate' mode, enriches items
    with KB market data.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID for user scoping
        mode (str | Unset): Query mode: list, value, or aggregate Default: 'list'.
        item_type (str | Unset): Filter by item type
        query (str | Unset): Free-text search filter
        project_id (str | Unset): KB project scope for value/aggregate modes
        aggregations (str | Unset): Comma-separated aggregation expressions (for aggregate mode)
        group_by (str | Unset): Group-by field for aggregations
        limit (int | Unset): Max items per page (default 1000, max 5000) Default: 1000.
        offset (int | Unset): Pagination offset Default: 0.
        cursor (str | Unset): Base64-encoded pagination cursor
        filters (str | Unset): JSON-encoded metadata filters
        sort_by (str | Unset): Sort by metadata field
        sort_order (str | Unset): Sort order: asc or desc Default: 'asc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | InventoryReadResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,
mode=mode,
item_type=item_type,
query=query,
project_id=project_id,
aggregations=aggregations,
group_by=group_by,
limit=limit,
offset=offset,
cursor=cursor,
filters=filters,
sort_by=sort_by,
sort_order=sort_order,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    mode: str | Unset = 'list',
    item_type: str | Unset = UNSET,
    query: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    aggregations: str | Unset = UNSET,
    group_by: str | Unset = UNSET,
    limit: int | Unset = 1000,
    offset: int | Unset = 0,
    cursor: str | Unset = UNSET,
    filters: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = 'asc',

) -> ErrorModel | InventoryReadResponse | None:
    """ Query user inventory

     Lists, values, or aggregates a user's inventory items. Supports filtering by item_type, free-text
    search, metadata filters, pagination, and sorting. In 'value' or 'aggregate' mode, enriches items
    with KB market data.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID for user scoping
        mode (str | Unset): Query mode: list, value, or aggregate Default: 'list'.
        item_type (str | Unset): Filter by item type
        query (str | Unset): Free-text search filter
        project_id (str | Unset): KB project scope for value/aggregate modes
        aggregations (str | Unset): Comma-separated aggregation expressions (for aggregate mode)
        group_by (str | Unset): Group-by field for aggregations
        limit (int | Unset): Max items per page (default 1000, max 5000) Default: 1000.
        offset (int | Unset): Pagination offset Default: 0.
        cursor (str | Unset): Base64-encoded pagination cursor
        filters (str | Unset): JSON-encoded metadata filters
        sort_by (str | Unset): Sort by metadata field
        sort_order (str | Unset): Sort order: asc or desc Default: 'asc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | InventoryReadResponse
     """


    return sync_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
instance_id=instance_id,
mode=mode,
item_type=item_type,
query=query,
project_id=project_id,
aggregations=aggregations,
group_by=group_by,
limit=limit,
offset=offset,
cursor=cursor,
filters=filters,
sort_by=sort_by,
sort_order=sort_order,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    mode: str | Unset = 'list',
    item_type: str | Unset = UNSET,
    query: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    aggregations: str | Unset = UNSET,
    group_by: str | Unset = UNSET,
    limit: int | Unset = 1000,
    offset: int | Unset = 0,
    cursor: str | Unset = UNSET,
    filters: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = 'asc',

) -> Response[ErrorModel | InventoryReadResponse]:
    """ Query user inventory

     Lists, values, or aggregates a user's inventory items. Supports filtering by item_type, free-text
    search, metadata filters, pagination, and sorting. In 'value' or 'aggregate' mode, enriches items
    with KB market data.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID for user scoping
        mode (str | Unset): Query mode: list, value, or aggregate Default: 'list'.
        item_type (str | Unset): Filter by item type
        query (str | Unset): Free-text search filter
        project_id (str | Unset): KB project scope for value/aggregate modes
        aggregations (str | Unset): Comma-separated aggregation expressions (for aggregate mode)
        group_by (str | Unset): Group-by field for aggregations
        limit (int | Unset): Max items per page (default 1000, max 5000) Default: 1000.
        offset (int | Unset): Pagination offset Default: 0.
        cursor (str | Unset): Base64-encoded pagination cursor
        filters (str | Unset): JSON-encoded metadata filters
        sort_by (str | Unset): Sort by metadata field
        sort_order (str | Unset): Sort order: asc or desc Default: 'asc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | InventoryReadResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,
mode=mode,
item_type=item_type,
query=query,
project_id=project_id,
aggregations=aggregations,
group_by=group_by,
limit=limit,
offset=offset,
cursor=cursor,
filters=filters,
sort_by=sort_by,
sort_order=sort_order,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    mode: str | Unset = 'list',
    item_type: str | Unset = UNSET,
    query: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    aggregations: str | Unset = UNSET,
    group_by: str | Unset = UNSET,
    limit: int | Unset = 1000,
    offset: int | Unset = 0,
    cursor: str | Unset = UNSET,
    filters: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = 'asc',

) -> ErrorModel | InventoryReadResponse | None:
    """ Query user inventory

     Lists, values, or aggregates a user's inventory items. Supports filtering by item_type, free-text
    search, metadata filters, pagination, and sorting. In 'value' or 'aggregate' mode, enriches items
    with KB market data.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID for user scoping
        mode (str | Unset): Query mode: list, value, or aggregate Default: 'list'.
        item_type (str | Unset): Filter by item type
        query (str | Unset): Free-text search filter
        project_id (str | Unset): KB project scope for value/aggregate modes
        aggregations (str | Unset): Comma-separated aggregation expressions (for aggregate mode)
        group_by (str | Unset): Group-by field for aggregations
        limit (int | Unset): Max items per page (default 1000, max 5000) Default: 1000.
        offset (int | Unset): Pagination offset Default: 0.
        cursor (str | Unset): Base64-encoded pagination cursor
        filters (str | Unset): JSON-encoded metadata filters
        sort_by (str | Unset): Sort by metadata field
        sort_order (str | Unset): Sort order: asc or desc Default: 'asc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | InventoryReadResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
instance_id=instance_id,
mode=mode,
item_type=item_type,
query=query,
project_id=project_id,
aggregations=aggregations,
group_by=group_by,
limit=limit,
offset=offset,
cursor=cursor,
filters=filters,
sort_by=sort_by,
sort_order=sort_order,

    )).parsed
