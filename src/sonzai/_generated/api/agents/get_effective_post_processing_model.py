from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.effective_post_processing_model_output_body import EffectivePostProcessingModelOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    chat_model: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["chat_model"] = chat_model


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/effective-post-processing-model".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> EffectivePostProcessingModelOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = EffectivePostProcessingModelOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[EffectivePostProcessingModelOutputBody | ErrorModel]:
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
    chat_model: str,

) -> Response[EffectivePostProcessingModelOutputBody | ErrorModel]:
    """ Preview the resolved post-processing model for this agent

     Runs the cascade resolver server-side without firing any inference. When
    ENABLE_POST_PROCESSING_MODEL_MAP is off, returns the chat model itself (matches runtime behaviour on
    disabled deployments).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        chat_model (str): The chat model whose post-processing routing should be previewed

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EffectivePostProcessingModelOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
chat_model=chat_model,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    chat_model: str,

) -> EffectivePostProcessingModelOutputBody | ErrorModel | None:
    """ Preview the resolved post-processing model for this agent

     Runs the cascade resolver server-side without firing any inference. When
    ENABLE_POST_PROCESSING_MODEL_MAP is off, returns the chat model itself (matches runtime behaviour on
    disabled deployments).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        chat_model (str): The chat model whose post-processing routing should be previewed

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EffectivePostProcessingModelOutputBody | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
chat_model=chat_model,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    chat_model: str,

) -> Response[EffectivePostProcessingModelOutputBody | ErrorModel]:
    """ Preview the resolved post-processing model for this agent

     Runs the cascade resolver server-side without firing any inference. When
    ENABLE_POST_PROCESSING_MODEL_MAP is off, returns the chat model itself (matches runtime behaviour on
    disabled deployments).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        chat_model (str): The chat model whose post-processing routing should be previewed

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EffectivePostProcessingModelOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
chat_model=chat_model,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    chat_model: str,

) -> EffectivePostProcessingModelOutputBody | ErrorModel | None:
    """ Preview the resolved post-processing model for this agent

     Runs the cascade resolver server-side without firing any inference. When
    ENABLE_POST_PROCESSING_MODEL_MAP is off, returns the chat model itself (matches runtime behaviour on
    disabled deployments).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        chat_model (str): The chat model whose post-processing routing should be previewed

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EffectivePostProcessingModelOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
chat_model=chat_model,

    )).parsed
