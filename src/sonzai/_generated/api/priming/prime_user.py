from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.prime_user_request import PrimeUserRequest
from ...models.prime_user_response_200 import PrimeUserResponse200
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,
    *,
    body: PrimeUserRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/users/{user_id}/prime".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | PrimeUserResponse200:
    if response.status_code == 200:
        response_200 = PrimeUserResponse200.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | PrimeUserResponse200]:
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
    body: PrimeUserRequest,

) -> Response[ErrorModel | PrimeUserResponse200]:
    """ Prime a user with external data

     Accepts raw data from CRM, LinkedIn, scrapers etc. so the AI agent already 'knows' the user. Returns
    a job ID for async tracking. Metadata facts are generated synchronously; content extraction happens
    asynchronously via NATS.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID to prime
        body (PrimeUserRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | PrimeUserResponse200]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
body=body,

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
    body: PrimeUserRequest,

) -> ErrorModel | PrimeUserResponse200 | None:
    """ Prime a user with external data

     Accepts raw data from CRM, LinkedIn, scrapers etc. so the AI agent already 'knows' the user. Returns
    a job ID for async tracking. Metadata facts are generated synchronously; content extraction happens
    asynchronously via NATS.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID to prime
        body (PrimeUserRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | PrimeUserResponse200
     """


    return sync_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: PrimeUserRequest,

) -> Response[ErrorModel | PrimeUserResponse200]:
    """ Prime a user with external data

     Accepts raw data from CRM, LinkedIn, scrapers etc. so the AI agent already 'knows' the user. Returns
    a job ID for async tracking. Metadata facts are generated synchronously; content extraction happens
    asynchronously via NATS.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID to prime
        body (PrimeUserRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | PrimeUserResponse200]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
body=body,

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
    body: PrimeUserRequest,

) -> ErrorModel | PrimeUserResponse200 | None:
    """ Prime a user with external data

     Accepts raw data from CRM, LinkedIn, scrapers etc. so the AI agent already 'knows' the user. Returns
    a job ID for async tracking. Metadata facts are generated synchronously; content extraction happens
    asynchronously via NATS.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID to prime
        body (PrimeUserRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | PrimeUserResponse200
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
body=body,

    )).parsed
