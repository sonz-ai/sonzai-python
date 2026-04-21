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
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    mode: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["q"] = q

    params["user_id"] = user_id

    params["instance_id"] = instance_id

    params["mode"] = mode

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
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    mode: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> Response[ErrorModel | SearchResponse]:
    """ Search agent memories (semantic or BM25)

     Searches across the agent's indexed memory facts. When a user_id is provided and a vector index is
    wired (default in production), results are ranked by cosine similarity to the query embedding.
    Otherwise falls back to a BM25 token search. Pass `mode=bm25` to force the lexical path even when
    user_id is set.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query text
        user_id (str | Unset): Optional user ID. When set and a vector index is available, search
            uses cosine similarity over fact embeddings; otherwise falls back to BM25.
        instance_id (str | Unset): Optional instance ID for scoping
        mode (str | Unset): Retrieval mode: 'semantic' (requires user_id), 'bm25', or 'auto'
            (default). 'auto' picks semantic when user_id is set and a vector index is wired.
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
user_id=user_id,
instance_id=instance_id,
mode=mode,
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
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    mode: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> ErrorModel | SearchResponse | None:
    """ Search agent memories (semantic or BM25)

     Searches across the agent's indexed memory facts. When a user_id is provided and a vector index is
    wired (default in production), results are ranked by cosine similarity to the query embedding.
    Otherwise falls back to a BM25 token search. Pass `mode=bm25` to force the lexical path even when
    user_id is set.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query text
        user_id (str | Unset): Optional user ID. When set and a vector index is available, search
            uses cosine similarity over fact embeddings; otherwise falls back to BM25.
        instance_id (str | Unset): Optional instance ID for scoping
        mode (str | Unset): Retrieval mode: 'semantic' (requires user_id), 'bm25', or 'auto'
            (default). 'auto' picks semantic when user_id is set and a vector index is wired.
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
user_id=user_id,
instance_id=instance_id,
mode=mode,
limit=limit,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    q: str,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    mode: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> Response[ErrorModel | SearchResponse]:
    """ Search agent memories (semantic or BM25)

     Searches across the agent's indexed memory facts. When a user_id is provided and a vector index is
    wired (default in production), results are ranked by cosine similarity to the query embedding.
    Otherwise falls back to a BM25 token search. Pass `mode=bm25` to force the lexical path even when
    user_id is set.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query text
        user_id (str | Unset): Optional user ID. When set and a vector index is available, search
            uses cosine similarity over fact embeddings; otherwise falls back to BM25.
        instance_id (str | Unset): Optional instance ID for scoping
        mode (str | Unset): Retrieval mode: 'semantic' (requires user_id), 'bm25', or 'auto'
            (default). 'auto' picks semantic when user_id is set and a vector index is wired.
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
user_id=user_id,
instance_id=instance_id,
mode=mode,
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
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    mode: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> ErrorModel | SearchResponse | None:
    """ Search agent memories (semantic or BM25)

     Searches across the agent's indexed memory facts. When a user_id is provided and a vector index is
    wired (default in production), results are ranked by cosine similarity to the query embedding.
    Otherwise falls back to a BM25 token search. Pass `mode=bm25` to force the lexical path even when
    user_id is set.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query text
        user_id (str | Unset): Optional user ID. When set and a vector index is available, search
            uses cosine similarity over fact embeddings; otherwise falls back to BM25.
        instance_id (str | Unset): Optional instance ID for scoping
        mode (str | Unset): Retrieval mode: 'semantic' (requires user_id), 'bm25', or 'auto'
            (default). 'auto' picks semantic when user_id is set and a vector index is wired.
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
user_id=user_id,
instance_id=instance_id,
mode=mode,
limit=limit,

    )).parsed
