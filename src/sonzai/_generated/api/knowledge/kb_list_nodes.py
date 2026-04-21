from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_list_nodes_output_body import KbListNodesOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    type_: str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["type"] = type_

    params["limit"] = limit

    params["offset"] = offset

    params["sort_by"] = sort_by

    params["sort_order"] = sort_order


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/nodes".format(project_id=quote(str(project_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbListNodesOutputBody:
    if response.status_code == 200:
        response_200 = KbListNodesOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbListNodesOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    type_: str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,

) -> Response[ErrorModel | KbListNodesOutputBody]:
    """ List knowledge base nodes

     Returns active nodes with support for property-level filtering, pagination, and sorting. Filter
    operators: eq (default), __neq, __gt, __gte, __lt, __lte, __in, __contains via query params like
    properties.field__gt=5.

    Args:
        project_id (str): Project UUID
        type_ (str | Unset): Filter by node type
        limit (int | Unset): Max results Default: 100.
        offset (int | Unset): Pagination offset Default: 0.
        sort_by (str | Unset): Sort field (label, node_type, created_at, updated_at, version, or
            properties.*)
        sort_order (str | Unset): Sort direction: asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbListNodesOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
type_=type_,
limit=limit,
offset=offset,
sort_by=sort_by,
sort_order=sort_order,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    type_: str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,

) -> ErrorModel | KbListNodesOutputBody | None:
    """ List knowledge base nodes

     Returns active nodes with support for property-level filtering, pagination, and sorting. Filter
    operators: eq (default), __neq, __gt, __gte, __lt, __lte, __in, __contains via query params like
    properties.field__gt=5.

    Args:
        project_id (str): Project UUID
        type_ (str | Unset): Filter by node type
        limit (int | Unset): Max results Default: 100.
        offset (int | Unset): Pagination offset Default: 0.
        sort_by (str | Unset): Sort field (label, node_type, created_at, updated_at, version, or
            properties.*)
        sort_order (str | Unset): Sort direction: asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbListNodesOutputBody
     """


    return sync_detailed(
        project_id=project_id,
client=client,
type_=type_,
limit=limit,
offset=offset,
sort_by=sort_by,
sort_order=sort_order,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    type_: str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,

) -> Response[ErrorModel | KbListNodesOutputBody]:
    """ List knowledge base nodes

     Returns active nodes with support for property-level filtering, pagination, and sorting. Filter
    operators: eq (default), __neq, __gt, __gte, __lt, __lte, __in, __contains via query params like
    properties.field__gt=5.

    Args:
        project_id (str): Project UUID
        type_ (str | Unset): Filter by node type
        limit (int | Unset): Max results Default: 100.
        offset (int | Unset): Pagination offset Default: 0.
        sort_by (str | Unset): Sort field (label, node_type, created_at, updated_at, version, or
            properties.*)
        sort_order (str | Unset): Sort direction: asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbListNodesOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
type_=type_,
limit=limit,
offset=offset,
sort_by=sort_by,
sort_order=sort_order,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    type_: str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,

) -> ErrorModel | KbListNodesOutputBody | None:
    """ List knowledge base nodes

     Returns active nodes with support for property-level filtering, pagination, and sorting. Filter
    operators: eq (default), __neq, __gt, __gte, __lt, __lte, __in, __contains via query params like
    properties.field__gt=5.

    Args:
        project_id (str): Project UUID
        type_ (str | Unset): Filter by node type
        limit (int | Unset): Max results Default: 100.
        offset (int | Unset): Pagination offset Default: 0.
        sort_by (str | Unset): Sort field (label, node_type, created_at, updated_at, version, or
            properties.*)
        sort_order (str | Unset): Sort direction: asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbListNodesOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
type_=type_,
limit=limit,
offset=offset,
sort_by=sort_by,
sort_order=sort_order,

    )).parsed
