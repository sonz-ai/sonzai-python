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
    key: str,
    scope: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["key"] = key

    params["scope"] = scope

    params["user_id"] = user_id

    params["instance_id"] = instance_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/agents/{agent_id}/custom-states/by-key".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorModel:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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
    key: str,
    scope: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,

) -> Response[Any | ErrorModel]:
    """ Delete a custom state by key

     Deletes a custom state by its composite key (agent_id, instance_id, scope, user_id, key).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        key (str): State key to delete
        scope (str | Unset): Scope (global or user, defaults to global)
        user_id (str | Unset): User ID for user-scoped states
        instance_id (str | Unset): Instance ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
key=key,
scope=scope,
user_id=user_id,
instance_id=instance_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    key: str,
    scope: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,

) -> Any | ErrorModel | None:
    """ Delete a custom state by key

     Deletes a custom state by its composite key (agent_id, instance_id, scope, user_id, key).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        key (str): State key to delete
        scope (str | Unset): Scope (global or user, defaults to global)
        user_id (str | Unset): User ID for user-scoped states
        instance_id (str | Unset): Instance ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
key=key,
scope=scope,
user_id=user_id,
instance_id=instance_id,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    key: str,
    scope: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,

) -> Response[Any | ErrorModel]:
    """ Delete a custom state by key

     Deletes a custom state by its composite key (agent_id, instance_id, scope, user_id, key).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        key (str): State key to delete
        scope (str | Unset): Scope (global or user, defaults to global)
        user_id (str | Unset): User ID for user-scoped states
        instance_id (str | Unset): Instance ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
key=key,
scope=scope,
user_id=user_id,
instance_id=instance_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    key: str,
    scope: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,

) -> Any | ErrorModel | None:
    """ Delete a custom state by key

     Deletes a custom state by its composite key (agent_id, instance_id, scope, user_id, key).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        key (str): State key to delete
        scope (str | Unset): Scope (global or user, defaults to global)
        user_id (str | Unset): User ID for user-scoped states
        instance_id (str | Unset): Instance ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
key=key,
scope=scope,
user_id=user_id,
instance_id=instance_id,

    )).parsed
