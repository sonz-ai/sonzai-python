from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.start_session_input_body import StartSessionInputBody
from ...models.start_session_output_body import StartSessionOutputBody
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: StartSessionInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/sessions/start".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | StartSessionOutputBody:
    if response.status_code == 200:
        response_200 = StartSessionOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | StartSessionOutputBody]:
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
    body: StartSessionInputBody,

) -> Response[ErrorModel | StartSessionOutputBody]:
    """ Start a chat session

     Explicitly starts a chat session. This is optional -- the `/chat` endpoint auto-creates sessions.
    Use this when you need to register custom tool definitions before the first message.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (StartSessionInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | StartSessionOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: StartSessionInputBody,

) -> ErrorModel | StartSessionOutputBody | None:
    """ Start a chat session

     Explicitly starts a chat session. This is optional -- the `/chat` endpoint auto-creates sessions.
    Use this when you need to register custom tool definitions before the first message.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (StartSessionInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | StartSessionOutputBody
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: StartSessionInputBody,

) -> Response[ErrorModel | StartSessionOutputBody]:
    """ Start a chat session

     Explicitly starts a chat session. This is optional -- the `/chat` endpoint auto-creates sessions.
    Use this when you need to register custom tool definitions before the first message.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (StartSessionInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | StartSessionOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: StartSessionInputBody,

) -> ErrorModel | StartSessionOutputBody | None:
    """ Start a chat session

     Explicitly starts a chat session. This is optional -- the `/chat` endpoint auto-creates sessions.
    Use this when you need to register custom tool definitions before the first message.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (StartSessionInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | StartSessionOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,

    )).parsed
