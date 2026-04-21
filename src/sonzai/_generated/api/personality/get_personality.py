from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.personality_response import PersonalityResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    history_limit: int | Unset = 200,
    since: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["history_limit"] = history_limit

    params["since"] = since


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/personality".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | PersonalityResponse:
    if response.status_code == 200:
        response_200 = PersonalityResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | PersonalityResponse]:
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
    history_limit: int | Unset = 200,
    since: str | Unset = UNSET,

) -> Response[ErrorModel | PersonalityResponse]:
    """ Get agent personality profile and evolution

     Returns the agent's personality profile (Big5, dimensions, traits) and recent personality evolution
    deltas.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        history_limit (int | Unset): Max evolution entries to return (1-1000) Default: 200.
        since (str | Unset): Start date for evolution history (YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | PersonalityResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
history_limit=history_limit,
since=since,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    history_limit: int | Unset = 200,
    since: str | Unset = UNSET,

) -> ErrorModel | PersonalityResponse | None:
    """ Get agent personality profile and evolution

     Returns the agent's personality profile (Big5, dimensions, traits) and recent personality evolution
    deltas.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        history_limit (int | Unset): Max evolution entries to return (1-1000) Default: 200.
        since (str | Unset): Start date for evolution history (YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | PersonalityResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
history_limit=history_limit,
since=since,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    history_limit: int | Unset = 200,
    since: str | Unset = UNSET,

) -> Response[ErrorModel | PersonalityResponse]:
    """ Get agent personality profile and evolution

     Returns the agent's personality profile (Big5, dimensions, traits) and recent personality evolution
    deltas.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        history_limit (int | Unset): Max evolution entries to return (1-1000) Default: 200.
        since (str | Unset): Start date for evolution history (YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | PersonalityResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
history_limit=history_limit,
since=since,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    history_limit: int | Unset = 200,
    since: str | Unset = UNSET,

) -> ErrorModel | PersonalityResponse | None:
    """ Get agent personality profile and evolution

     Returns the agent's personality profile (Big5, dimensions, traits) and recent personality evolution
    deltas.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        history_limit (int | Unset): Max evolution entries to return (1-1000) Default: 200.
        since (str | Unset): Start date for evolution history (YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | PersonalityResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
history_limit=history_limit,
since=since,

    )).parsed
