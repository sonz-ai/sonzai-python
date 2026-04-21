from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.get_tool_schemas_output_body import GetToolSchemasOutputBody
from typing import cast



def _get_kwargs(
    agent_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/tools/schemas".format(agent_id=quote(str(agent_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | GetToolSchemasOutputBody:
    if response.status_code == 200:
        response_200 = GetToolSchemasOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | GetToolSchemasOutputBody]:
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

) -> Response[ErrorModel | GetToolSchemasOutputBody]:
    """ Get available tool schemas

     Returns JSON tool definitions that BYO-LLM integrations can add to their LLM's tool calling config.
    This is the tool catalog for external agent frameworks.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | GetToolSchemasOutputBody]
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

) -> ErrorModel | GetToolSchemasOutputBody | None:
    """ Get available tool schemas

     Returns JSON tool definitions that BYO-LLM integrations can add to their LLM's tool calling config.
    This is the tool catalog for external agent frameworks.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | GetToolSchemasOutputBody
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | GetToolSchemasOutputBody]:
    """ Get available tool schemas

     Returns JSON tool definitions that BYO-LLM integrations can add to their LLM's tool calling config.
    This is the tool catalog for external agent frameworks.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | GetToolSchemasOutputBody]
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

) -> ErrorModel | GetToolSchemasOutputBody | None:
    """ Get available tool schemas

     Returns JSON tool definitions that BYO-LLM integrations can add to their LLM's tool calling config.
    This is the tool catalog for external agent frameworks.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | GetToolSchemasOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,

    )).parsed
