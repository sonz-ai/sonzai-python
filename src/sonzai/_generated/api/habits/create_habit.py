from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_habit_input_body import CreateHabitInputBody
from ...models.error_model import ErrorModel
from ...models.habit import Habit
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: CreateHabitInputBody,
    instance_id: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["instance_id"] = instance_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/habits".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | Habit:
    if response.status_code == 200:
        response_200 = Habit.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | Habit]:
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
    body: CreateHabitInputBody,
    instance_id: str | Unset = UNSET,

) -> Response[ErrorModel | Habit]:
    """ Create a habit for an agent

     Creates a new habit. Set `user_id` in the body for a per-user habit. Returns 409 if a habit with
    that name already exists.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str | Unset): Optional instance ID for scoping
        body (CreateHabitInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | Habit]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,
instance_id=instance_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateHabitInputBody,
    instance_id: str | Unset = UNSET,

) -> ErrorModel | Habit | None:
    """ Create a habit for an agent

     Creates a new habit. Set `user_id` in the body for a per-user habit. Returns 409 if a habit with
    that name already exists.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str | Unset): Optional instance ID for scoping
        body (CreateHabitInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | Habit
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
body=body,
instance_id=instance_id,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateHabitInputBody,
    instance_id: str | Unset = UNSET,

) -> Response[ErrorModel | Habit]:
    """ Create a habit for an agent

     Creates a new habit. Set `user_id` in the body for a per-user habit. Returns 409 if a habit with
    that name already exists.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str | Unset): Optional instance ID for scoping
        body (CreateHabitInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | Habit]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,
instance_id=instance_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateHabitInputBody,
    instance_id: str | Unset = UNSET,

) -> ErrorModel | Habit | None:
    """ Create a habit for an agent

     Creates a new habit. Set `user_id` in the body for a per-user habit. Returns 409 if a habit with
    that name already exists.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str | Unset): Optional instance ID for scoping
        body (CreateHabitInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | Habit
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,
instance_id=instance_id,

    )).parsed
