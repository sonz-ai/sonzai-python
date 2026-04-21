from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.speech_to_text_input_body import SpeechToTextInputBody
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: SpeechToTextInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/voice/stt".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorModel:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorModel]:
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
    body: SpeechToTextInputBody,

) -> Response[Any | ErrorModel]:
    """ Convert speech to text

     Proxies to the AI service for one-shot speech-to-text conversion. Audio is sent as base64-encoded
    JSON, not multipart. Returns the AI service JSON response containing transcription and usage info.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (SpeechToTextInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
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
    body: SpeechToTextInputBody,

) -> Any | ErrorModel | None:
    """ Convert speech to text

     Proxies to the AI service for one-shot speech-to-text conversion. Audio is sent as base64-encoded
    JSON, not multipart. Returns the AI service JSON response containing transcription and usage info.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (SpeechToTextInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
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
    body: SpeechToTextInputBody,

) -> Response[Any | ErrorModel]:
    """ Convert speech to text

     Proxies to the AI service for one-shot speech-to-text conversion. Audio is sent as base64-encoded
    JSON, not multipart. Returns the AI service JSON response containing transcription and usage info.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (SpeechToTextInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
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
    body: SpeechToTextInputBody,

) -> Any | ErrorModel | None:
    """ Convert speech to text

     Proxies to the AI service for one-shot speech-to-text conversion. Audio is sent as base64-encoded
    JSON, not multipart. Returns the AI service JSON response containing transcription and usage info.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (SpeechToTextInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,

    )).parsed
