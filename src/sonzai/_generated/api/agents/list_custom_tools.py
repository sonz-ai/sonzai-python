from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.list_custom_tools_output_body import ListCustomToolsOutputBody
from typing import cast



def _get_kwargs(
    agent_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/tools".format(agent_id=quote(str(agent_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ListCustomToolsOutputBody:
    if response.status_code == 200:
        response_200 = ListCustomToolsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ListCustomToolsOutputBody]:
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

) -> Response[ErrorModel | ListCustomToolsOutputBody]:
    """ List custom tools

     Returns the developer-defined custom tools for an agent.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListCustomToolsOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | ListCustomToolsOutputBody | None:
    """ List custom tools

     Returns the developer-defined custom tools for an agent.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListCustomToolsOutputBody
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | ListCustomToolsOutputBody]:
    """ List custom tools

     Returns the developer-defined custom tools for an agent.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListCustomToolsOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | ListCustomToolsOutputBody | None:
    """ List custom tools

     Returns the developer-defined custom tools for an agent.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListCustomToolsOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,

    )).parsed
