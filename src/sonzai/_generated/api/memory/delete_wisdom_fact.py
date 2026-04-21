from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_wisdom_response import DeleteWisdomResponse
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    agent_id: str,
    fact_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/agents/{agent_id}/memory/wisdom/{fact_id}".format(agent_id=quote(str(agent_id), safe=""),fact_id=quote(str(fact_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteWisdomResponse | ErrorModel:
    if response.status_code == 200:
        response_200 = DeleteWisdomResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteWisdomResponse | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    fact_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteWisdomResponse | ErrorModel]:
    """ Delete a wisdom fact

     Deletes a wisdom fact from the agent-global partition. Only operates on agent-global wisdom facts;
    per-user fact IDs return 404.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        fact_id (str): Wisdom fact identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteWisdomResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
fact_id=fact_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    fact_id: str,
    *,
    client: AuthenticatedClient,

) -> DeleteWisdomResponse | ErrorModel | None:
    """ Delete a wisdom fact

     Deletes a wisdom fact from the agent-global partition. Only operates on agent-global wisdom facts;
    per-user fact IDs return 404.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        fact_id (str): Wisdom fact identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteWisdomResponse | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
fact_id=fact_id,
client=client,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    fact_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteWisdomResponse | ErrorModel]:
    """ Delete a wisdom fact

     Deletes a wisdom fact from the agent-global partition. Only operates on agent-global wisdom facts;
    per-user fact IDs return 404.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        fact_id (str): Wisdom fact identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteWisdomResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
fact_id=fact_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    fact_id: str,
    *,
    client: AuthenticatedClient,

) -> DeleteWisdomResponse | ErrorModel | None:
    """ Delete a wisdom fact

     Deletes a wisdom fact from the agent-global partition. Only operates on agent-global wisdom facts;
    per-user fact IDs return 404.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        fact_id (str): Wisdom fact identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteWisdomResponse | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
fact_id=fact_id,
client=client,

    )).parsed
