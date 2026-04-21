from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.project_notifications_list_output_body import ProjectNotificationsListOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    agent_id: str | Unset = UNSET,
    event_type: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["agent_id"] = agent_id

    params["event_type"] = event_type

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/notifications".format(project_id=quote(str(project_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ProjectNotificationsListOutputBody:
    if response.status_code == 200:
        response_200 = ProjectNotificationsListOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ProjectNotificationsListOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    event_type: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> Response[ErrorModel | ProjectNotificationsListOutputBody]:
    """ List pending notifications for a project

     Returns pending notifications for a project, with optional filtering by agent ID and event type.
    Supports three-layer caching.

    Args:
        project_id (str): Project UUID
        agent_id (str | Unset): Filter by agent ID
        event_type (str | Unset): Filter by event type
        limit (int | Unset): Max results Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ProjectNotificationsListOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
agent_id=agent_id,
event_type=event_type,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    event_type: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> ErrorModel | ProjectNotificationsListOutputBody | None:
    """ List pending notifications for a project

     Returns pending notifications for a project, with optional filtering by agent ID and event type.
    Supports three-layer caching.

    Args:
        project_id (str): Project UUID
        agent_id (str | Unset): Filter by agent ID
        event_type (str | Unset): Filter by event type
        limit (int | Unset): Max results Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ProjectNotificationsListOutputBody
     """


    return sync_detailed(
        project_id=project_id,
client=client,
agent_id=agent_id,
event_type=event_type,
limit=limit,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    event_type: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> Response[ErrorModel | ProjectNotificationsListOutputBody]:
    """ List pending notifications for a project

     Returns pending notifications for a project, with optional filtering by agent ID and event type.
    Supports three-layer caching.

    Args:
        project_id (str): Project UUID
        agent_id (str | Unset): Filter by agent ID
        event_type (str | Unset): Filter by event type
        limit (int | Unset): Max results Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ProjectNotificationsListOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
agent_id=agent_id,
event_type=event_type,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    event_type: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> ErrorModel | ProjectNotificationsListOutputBody | None:
    """ List pending notifications for a project

     Returns pending notifications for a project, with optional filtering by agent ID and event type.
    Supports three-layer caching.

    Args:
        project_id (str): Project UUID
        agent_id (str | Unset): Filter by agent ID
        event_type (str | Unset): Filter by event type
        limit (int | Unset): Max results Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ProjectNotificationsListOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
agent_id=agent_id,
event_type=event_type,
limit=limit,

    )).parsed
