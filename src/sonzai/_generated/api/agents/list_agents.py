from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.paginated_agents_response import PaginatedAgentsResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    page_size: int | Unset = 30,
    cursor: str | Unset = UNSET,
    search: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    include_count: str | Unset = UNSET,
    limit: int | Unset = 50,
    offset: int | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page_size"] = page_size

    params["cursor"] = cursor

    params["search"] = search

    params["project_id"] = project_id

    params["include_count"] = include_count

    params["limit"] = limit

    params["offset"] = offset


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | PaginatedAgentsResponse:
    if response.status_code == 200:
        response_200 = PaginatedAgentsResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | PaginatedAgentsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page_size: int | Unset = 30,
    cursor: str | Unset = UNSET,
    search: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    include_count: str | Unset = UNSET,
    limit: int | Unset = 50,
    offset: int | Unset = UNSET,

) -> Response[ErrorModel | PaginatedAgentsResponse]:
    """ List agents

     Returns agents for the caller's tenant, optionally filtered by project. Supports cursor-based
    pagination (page_size+cursor) and legacy offset-based pagination (limit+offset).

    Args:
        page_size (int | Unset): Items per page (cursor mode) Default: 30.
        cursor (str | Unset): Pagination cursor (base64)
        search (str | Unset): Free-text search filter
        project_id (str | Unset): Filter by project UUID
        include_count (str | Unset): Set to 'true' to include total_count (expensive)
        limit (int | Unset): Items per page (legacy offset mode) Default: 50.
        offset (int | Unset): Offset for legacy pagination

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | PaginatedAgentsResponse]
     """


    kwargs = _get_kwargs(
        page_size=page_size,
cursor=cursor,
search=search,
project_id=project_id,
include_count=include_count,
limit=limit,
offset=offset,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    page_size: int | Unset = 30,
    cursor: str | Unset = UNSET,
    search: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    include_count: str | Unset = UNSET,
    limit: int | Unset = 50,
    offset: int | Unset = UNSET,

) -> ErrorModel | PaginatedAgentsResponse | None:
    """ List agents

     Returns agents for the caller's tenant, optionally filtered by project. Supports cursor-based
    pagination (page_size+cursor) and legacy offset-based pagination (limit+offset).

    Args:
        page_size (int | Unset): Items per page (cursor mode) Default: 30.
        cursor (str | Unset): Pagination cursor (base64)
        search (str | Unset): Free-text search filter
        project_id (str | Unset): Filter by project UUID
        include_count (str | Unset): Set to 'true' to include total_count (expensive)
        limit (int | Unset): Items per page (legacy offset mode) Default: 50.
        offset (int | Unset): Offset for legacy pagination

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | PaginatedAgentsResponse
     """


    return sync_detailed(
        client=client,
page_size=page_size,
cursor=cursor,
search=search,
project_id=project_id,
include_count=include_count,
limit=limit,
offset=offset,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page_size: int | Unset = 30,
    cursor: str | Unset = UNSET,
    search: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    include_count: str | Unset = UNSET,
    limit: int | Unset = 50,
    offset: int | Unset = UNSET,

) -> Response[ErrorModel | PaginatedAgentsResponse]:
    """ List agents

     Returns agents for the caller's tenant, optionally filtered by project. Supports cursor-based
    pagination (page_size+cursor) and legacy offset-based pagination (limit+offset).

    Args:
        page_size (int | Unset): Items per page (cursor mode) Default: 30.
        cursor (str | Unset): Pagination cursor (base64)
        search (str | Unset): Free-text search filter
        project_id (str | Unset): Filter by project UUID
        include_count (str | Unset): Set to 'true' to include total_count (expensive)
        limit (int | Unset): Items per page (legacy offset mode) Default: 50.
        offset (int | Unset): Offset for legacy pagination

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | PaginatedAgentsResponse]
     """


    kwargs = _get_kwargs(
        page_size=page_size,
cursor=cursor,
search=search,
project_id=project_id,
include_count=include_count,
limit=limit,
offset=offset,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    page_size: int | Unset = 30,
    cursor: str | Unset = UNSET,
    search: str | Unset = UNSET,
    project_id: str | Unset = UNSET,
    include_count: str | Unset = UNSET,
    limit: int | Unset = 50,
    offset: int | Unset = UNSET,

) -> ErrorModel | PaginatedAgentsResponse | None:
    """ List agents

     Returns agents for the caller's tenant, optionally filtered by project. Supports cursor-based
    pagination (page_size+cursor) and legacy offset-based pagination (limit+offset).

    Args:
        page_size (int | Unset): Items per page (cursor mode) Default: 30.
        cursor (str | Unset): Pagination cursor (base64)
        search (str | Unset): Free-text search filter
        project_id (str | Unset): Filter by project UUID
        include_count (str | Unset): Set to 'true' to include total_count (expensive)
        limit (int | Unset): Items per page (legacy offset mode) Default: 50.
        offset (int | Unset): Offset for legacy pagination

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | PaginatedAgentsResponse
     """


    return (await asyncio_detailed(
        client=client,
page_size=page_size,
cursor=cursor,
search=search,
project_id=project_id,
include_count=include_count,
limit=limit,
offset=offset,

    )).parsed
