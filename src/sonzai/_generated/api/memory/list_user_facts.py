from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.list_all_facts_response import ListAllFactsResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,
    *,
    instance_id: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    has_metadata: str | Unset = UNSET,
    metadata_item_type: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["instance_id"] = instance_id

    params["limit"] = limit

    params["has_metadata"] = has_metadata

    params["metadata.item_type"] = metadata_item_type


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/users/{user_id}/facts".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ListAllFactsResponse:
    if response.status_code == 200:
        response_200 = ListAllFactsResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ListAllFactsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    has_metadata: str | Unset = UNSET,
    metadata_item_type: str | Unset = UNSET,

) -> Response[ErrorModel | ListAllFactsResponse]:
    """ List all active facts for a specific user

     Returns active (non-superseded) facts for an agent-user pair. Supports metadata filtering.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User identifier
        instance_id (str | Unset): Optional instance ID for scoping
        limit (str | Unset): Max facts to return (default 1000, max 5000)
        has_metadata (str | Unset): Set to 'true' to only return facts with metadata
        metadata_item_type (str | Unset): Filter by metadata.item_type value

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListAllFactsResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,
limit=limit,
has_metadata=has_metadata,
metadata_item_type=metadata_item_type,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    has_metadata: str | Unset = UNSET,
    metadata_item_type: str | Unset = UNSET,

) -> ErrorModel | ListAllFactsResponse | None:
    """ List all active facts for a specific user

     Returns active (non-superseded) facts for an agent-user pair. Supports metadata filtering.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User identifier
        instance_id (str | Unset): Optional instance ID for scoping
        limit (str | Unset): Max facts to return (default 1000, max 5000)
        has_metadata (str | Unset): Set to 'true' to only return facts with metadata
        metadata_item_type (str | Unset): Filter by metadata.item_type value

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListAllFactsResponse
     """


    return sync_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
instance_id=instance_id,
limit=limit,
has_metadata=has_metadata,
metadata_item_type=metadata_item_type,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    has_metadata: str | Unset = UNSET,
    metadata_item_type: str | Unset = UNSET,

) -> Response[ErrorModel | ListAllFactsResponse]:
    """ List all active facts for a specific user

     Returns active (non-superseded) facts for an agent-user pair. Supports metadata filtering.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User identifier
        instance_id (str | Unset): Optional instance ID for scoping
        limit (str | Unset): Max facts to return (default 1000, max 5000)
        has_metadata (str | Unset): Set to 'true' to only return facts with metadata
        metadata_item_type (str | Unset): Filter by metadata.item_type value

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListAllFactsResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,
limit=limit,
has_metadata=has_metadata,
metadata_item_type=metadata_item_type,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    instance_id: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    has_metadata: str | Unset = UNSET,
    metadata_item_type: str | Unset = UNSET,

) -> ErrorModel | ListAllFactsResponse | None:
    """ List all active facts for a specific user

     Returns active (non-superseded) facts for an agent-user pair. Supports metadata filtering.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User identifier
        instance_id (str | Unset): Optional instance ID for scoping
        limit (str | Unset): Max facts to return (default 1000, max 5000)
        has_metadata (str | Unset): Set to 'true' to only return facts with metadata
        metadata_item_type (str | Unset): Filter by metadata.item_type value

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListAllFactsResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
instance_id=instance_id,
limit=limit,
has_metadata=has_metadata,
metadata_item_type=metadata_item_type,

    )).parsed
