from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.habit import Habit
from ...models.update_habit_input_body import UpdateHabitInputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    habit_name: str,
    *,
    body: UpdateHabitInputBody,
    instance_id: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["instance_id"] = instance_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/agents/{agent_id}/habits/{habit_name}".format(agent_id=quote(str(agent_id), safe=""),habit_name=quote(str(habit_name), safe=""),),
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
    habit_name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateHabitInputBody,
    instance_id: str | Unset = UNSET,

) -> Response[ErrorModel | Habit]:
    """ Update a habit

     Updates an existing habit. Set `user_id` in the body for per-user habits.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        habit_name (str): Habit name
        instance_id (str | Unset): Optional instance ID for scoping
        body (UpdateHabitInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | Habit]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
habit_name=habit_name,
body=body,
instance_id=instance_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    habit_name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateHabitInputBody,
    instance_id: str | Unset = UNSET,

) -> ErrorModel | Habit | None:
    """ Update a habit

     Updates an existing habit. Set `user_id` in the body for per-user habits.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        habit_name (str): Habit name
        instance_id (str | Unset): Optional instance ID for scoping
        body (UpdateHabitInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | Habit
     """


    return sync_detailed(
        agent_id=agent_id,
habit_name=habit_name,
client=client,
body=body,
instance_id=instance_id,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    habit_name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateHabitInputBody,
    instance_id: str | Unset = UNSET,

) -> Response[ErrorModel | Habit]:
    """ Update a habit

     Updates an existing habit. Set `user_id` in the body for per-user habits.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        habit_name (str): Habit name
        instance_id (str | Unset): Optional instance ID for scoping
        body (UpdateHabitInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | Habit]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
habit_name=habit_name,
body=body,
instance_id=instance_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    habit_name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateHabitInputBody,
    instance_id: str | Unset = UNSET,

) -> ErrorModel | Habit | None:
    """ Update a habit

     Updates an existing habit. Set `user_id` in the body for per-user habits.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        habit_name (str): Habit name
        instance_id (str | Unset): Optional instance ID for scoping
        body (UpdateHabitInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | Habit
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
habit_name=habit_name,
client=client,
body=body,
instance_id=instance_id,

    )).parsed
