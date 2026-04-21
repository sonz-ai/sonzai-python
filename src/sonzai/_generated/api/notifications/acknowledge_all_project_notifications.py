from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.acknowledge_all_project_notifications_output_body import AcknowledgeAllProjectNotificationsOutputBody
from ...models.error_model import ErrorModel
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    agent_id: str | Unset = UNSET,
    event_type: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["agent_id"] = agent_id

    params["event_type"] = event_type


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/notifications/acknowledge-all".format(project_id=quote(str(project_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AcknowledgeAllProjectNotificationsOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = AcknowledgeAllProjectNotificationsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AcknowledgeAllProjectNotificationsOutputBody | ErrorModel]:
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

) -> Response[AcknowledgeAllProjectNotificationsOutputBody | ErrorModel]:
    """ Acknowledge all pending project notifications

     Marks all pending notifications for a project as acknowledged. Can be scoped by agent ID and/or
    event type.

    Args:
        project_id (str): Project UUID
        agent_id (str | Unset): Scope to specific agent
        event_type (str | Unset): Scope to specific event type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AcknowledgeAllProjectNotificationsOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
agent_id=agent_id,
event_type=event_type,

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

) -> AcknowledgeAllProjectNotificationsOutputBody | ErrorModel | None:
    """ Acknowledge all pending project notifications

     Marks all pending notifications for a project as acknowledged. Can be scoped by agent ID and/or
    event type.

    Args:
        project_id (str): Project UUID
        agent_id (str | Unset): Scope to specific agent
        event_type (str | Unset): Scope to specific event type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AcknowledgeAllProjectNotificationsOutputBody | ErrorModel
     """


    return sync_detailed(
        project_id=project_id,
client=client,
agent_id=agent_id,
event_type=event_type,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    event_type: str | Unset = UNSET,

) -> Response[AcknowledgeAllProjectNotificationsOutputBody | ErrorModel]:
    """ Acknowledge all pending project notifications

     Marks all pending notifications for a project as acknowledged. Can be scoped by agent ID and/or
    event type.

    Args:
        project_id (str): Project UUID
        agent_id (str | Unset): Scope to specific agent
        event_type (str | Unset): Scope to specific event type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AcknowledgeAllProjectNotificationsOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
agent_id=agent_id,
event_type=event_type,

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

) -> AcknowledgeAllProjectNotificationsOutputBody | ErrorModel | None:
    """ Acknowledge all pending project notifications

     Marks all pending notifications for a project as acknowledged. Can be scoped by agent ID and/or
    event type.

    Args:
        project_id (str): Project UUID
        agent_id (str | Unset): Scope to specific agent
        event_type (str | Unset): Scope to specific event type

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AcknowledgeAllProjectNotificationsOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
agent_id=agent_id,
event_type=event_type,

    )).parsed
