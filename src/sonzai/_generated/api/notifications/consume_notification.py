from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.consume_notification_output_body import ConsumeNotificationOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    agent_id: str,
    message_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/notifications/{message_id}/consume".format(agent_id=quote(str(agent_id), safe=""),message_id=quote(str(message_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ConsumeNotificationOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = ConsumeNotificationOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ConsumeNotificationOutputBody | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    message_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ConsumeNotificationOutputBody | ErrorModel]:
    """ Consume a proactive notification

     Marks a proactive message as consumed and invalidates the agent's notification caches.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        message_id (str): Proactive message ID to consume

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConsumeNotificationOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
message_id=message_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    message_id: str,
    *,
    client: AuthenticatedClient,

) -> ConsumeNotificationOutputBody | ErrorModel | None:
    """ Consume a proactive notification

     Marks a proactive message as consumed and invalidates the agent's notification caches.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        message_id (str): Proactive message ID to consume

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConsumeNotificationOutputBody | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
message_id=message_id,
client=client,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    message_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ConsumeNotificationOutputBody | ErrorModel]:
    """ Consume a proactive notification

     Marks a proactive message as consumed and invalidates the agent's notification caches.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        message_id (str): Proactive message ID to consume

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConsumeNotificationOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
message_id=message_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    message_id: str,
    *,
    client: AuthenticatedClient,

) -> ConsumeNotificationOutputBody | ErrorModel | None:
    """ Consume a proactive notification

     Marks a proactive message as consumed and invalidates the agent's notification caches.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        message_id (str): Proactive message ID to consume

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConsumeNotificationOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
message_id=message_id,
client=client,

    )).parsed
