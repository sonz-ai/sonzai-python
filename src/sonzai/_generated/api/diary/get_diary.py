from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.diary_polymorphic_response import DiaryPolymorphicResponse
from ...models.error_model import ErrorModel
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    date: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["date"] = date

    params["limit"] = limit

    params["user_id"] = user_id

    params["instance_id"] = instance_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/diary".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DiaryPolymorphicResponse | ErrorModel:
    if response.status_code == 200:
        response_200 = DiaryPolymorphicResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DiaryPolymorphicResponse | ErrorModel]:
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
    date: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,

) -> Response[DiaryPolymorphicResponse | ErrorModel]:
    """ Get diary entries for an agent

     Returns diary entries. When `date` is specified, returns a single entry for that date (in `entry`
    field). Otherwise returns the most recent entries up to `limit` (in `entries` field). Optionally
    scoped by `user_id` and `instance_id`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        date (str | Unset): Fetch a single entry by date (YYYY-MM-DD). Mutually exclusive with
            limit.
        limit (str | Unset): Maximum number of recent entries to return (default 30, max 100)
        user_id (str | Unset): Optional user ID to filter entries
        instance_id (str | Unset): Optional instance ID for scoping

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DiaryPolymorphicResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
date=date,
limit=limit,
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
    date: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,

) -> DiaryPolymorphicResponse | ErrorModel | None:
    """ Get diary entries for an agent

     Returns diary entries. When `date` is specified, returns a single entry for that date (in `entry`
    field). Otherwise returns the most recent entries up to `limit` (in `entries` field). Optionally
    scoped by `user_id` and `instance_id`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        date (str | Unset): Fetch a single entry by date (YYYY-MM-DD). Mutually exclusive with
            limit.
        limit (str | Unset): Maximum number of recent entries to return (default 30, max 100)
        user_id (str | Unset): Optional user ID to filter entries
        instance_id (str | Unset): Optional instance ID for scoping

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DiaryPolymorphicResponse | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
date=date,
limit=limit,
user_id=user_id,
instance_id=instance_id,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    date: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,

) -> Response[DiaryPolymorphicResponse | ErrorModel]:
    """ Get diary entries for an agent

     Returns diary entries. When `date` is specified, returns a single entry for that date (in `entry`
    field). Otherwise returns the most recent entries up to `limit` (in `entries` field). Optionally
    scoped by `user_id` and `instance_id`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        date (str | Unset): Fetch a single entry by date (YYYY-MM-DD). Mutually exclusive with
            limit.
        limit (str | Unset): Maximum number of recent entries to return (default 30, max 100)
        user_id (str | Unset): Optional user ID to filter entries
        instance_id (str | Unset): Optional instance ID for scoping

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DiaryPolymorphicResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
date=date,
limit=limit,
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
    date: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,

) -> DiaryPolymorphicResponse | ErrorModel | None:
    """ Get diary entries for an agent

     Returns diary entries. When `date` is specified, returns a single entry for that date (in `entry`
    field). Otherwise returns the most recent entries up to `limit` (in `entries` field). Optionally
    scoped by `user_id` and `instance_id`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        date (str | Unset): Fetch a single entry by date (YYYY-MM-DD). Mutually exclusive with
            limit.
        limit (str | Unset): Maximum number of recent entries to return (default 30, max 100)
        user_id (str | Unset): Optional user ID to filter entries
        instance_id (str | Unset): Optional instance ID for scoping

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DiaryPolymorphicResponse | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
date=date,
limit=limit,
user_id=user_id,
instance_id=instance_id,

    )).parsed
