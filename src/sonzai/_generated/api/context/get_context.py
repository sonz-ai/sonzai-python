from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    user_id: str,
    session_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    query: str | Unset = UNSET,
    language: str | Unset = UNSET,
    timezone: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["userId"] = user_id

    params["sessionId"] = session_id

    params["instanceId"] = instance_id

    params["query"] = query

    params["language"] = language

    params["timezone"] = timezone


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/context".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


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
    user_id: str,
    session_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    query: str | Unset = UNSET,
    language: str | Unset = UNSET,
    timezone: str | Unset = UNSET,

) -> Response[Any | ErrorModel]:
    """ Get enriched agent context

     Returns the full enriched agent context built by the 7-layer context builder, including personality,
    memory, mood, relationships, knowledge base results, and more. Replaces multiple individual API
    calls with a single request.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID for per-user context scoping
        session_id (str | Unset): Session ID for memory caching
        instance_id (str | Unset): Instance scope
        query (str | Unset): Current user message for supplementary memory search
        language (str | Unset): Language code (e.g. en, ja)
        timezone (str | Unset): IANA timezone (e.g. Asia/Singapore)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
session_id=session_id,
instance_id=instance_id,
query=query,
language=language,
timezone=timezone,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str,
    session_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    query: str | Unset = UNSET,
    language: str | Unset = UNSET,
    timezone: str | Unset = UNSET,

) -> Any | ErrorModel | None:
    """ Get enriched agent context

     Returns the full enriched agent context built by the 7-layer context builder, including personality,
    memory, mood, relationships, knowledge base results, and more. Replaces multiple individual API
    calls with a single request.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID for per-user context scoping
        session_id (str | Unset): Session ID for memory caching
        instance_id (str | Unset): Instance scope
        query (str | Unset): Current user message for supplementary memory search
        language (str | Unset): Language code (e.g. en, ja)
        timezone (str | Unset): IANA timezone (e.g. Asia/Singapore)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
user_id=user_id,
session_id=session_id,
instance_id=instance_id,
query=query,
language=language,
timezone=timezone,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str,
    session_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    query: str | Unset = UNSET,
    language: str | Unset = UNSET,
    timezone: str | Unset = UNSET,

) -> Response[Any | ErrorModel]:
    """ Get enriched agent context

     Returns the full enriched agent context built by the 7-layer context builder, including personality,
    memory, mood, relationships, knowledge base results, and more. Replaces multiple individual API
    calls with a single request.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID for per-user context scoping
        session_id (str | Unset): Session ID for memory caching
        instance_id (str | Unset): Instance scope
        query (str | Unset): Current user message for supplementary memory search
        language (str | Unset): Language code (e.g. en, ja)
        timezone (str | Unset): IANA timezone (e.g. Asia/Singapore)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
session_id=session_id,
instance_id=instance_id,
query=query,
language=language,
timezone=timezone,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str,
    session_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    query: str | Unset = UNSET,
    language: str | Unset = UNSET,
    timezone: str | Unset = UNSET,

) -> Any | ErrorModel | None:
    """ Get enriched agent context

     Returns the full enriched agent context built by the 7-layer context builder, including personality,
    memory, mood, relationships, knowledge base results, and more. Replaces multiple individual API
    calls with a single request.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID for per-user context scoping
        session_id (str | Unset): Session ID for memory caching
        instance_id (str | Unset): Instance scope
        query (str | Unset): Current user message for supplementary memory search
        language (str | Unset): Language code (e.g. en, ja)
        timezone (str | Unset): IANA timezone (e.g. Asia/Singapore)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
user_id=user_id,
session_id=session_id,
instance_id=instance_id,
query=query,
language=language,
timezone=timezone,

    )).parsed
