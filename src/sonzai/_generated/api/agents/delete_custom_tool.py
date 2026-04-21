from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_custom_tool_output_body import DeleteCustomToolOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    agent_id: str,
    tool_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/agents/{agent_id}/tools/{tool_name}".format(agent_id=quote(str(agent_id), safe=""),tool_name=quote(str(tool_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteCustomToolOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = DeleteCustomToolOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteCustomToolOutputBody | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    tool_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteCustomToolOutputBody | ErrorModel]:
    """ Delete a custom tool

     Removes a developer-defined custom tool. Sonzai platform tools (prefixed sonzai_) cannot be deleted.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        tool_name (str): Tool name to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteCustomToolOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
tool_name=tool_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    tool_name: str,
    *,
    client: AuthenticatedClient,

) -> DeleteCustomToolOutputBody | ErrorModel | None:
    """ Delete a custom tool

     Removes a developer-defined custom tool. Sonzai platform tools (prefixed sonzai_) cannot be deleted.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        tool_name (str): Tool name to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteCustomToolOutputBody | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
tool_name=tool_name,
client=client,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    tool_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteCustomToolOutputBody | ErrorModel]:
    """ Delete a custom tool

     Removes a developer-defined custom tool. Sonzai platform tools (prefixed sonzai_) cannot be deleted.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        tool_name (str): Tool name to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteCustomToolOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
tool_name=tool_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    tool_name: str,
    *,
    client: AuthenticatedClient,

) -> DeleteCustomToolOutputBody | ErrorModel | None:
    """ Delete a custom tool

     Removes a developer-defined custom tool. Sonzai platform tools (prefixed sonzai_) cannot be deleted.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        tool_name (str): Tool name to delete

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteCustomToolOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
tool_name=tool_name,
client=client,

    )).parsed
