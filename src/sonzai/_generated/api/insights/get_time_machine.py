from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.time_machine_response import TimeMachineResponse
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    at: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["at"] = at


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/timemachine".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | TimeMachineResponse:
    if response.status_code == 200:
        response_200 = TimeMachineResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | TimeMachineResponse]:
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
    at: str,

) -> Response[ErrorModel | TimeMachineResponse]:
    """ Reconstruct personality at a point in time

     Replays personality evolution deltas up to the requested timestamp to reconstruct what the agent's
    personality looked like at that moment.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        at (str): ISO 8601 timestamp to reconstruct personality at

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | TimeMachineResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
at=at,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    at: str,

) -> ErrorModel | TimeMachineResponse | None:
    """ Reconstruct personality at a point in time

     Replays personality evolution deltas up to the requested timestamp to reconstruct what the agent's
    personality looked like at that moment.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        at (str): ISO 8601 timestamp to reconstruct personality at

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | TimeMachineResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
at=at,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    at: str,

) -> Response[ErrorModel | TimeMachineResponse]:
    """ Reconstruct personality at a point in time

     Replays personality evolution deltas up to the requested timestamp to reconstruct what the agent's
    personality looked like at that moment.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        at (str): ISO 8601 timestamp to reconstruct personality at

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | TimeMachineResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
at=at,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    at: str,

) -> ErrorModel | TimeMachineResponse | None:
    """ Reconstruct personality at a point in time

     Replays personality evolution deltas up to the requested timestamp to reconstruct what the agent's
    personality looked like at that moment.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        at (str): ISO 8601 timestamp to reconstruct personality at

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | TimeMachineResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
at=at,

    )).parsed
