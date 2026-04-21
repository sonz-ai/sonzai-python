from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.agent_kb_search_input_body import AgentKBSearchInputBody
from ...models.error_model import ErrorModel
from ...models.kb_search_response import KbSearchResponse
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: AgentKBSearchInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/tools/kb-search".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbSearchResponse:
    if response.status_code == 200:
        response_200 = KbSearchResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbSearchResponse]:
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
    body: AgentKBSearchInputBody,

) -> Response[ErrorModel | KbSearchResponse]:
    """ Search agent knowledge base

     Searches the agent's configured knowledge base and returns ranked results. Uses hybrid BM25 +
    semantic search when available.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (AgentKBSearchInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbSearchResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: AgentKBSearchInputBody,

) -> ErrorModel | KbSearchResponse | None:
    """ Search agent knowledge base

     Searches the agent's configured knowledge base and returns ranked results. Uses hybrid BM25 +
    semantic search when available.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (AgentKBSearchInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbSearchResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: AgentKBSearchInputBody,

) -> Response[ErrorModel | KbSearchResponse]:
    """ Search agent knowledge base

     Searches the agent's configured knowledge base and returns ranked results. Uses hybrid BM25 +
    semantic search when available.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (AgentKBSearchInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbSearchResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: AgentKBSearchInputBody,

) -> ErrorModel | KbSearchResponse | None:
    """ Search agent knowledge base

     Searches the agent's configured knowledge base and returns ranked results. Uses hybrid BM25 +
    semantic search when available.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (AgentKBSearchInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbSearchResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,

    )).parsed
