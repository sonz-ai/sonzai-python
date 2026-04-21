from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.reset_instance_output_body import ResetInstanceOutputBody
from typing import cast



def _get_kwargs(
    agent_id: str,
    instance_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/instances/{instance_id}/reset".format(agent_id=quote(str(agent_id), safe=""),instance_id=quote(str(instance_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ResetInstanceOutputBody:
    if response.status_code == 200:
        response_200 = ResetInstanceOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ResetInstanceOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    instance_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | ResetInstanceOutputBody]:
    """ Reset an instance

     Resets all memory data (facts, nodes) for an agent instance via the context engine, then restores
    the instance to active status.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str): Instance UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ResetInstanceOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
instance_id=instance_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    instance_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | ResetInstanceOutputBody | None:
    """ Reset an instance

     Resets all memory data (facts, nodes) for an agent instance via the context engine, then restores
    the instance to active status.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str): Instance UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ResetInstanceOutputBody
     """


    return sync_detailed(
        agent_id=agent_id,
instance_id=instance_id,
client=client,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    instance_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | ResetInstanceOutputBody]:
    """ Reset an instance

     Resets all memory data (facts, nodes) for an agent instance via the context engine, then restores
    the instance to active status.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str): Instance UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ResetInstanceOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
instance_id=instance_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    instance_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | ResetInstanceOutputBody | None:
    """ Reset an instance

     Resets all memory data (facts, nodes) for an agent instance via the context engine, then restores
    the instance to active status.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str): Instance UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ResetInstanceOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
instance_id=instance_id,
client=client,

    )).parsed
