from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.user_overlays_list_response import UserOverlaysListResponse
from typing import cast



def _get_kwargs(
    agent_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/personality/users".format(agent_id=quote(str(agent_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | UserOverlaysListResponse:
    if response.status_code == 200:
        response_200 = UserOverlaysListResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | UserOverlaysListResponse]:
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

) -> Response[ErrorModel | UserOverlaysListResponse]:
    """ List per-user personality overlays

     Returns all per-user personality overlays for an agent, showing how the agent adapts to each user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UserOverlaysListResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | UserOverlaysListResponse | None:
    """ List per-user personality overlays

     Returns all per-user personality overlays for an agent, showing how the agent adapts to each user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UserOverlaysListResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | UserOverlaysListResponse]:
    """ List per-user personality overlays

     Returns all per-user personality overlays for an agent, showing how the agent adapts to each user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UserOverlaysListResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | UserOverlaysListResponse | None:
    """ List per-user personality overlays

     Returns all per-user personality overlays for an agent, showing how the agent adapts to each user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UserOverlaysListResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,

    )).parsed
