from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.voice_live_ws_token_input_body import VoiceLiveWSTokenInputBody
from ...models.voice_live_ws_token_output_body import VoiceLiveWSTokenOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: VoiceLiveWSTokenInputBody,
    host: str | Unset = UNSET,
    x_forwarded_proto: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(host, Unset):
        headers["Host"] = host

    if not isinstance(x_forwarded_proto, Unset):
        headers["X-Forwarded-Proto"] = x_forwarded_proto



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/voice/live-ws-token".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | VoiceLiveWSTokenOutputBody:
    if response.status_code == 200:
        response_200 = VoiceLiveWSTokenOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | VoiceLiveWSTokenOutputBody]:
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
    body: VoiceLiveWSTokenInputBody,
    host: str | Unset = UNSET,
    x_forwarded_proto: str | Unset = UNSET,

) -> Response[ErrorModel | VoiceLiveWSTokenOutputBody]:
    """ Get a voice live WebSocket token

     Issues a short-lived token for duplex voice live WebSocket connections. The returned `wsUrl` and
    `authToken` are used to connect to the `/ws/voice/live` endpoint. This endpoint does NOT require
    agent authorization (supports PocketSouls agents in ScyllaDB only).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        host (str | Unset): Request host (used to build WebSocket URL)
        x_forwarded_proto (str | Unset): Forwarded protocol (http/https)
        body (VoiceLiveWSTokenInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | VoiceLiveWSTokenOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,
host=host,
x_forwarded_proto=x_forwarded_proto,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: VoiceLiveWSTokenInputBody,
    host: str | Unset = UNSET,
    x_forwarded_proto: str | Unset = UNSET,

) -> ErrorModel | VoiceLiveWSTokenOutputBody | None:
    """ Get a voice live WebSocket token

     Issues a short-lived token for duplex voice live WebSocket connections. The returned `wsUrl` and
    `authToken` are used to connect to the `/ws/voice/live` endpoint. This endpoint does NOT require
    agent authorization (supports PocketSouls agents in ScyllaDB only).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        host (str | Unset): Request host (used to build WebSocket URL)
        x_forwarded_proto (str | Unset): Forwarded protocol (http/https)
        body (VoiceLiveWSTokenInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | VoiceLiveWSTokenOutputBody
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
body=body,
host=host,
x_forwarded_proto=x_forwarded_proto,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: VoiceLiveWSTokenInputBody,
    host: str | Unset = UNSET,
    x_forwarded_proto: str | Unset = UNSET,

) -> Response[ErrorModel | VoiceLiveWSTokenOutputBody]:
    """ Get a voice live WebSocket token

     Issues a short-lived token for duplex voice live WebSocket connections. The returned `wsUrl` and
    `authToken` are used to connect to the `/ws/voice/live` endpoint. This endpoint does NOT require
    agent authorization (supports PocketSouls agents in ScyllaDB only).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        host (str | Unset): Request host (used to build WebSocket URL)
        x_forwarded_proto (str | Unset): Forwarded protocol (http/https)
        body (VoiceLiveWSTokenInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | VoiceLiveWSTokenOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,
host=host,
x_forwarded_proto=x_forwarded_proto,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: VoiceLiveWSTokenInputBody,
    host: str | Unset = UNSET,
    x_forwarded_proto: str | Unset = UNSET,

) -> ErrorModel | VoiceLiveWSTokenOutputBody | None:
    """ Get a voice live WebSocket token

     Issues a short-lived token for duplex voice live WebSocket connections. The returned `wsUrl` and
    `authToken` are used to connect to the `/ws/voice/live` endpoint. This endpoint does NOT require
    agent authorization (supports PocketSouls agents in ScyllaDB only).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        host (str | Unset): Request host (used to build WebSocket URL)
        x_forwarded_proto (str | Unset): Forwarded protocol (http/https)
        body (VoiceLiveWSTokenInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | VoiceLiveWSTokenOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,
host=host,
x_forwarded_proto=x_forwarded_proto,

    )).parsed
