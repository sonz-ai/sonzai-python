from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.fact_history_response import FactHistoryResponse
from typing import cast



def _get_kwargs(
    agent_id: str,
    fact_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/memory/fact/{fact_id}/history".format(agent_id=quote(str(agent_id), safe=""),fact_id=quote(str(fact_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | FactHistoryResponse:
    if response.status_code == 200:
        response_200 = FactHistoryResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | FactHistoryResponse]:
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

) -> Response[ErrorModel | FactHistoryResponse]:
    """ Get fact supersedes history

     Walks the supersedes chain backward from the current fact to return all previous versions.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        fact_id (str): Fact identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | FactHistoryResponse]
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

) -> ErrorModel | FactHistoryResponse | None:
    """ Get fact supersedes history

     Walks the supersedes chain backward from the current fact to return all previous versions.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        fact_id (str): Fact identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | FactHistoryResponse
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

) -> Response[ErrorModel | FactHistoryResponse]:
    """ Get fact supersedes history

     Walks the supersedes chain backward from the current fact to return all previous versions.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        fact_id (str): Fact identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | FactHistoryResponse]
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

) -> ErrorModel | FactHistoryResponse | None:
    """ Get fact supersedes history

     Walks the supersedes chain backward from the current fact to return all previous versions.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        fact_id (str): Fact identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | FactHistoryResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
fact_id=fact_id,
client=client,

    )).parsed
