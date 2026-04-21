from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.search_response import SearchResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    q: str,
    instance_id: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["q"] = q

    params["instance_id"] = instance_id

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/memory/search".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | SearchResponse:
    if response.status_code == 200:
        response_200 = SearchResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | SearchResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    q: str,
    instance_id: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> Response[ErrorModel | SearchResponse]:
    """ Search agent memories via BM25

     Performs a BM25 text search across the agent's indexed memory facts. Returns scored results ordered
    by relevance.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query text
        instance_id (str | Unset): Optional instance ID for scoping
        limit (str | Unset): Max results to return (default 20, max 100)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SearchResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
q=q,
instance_id=instance_id,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    q: str,
    instance_id: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> ErrorModel | SearchResponse | None:
    """ Search agent memories via BM25

     Performs a BM25 text search across the agent's indexed memory facts. Returns scored results ordered
    by relevance.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query text
        instance_id (str | Unset): Optional instance ID for scoping
        limit (str | Unset): Max results to return (default 20, max 100)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SearchResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
q=q,
instance_id=instance_id,
limit=limit,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    q: str,
    instance_id: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> Response[ErrorModel | SearchResponse]:
    """ Search agent memories via BM25

     Performs a BM25 text search across the agent's indexed memory facts. Returns scored results ordered
    by relevance.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query text
        instance_id (str | Unset): Optional instance ID for scoping
        limit (str | Unset): Max results to return (default 20, max 100)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SearchResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
q=q,
instance_id=instance_id,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    q: str,
    instance_id: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> ErrorModel | SearchResponse | None:
    """ Search agent memories via BM25

     Performs a BM25 text search across the agent's indexed memory facts. Returns scored results ordered
    by relevance.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query text
        instance_id (str | Unset): Optional instance ID for scoping
        limit (str | Unset): Max results to return (default 20, max 100)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SearchResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
q=q,
instance_id=instance_id,
limit=limit,

    )).parsed
