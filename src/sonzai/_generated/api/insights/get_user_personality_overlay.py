from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.user_overlay_detail_response import UserOverlayDetailResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,
    *,
    instance_id: str | Unset = UNSET,
    since: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["instance_id"] = instance_id

    params["since"] = since


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/personality/users/{user_id}".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | UserOverlayDetailResponse:
    if response.status_code == 200:
        response_200 = UserOverlayDetailResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | UserOverlayDetailResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    since: str | Unset = UNSET,

) -> Response[ErrorModel | UserOverlayDetailResponse]:
    """ Get user personality overlay

     Returns a specific user's personality overlay with their delta history, plus the agent's base
    personality profile for comparison.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID (scoped with userId)
        since (str | Unset): Start date for evolution history (YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UserOverlayDetailResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,
since=since,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    since: str | Unset = UNSET,

) -> ErrorModel | UserOverlayDetailResponse | None:
    """ Get user personality overlay

     Returns a specific user's personality overlay with their delta history, plus the agent's base
    personality profile for comparison.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID (scoped with userId)
        since (str | Unset): Start date for evolution history (YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UserOverlayDetailResponse
     """


    return sync_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
instance_id=instance_id,
since=since,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    since: str | Unset = UNSET,

) -> Response[ErrorModel | UserOverlayDetailResponse]:
    """ Get user personality overlay

     Returns a specific user's personality overlay with their delta history, plus the agent's base
    personality profile for comparison.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID (scoped with userId)
        since (str | Unset): Start date for evolution history (YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UserOverlayDetailResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,
since=since,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    since: str | Unset = UNSET,

) -> ErrorModel | UserOverlayDetailResponse | None:
    """ Get user personality overlay

     Returns a specific user's personality overlay with their delta history, plus the agent's base
    personality profile for comparison.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID (scoped with userId)
        since (str | Unset): Start date for evolution history (YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UserOverlayDetailResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
instance_id=instance_id,
since=since,

    )).parsed
