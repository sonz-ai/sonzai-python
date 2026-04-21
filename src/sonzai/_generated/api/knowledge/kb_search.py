from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_search_response import KBSearchResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    q: str,
    limit: int | Unset = 20,
    depth: int | Unset = 1,
    history: str | Unset = UNSET,
    type_: str | Unset = UNSET,
    mode: str | Unset = UNSET,
    filters: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["q"] = q

    params["limit"] = limit

    params["depth"] = depth

    params["history"] = history

    params["type"] = type_

    params["mode"] = mode

    params["filters"] = filters


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/search".format(project_id=quote(str(project_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KBSearchResponse:
    if response.status_code == 200:
        response_200 = KBSearchResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KBSearchResponse]:
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
    q: str,
    limit: int | Unset = 20,
    depth: int | Unset = 1,
    history: str | Unset = UNSET,
    type_: str | Unset = UNSET,
    mode: str | Unset = UNSET,
    filters: str | Unset = UNSET,

) -> Response[ErrorModel | KBSearchResponse]:
    """ Search the knowledge base

     Performs BM25/semantic/hybrid search with property filtering and 1-2 hop graph traversal.

    Args:
        project_id (str): Project UUID
        q (str): Search query text
        limit (int | Unset): Max results Default: 20.
        depth (int | Unset): Graph traversal depth (1 or 2) Default: 1.
        history (str | Unset): Set to 'true' to include version history per result
        type_ (str | Unset): Comma-separated entity types to filter
        mode (str | Unset): Search mode: bm25, semantic, hybrid, or auto
        filters (str | Unset): JSON object of property filters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBSearchResponse]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
q=q,
limit=limit,
depth=depth,
history=history,
type_=type_,
mode=mode,
filters=filters,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    q: str,
    limit: int | Unset = 20,
    depth: int | Unset = 1,
    history: str | Unset = UNSET,
    type_: str | Unset = UNSET,
    mode: str | Unset = UNSET,
    filters: str | Unset = UNSET,

) -> ErrorModel | KBSearchResponse | None:
    """ Search the knowledge base

     Performs BM25/semantic/hybrid search with property filtering and 1-2 hop graph traversal.

    Args:
        project_id (str): Project UUID
        q (str): Search query text
        limit (int | Unset): Max results Default: 20.
        depth (int | Unset): Graph traversal depth (1 or 2) Default: 1.
        history (str | Unset): Set to 'true' to include version history per result
        type_ (str | Unset): Comma-separated entity types to filter
        mode (str | Unset): Search mode: bm25, semantic, hybrid, or auto
        filters (str | Unset): JSON object of property filters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBSearchResponse
     """


    return sync_detailed(
        project_id=project_id,
client=client,
q=q,
limit=limit,
depth=depth,
history=history,
type_=type_,
mode=mode,
filters=filters,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    q: str,
    limit: int | Unset = 20,
    depth: int | Unset = 1,
    history: str | Unset = UNSET,
    type_: str | Unset = UNSET,
    mode: str | Unset = UNSET,
    filters: str | Unset = UNSET,

) -> Response[ErrorModel | KBSearchResponse]:
    """ Search the knowledge base

     Performs BM25/semantic/hybrid search with property filtering and 1-2 hop graph traversal.

    Args:
        project_id (str): Project UUID
        q (str): Search query text
        limit (int | Unset): Max results Default: 20.
        depth (int | Unset): Graph traversal depth (1 or 2) Default: 1.
        history (str | Unset): Set to 'true' to include version history per result
        type_ (str | Unset): Comma-separated entity types to filter
        mode (str | Unset): Search mode: bm25, semantic, hybrid, or auto
        filters (str | Unset): JSON object of property filters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBSearchResponse]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
q=q,
limit=limit,
depth=depth,
history=history,
type_=type_,
mode=mode,
filters=filters,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    q: str,
    limit: int | Unset = 20,
    depth: int | Unset = 1,
    history: str | Unset = UNSET,
    type_: str | Unset = UNSET,
    mode: str | Unset = UNSET,
    filters: str | Unset = UNSET,

) -> ErrorModel | KBSearchResponse | None:
    """ Search the knowledge base

     Performs BM25/semantic/hybrid search with property filtering and 1-2 hop graph traversal.

    Args:
        project_id (str): Project UUID
        q (str): Search query text
        limit (int | Unset): Max results Default: 20.
        depth (int | Unset): Graph traversal depth (1 or 2) Default: 1.
        history (str | Unset): Set to 'true' to include version history per result
        type_ (str | Unset): Comma-separated entity types to filter
        mode (str | Unset): Search mode: bm25, semantic, hybrid, or auto
        filters (str | Unset): JSON object of property filters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBSearchResponse
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
q=q,
limit=limit,
depth=depth,
history=history,
type_=type_,
mode=mode,
filters=filters,

    )).parsed
