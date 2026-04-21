from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.users_response import UsersResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["sort_by"] = sort_by

    params["sort_order"] = sort_order


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/users".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | UsersResponse:
    if response.status_code == 200:
        response_200 = UsersResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | UsersResponse]:
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
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,

) -> Response[ErrorModel | UsersResponse]:
    """ List users for an agent

     Returns all users associated with an agent, including mood and priming metadata. Supports
    pagination, sorting, and custom field filtering via `custom.<key>` query params.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max users per page (default 100, max 500) Default: 100.
        offset (int | Unset): Pagination offset Default: 0.
        sort_by (str | Unset): Sort field (display_name, last_interaction, created_at, user_id, or
            custom.<key>)
        sort_order (str | Unset): Sort order: asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UsersResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
limit=limit,
offset=offset,
sort_by=sort_by,
sort_order=sort_order,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,

) -> ErrorModel | UsersResponse | None:
    """ List users for an agent

     Returns all users associated with an agent, including mood and priming metadata. Supports
    pagination, sorting, and custom field filtering via `custom.<key>` query params.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max users per page (default 100, max 500) Default: 100.
        offset (int | Unset): Pagination offset Default: 0.
        sort_by (str | Unset): Sort field (display_name, last_interaction, created_at, user_id, or
            custom.<key>)
        sort_order (str | Unset): Sort order: asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UsersResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
limit=limit,
offset=offset,
sort_by=sort_by,
sort_order=sort_order,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,

) -> Response[ErrorModel | UsersResponse]:
    """ List users for an agent

     Returns all users associated with an agent, including mood and priming metadata. Supports
    pagination, sorting, and custom field filtering via `custom.<key>` query params.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max users per page (default 100, max 500) Default: 100.
        offset (int | Unset): Pagination offset Default: 0.
        sort_by (str | Unset): Sort field (display_name, last_interaction, created_at, user_id, or
            custom.<key>)
        sort_order (str | Unset): Sort order: asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UsersResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
limit=limit,
offset=offset,
sort_by=sort_by,
sort_order=sort_order,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort_by: str | Unset = UNSET,
    sort_order: str | Unset = UNSET,

) -> ErrorModel | UsersResponse | None:
    """ List users for an agent

     Returns all users associated with an agent, including mood and priming metadata. Supports
    pagination, sorting, and custom field filtering via `custom.<key>` query params.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max users per page (default 100, max 500) Default: 100.
        offset (int | Unset): Pagination offset Default: 0.
        sort_by (str | Unset): Sort field (display_name, last_interaction, created_at, user_id, or
            custom.<key>)
        sort_order (str | Unset): Sort order: asc or desc

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UsersResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
limit=limit,
offset=offset,
sort_by=sort_by,
sort_order=sort_order,

    )).parsed
