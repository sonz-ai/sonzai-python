from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_schedule_input_body import CreateScheduleInputBody
from ...models.create_schedule_output_body import CreateScheduleOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,
    *,
    body: CreateScheduleInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/users/{user_id}/schedules".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CreateScheduleOutputBody | ErrorModel | None:
    if response.status_code == 200:
        response_200 = CreateScheduleOutputBody.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ErrorModel.from_dict(response.json())



        return response_400

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CreateScheduleOutputBody | ErrorModel]:
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
    body: CreateScheduleInputBody,

) -> Response[CreateScheduleOutputBody | ErrorModel]:
    """ Create a recurring schedule for a user.

    Args:
        agent_id (str):
        user_id (str):
        body (CreateScheduleInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateScheduleOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
body=body,

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
    body: CreateScheduleInputBody,

) -> CreateScheduleOutputBody | ErrorModel | None:
    """ Create a recurring schedule for a user.

    Args:
        agent_id (str):
        user_id (str):
        body (CreateScheduleInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateScheduleOutputBody | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateScheduleInputBody,

) -> Response[CreateScheduleOutputBody | ErrorModel]:
    """ Create a recurring schedule for a user.

    Args:
        agent_id (str):
        user_id (str):
        body (CreateScheduleInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateScheduleOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
body=body,

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
    body: CreateScheduleInputBody,

) -> CreateScheduleOutputBody | ErrorModel | None:
    """ Create a recurring schedule for a user.

    Args:
        agent_id (str):
        user_id (str):
        body (CreateScheduleInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateScheduleOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
body=body,

    )).parsed
