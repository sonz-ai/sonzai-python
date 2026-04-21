from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.user_priming_metadata import UserPrimingMetadata
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/users/{user_id}/metadata".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | UserPrimingMetadata:
    if response.status_code == 200:
        response_200 = UserPrimingMetadata.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | UserPrimingMetadata]:
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

) -> Response[ErrorModel | UserPrimingMetadata]:
    """ Get user priming metadata

     Returns the structured priming metadata (display name, company, email, custom fields, etc.) for a
    user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UserPrimingMetadata]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,

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

) -> ErrorModel | UserPrimingMetadata | None:
    """ Get user priming metadata

     Returns the structured priming metadata (display name, company, email, custom fields, etc.) for a
    user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UserPrimingMetadata
     """


    return sync_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | UserPrimingMetadata]:
    """ Get user priming metadata

     Returns the structured priming metadata (display name, company, email, custom fields, etc.) for a
    user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UserPrimingMetadata]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,

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

) -> ErrorModel | UserPrimingMetadata | None:
    """ Get user priming metadata

     Returns the structured priming metadata (display name, company, email, custom fields, etc.) for a
    user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UserPrimingMetadata
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,

    )).parsed
