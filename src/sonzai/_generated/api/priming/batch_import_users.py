from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.batch_import_request import BatchImportRequest
from ...models.batch_import_users_huma_output_body import BatchImportUsersHumaOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: BatchImportRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/users/import".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> BatchImportUsersHumaOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = BatchImportUsersHumaOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[BatchImportUsersHumaOutputBody | ErrorModel]:
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
    body: BatchImportRequest,

) -> Response[BatchImportUsersHumaOutputBody | ErrorModel]:
    """ Batch import users

     Imports multiple users in a single request, initializing memory trees, granting access, storing
    metadata, and generating facts. Content extraction happens asynchronously via NATS.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (BatchImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchImportUsersHumaOutputBody | ErrorModel]
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
    body: BatchImportRequest,

) -> BatchImportUsersHumaOutputBody | ErrorModel | None:
    """ Batch import users

     Imports multiple users in a single request, initializing memory trees, granting access, storing
    metadata, and generating facts. Content extraction happens asynchronously via NATS.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (BatchImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchImportUsersHumaOutputBody | ErrorModel
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
    body: BatchImportRequest,

) -> Response[BatchImportUsersHumaOutputBody | ErrorModel]:
    """ Batch import users

     Imports multiple users in a single request, initializing memory trees, granting access, storing
    metadata, and generating facts. Content extraction happens asynchronously via NATS.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (BatchImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchImportUsersHumaOutputBody | ErrorModel]
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
    body: BatchImportRequest,

) -> BatchImportUsersHumaOutputBody | ErrorModel | None:
    """ Batch import users

     Imports multiple users in a single request, initializing memory trees, granting access, storing
    metadata, and generating facts. Content extraction happens asynchronously via NATS.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (BatchImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchImportUsersHumaOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,

    )).parsed
