from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.schedule_dto import ScheduleDTO
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,
    schedule_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/users/{user_id}/schedules/{schedule_id}".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),schedule_id=quote(str(schedule_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ScheduleDTO | None:
    if response.status_code == 200:
        response_200 = ScheduleDTO.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = ErrorModel.from_dict(response.json())



        return response_404

    if response.status_code == 422:
        response_422 = ErrorModel.from_dict(response.json())



        return response_422

    if response.status_code == 500:
        response_500 = ErrorModel.from_dict(response.json())



        return response_500

    if response.status_code == 503:
        response_503 = ErrorModel.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ScheduleDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    user_id: str,
    schedule_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | ScheduleDTO]:
    """ Fetch a single schedule by ID.

    Args:
        agent_id (str):
        user_id (str):
        schedule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ScheduleDTO]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
schedule_id=schedule_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    user_id: str,
    schedule_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | ScheduleDTO | None:
    """ Fetch a single schedule by ID.

    Args:
        agent_id (str):
        user_id (str):
        schedule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ScheduleDTO
     """


    return sync_detailed(
        agent_id=agent_id,
user_id=user_id,
schedule_id=schedule_id,
client=client,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    user_id: str,
    schedule_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | ScheduleDTO]:
    """ Fetch a single schedule by ID.

    Args:
        agent_id (str):
        user_id (str):
        schedule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ScheduleDTO]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
schedule_id=schedule_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    user_id: str,
    schedule_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | ScheduleDTO | None:
    """ Fetch a single schedule by ID.

    Args:
        agent_id (str):
        user_id (str):
        schedule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ScheduleDTO
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
schedule_id=schedule_id,
client=client,

    )).parsed
