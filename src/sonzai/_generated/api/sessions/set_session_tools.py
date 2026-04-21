from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.session_tool_def import SessionToolDef
from ...models.set_session_tools_output_body import SetSessionToolsOutputBody
from typing import cast



def _get_kwargs(
    agent_id: str,
    session_id: str,
    *,
    body: list[SessionToolDef] | None,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/agents/{agent_id}/sessions/{session_id}/tools".format(agent_id=quote(str(agent_id), safe=""),session_id=quote(str(session_id), safe=""),),
    }

    
    if isinstance(body, list):
        _kwargs["json"] = []
        for body_type_0_item_data in body:
            body_type_0_item = body_type_0_item_data.to_dict()
            _kwargs["json"].append(body_type_0_item)


    else:
        _kwargs["json"] = body


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | SetSessionToolsOutputBody:
    if response.status_code == 200:
        response_200 = SetSessionToolsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | SetSessionToolsOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: list[SessionToolDef] | None,

) -> Response[ErrorModel | SetSessionToolsOutputBody]:
    """ Set session tool definitions

     Registers custom tool definitions for an existing session. Tools persist for the session lifetime
    and are merged with character-level tools on every AI request. Tool names starting with `sonzai_`
    are reserved. The request body must be a JSON array of tool definitions.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        session_id (str): Session identifier
        body (list[SessionToolDef] | None): JSON array of tool definitions

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SetSessionToolsOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
session_id=session_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: list[SessionToolDef] | None,

) -> ErrorModel | SetSessionToolsOutputBody | None:
    """ Set session tool definitions

     Registers custom tool definitions for an existing session. Tools persist for the session lifetime
    and are merged with character-level tools on every AI request. Tool names starting with `sonzai_`
    are reserved. The request body must be a JSON array of tool definitions.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        session_id (str): Session identifier
        body (list[SessionToolDef] | None): JSON array of tool definitions

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SetSessionToolsOutputBody
     """


    return sync_detailed(
        agent_id=agent_id,
session_id=session_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: list[SessionToolDef] | None,

) -> Response[ErrorModel | SetSessionToolsOutputBody]:
    """ Set session tool definitions

     Registers custom tool definitions for an existing session. Tools persist for the session lifetime
    and are merged with character-level tools on every AI request. Tool names starting with `sonzai_`
    are reserved. The request body must be a JSON array of tool definitions.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        session_id (str): Session identifier
        body (list[SessionToolDef] | None): JSON array of tool definitions

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SetSessionToolsOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
session_id=session_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
    body: list[SessionToolDef] | None,

) -> ErrorModel | SetSessionToolsOutputBody | None:
    """ Set session tool definitions

     Registers custom tool definitions for an existing session. Tools persist for the session lifetime
    and are merged with character-level tools on every AI request. Tool names starting with `sonzai_`
    are reserved. The request body must be a JSON array of tool definitions.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        session_id (str): Session identifier
        body (list[SessionToolDef] | None): JSON array of tool definitions

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SetSessionToolsOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
session_id=session_id,
client=client,
body=body,

    )).parsed
