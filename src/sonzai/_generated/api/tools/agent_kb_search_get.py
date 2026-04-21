from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_search_response import KbSearchResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    q: str,
    limit: int | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["q"] = q

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/tools/kb-search".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


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
    q: str,
    limit: int | Unset = UNSET,

) -> Response[ErrorModel | KbSearchResponse]:
    """ Search agent knowledge base (GET)

     Same as POST kb-search but accepts query parameters instead of a JSON body. Convenient for browser
    testing and GET-based integrations.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query
        limit (int | Unset): Max results (default 10, max 50)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbSearchResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
q=q,
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
    limit: int | Unset = UNSET,

) -> ErrorModel | KbSearchResponse | None:
    """ Search agent knowledge base (GET)

     Same as POST kb-search but accepts query parameters instead of a JSON body. Convenient for browser
    testing and GET-based integrations.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query
        limit (int | Unset): Max results (default 10, max 50)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbSearchResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
q=q,
limit=limit,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    q: str,
    limit: int | Unset = UNSET,

) -> Response[ErrorModel | KbSearchResponse]:
    """ Search agent knowledge base (GET)

     Same as POST kb-search but accepts query parameters instead of a JSON body. Convenient for browser
    testing and GET-based integrations.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query
        limit (int | Unset): Max results (default 10, max 50)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbSearchResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
q=q,
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
    limit: int | Unset = UNSET,

) -> ErrorModel | KbSearchResponse | None:
    """ Search agent knowledge base (GET)

     Same as POST kb-search but accepts query parameters instead of a JSON body. Convenient for browser
    testing and GET-based integrations.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        q (str): Search query
        limit (int | Unset): Max results (default 10, max 50)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbSearchResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
q=q,
limit=limit,

    )).parsed
