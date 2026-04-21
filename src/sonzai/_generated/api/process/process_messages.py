from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.process_input_body import ProcessInputBody
from ...models.process_response import ProcessResponse
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: ProcessInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/process".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ProcessResponse:
    if response.status_code == 200:
        response_200 = ProcessResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ProcessResponse]:
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
    body: ProcessInputBody,

) -> Response[ErrorModel | ProcessResponse]:
    """ Process an external conversation transcript

     Runs the full Context Engine pipeline (behavioral side effects, fact extraction, memory storage,
    diary, knowledge gap detection) on a conversation transcript produced by an external LLM. Requires
    at least 2 messages.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (ProcessInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ProcessResponse]
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
    body: ProcessInputBody,

) -> ErrorModel | ProcessResponse | None:
    """ Process an external conversation transcript

     Runs the full Context Engine pipeline (behavioral side effects, fact extraction, memory storage,
    diary, knowledge gap detection) on a conversation transcript produced by an external LLM. Requires
    at least 2 messages.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (ProcessInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ProcessResponse
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
    body: ProcessInputBody,

) -> Response[ErrorModel | ProcessResponse]:
    """ Process an external conversation transcript

     Runs the full Context Engine pipeline (behavioral side effects, fact extraction, memory storage,
    diary, knowledge gap detection) on a conversation transcript produced by an external LLM. Requires
    at least 2 messages.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (ProcessInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ProcessResponse]
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
    body: ProcessInputBody,

) -> ErrorModel | ProcessResponse | None:
    """ Process an external conversation transcript

     Runs the full Context Engine pipeline (behavioral side effects, fact extraction, memory storage,
    diary, knowledge gap detection) on a conversation transcript produced by an external LLM. Requires
    at least 2 messages.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (ProcessInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ProcessResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,

    )).parsed
