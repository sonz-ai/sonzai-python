from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.update_custom_tool_input_body import UpdateCustomToolInputBody
from ...models.update_custom_tool_output_body import UpdateCustomToolOutputBody
from typing import cast



def _get_kwargs(
    agent_id: str,
    tool_name: str,
    *,
    body: UpdateCustomToolInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/agents/{agent_id}/tools/{tool_name}".format(agent_id=quote(str(agent_id), safe=""),tool_name=quote(str(tool_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | UpdateCustomToolOutputBody:
    if response.status_code == 200:
        response_200 = UpdateCustomToolOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | UpdateCustomToolOutputBody]:
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
    body: UpdateCustomToolInputBody,

) -> Response[ErrorModel | UpdateCustomToolOutputBody]:
    """ Update a custom tool

     Updates a developer-defined custom tool's description and/or parameters.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        tool_name (str): Tool name to update
        body (UpdateCustomToolInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UpdateCustomToolOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
tool_name=tool_name,
body=body,

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
    body: UpdateCustomToolInputBody,

) -> ErrorModel | UpdateCustomToolOutputBody | None:
    """ Update a custom tool

     Updates a developer-defined custom tool's description and/or parameters.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        tool_name (str): Tool name to update
        body (UpdateCustomToolInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UpdateCustomToolOutputBody
     """


    return sync_detailed(
        agent_id=agent_id,
tool_name=tool_name,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    tool_name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateCustomToolInputBody,

) -> Response[ErrorModel | UpdateCustomToolOutputBody]:
    """ Update a custom tool

     Updates a developer-defined custom tool's description and/or parameters.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        tool_name (str): Tool name to update
        body (UpdateCustomToolInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UpdateCustomToolOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
tool_name=tool_name,
body=body,

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
    body: UpdateCustomToolInputBody,

) -> ErrorModel | UpdateCustomToolOutputBody | None:
    """ Update a custom tool

     Updates a developer-defined custom tool's description and/or parameters.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        tool_name (str): Tool name to update
        body (UpdateCustomToolInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UpdateCustomToolOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
tool_name=tool_name,
client=client,
body=body,

    )).parsed
