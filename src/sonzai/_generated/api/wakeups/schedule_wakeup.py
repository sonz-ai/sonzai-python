from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.schedule_wakeup_input_body import ScheduleWakeupInputBody
from ...models.schedule_wakeup_output_body import ScheduleWakeupOutputBody
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: ScheduleWakeupInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/wakeups".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ScheduleWakeupOutputBody:
    if response.status_code == 200:
        response_200 = ScheduleWakeupOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ScheduleWakeupOutputBody]:
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
    body: ScheduleWakeupInputBody,

) -> Response[ErrorModel | ScheduleWakeupOutputBody]:
    """ Schedule a wakeup for an agent

     Schedules a new wakeup that will trigger the agent to proactively reach out to the specified user
    after the given delay.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (ScheduleWakeupInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ScheduleWakeupOutputBody]
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
    body: ScheduleWakeupInputBody,

) -> ErrorModel | ScheduleWakeupOutputBody | None:
    """ Schedule a wakeup for an agent

     Schedules a new wakeup that will trigger the agent to proactively reach out to the specified user
    after the given delay.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (ScheduleWakeupInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ScheduleWakeupOutputBody
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
    body: ScheduleWakeupInputBody,

) -> Response[ErrorModel | ScheduleWakeupOutputBody]:
    """ Schedule a wakeup for an agent

     Schedules a new wakeup that will trigger the agent to proactively reach out to the specified user
    after the given delay.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (ScheduleWakeupInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ScheduleWakeupOutputBody]
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
    body: ScheduleWakeupInputBody,

) -> ErrorModel | ScheduleWakeupOutputBody | None:
    """ Schedule a wakeup for an agent

     Schedules a new wakeup that will trigger the agent to proactively reach out to the specified user
    after the given delay.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (ScheduleWakeupInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ScheduleWakeupOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,

    )).parsed
