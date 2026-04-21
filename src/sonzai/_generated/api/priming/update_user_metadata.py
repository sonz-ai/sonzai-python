from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.update_metadata_request import UpdateMetadataRequest
from ...models.update_user_metadata_huma_output_body import UpdateUserMetadataHumaOutputBody
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,
    *,
    body: UpdateMetadataRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/agents/{agent_id}/users/{user_id}/metadata".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | UpdateUserMetadataHumaOutputBody:
    if response.status_code == 200:
        response_200 = UpdateUserMetadataHumaOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | UpdateUserMetadataHumaOutputBody]:
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
    body: UpdateMetadataRequest,

) -> Response[ErrorModel | UpdateUserMetadataHumaOutputBody]:
    """ Update user priming metadata

     Partially updates the structured priming metadata for a user. New facts are auto-generated from
    metadata fields. Returns the updated metadata and the number of facts created.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        body (UpdateMetadataRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UpdateUserMetadataHumaOutputBody]
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
    body: UpdateMetadataRequest,

) -> ErrorModel | UpdateUserMetadataHumaOutputBody | None:
    """ Update user priming metadata

     Partially updates the structured priming metadata for a user. New facts are auto-generated from
    metadata fields. Returns the updated metadata and the number of facts created.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        body (UpdateMetadataRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UpdateUserMetadataHumaOutputBody
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
    body: UpdateMetadataRequest,

) -> Response[ErrorModel | UpdateUserMetadataHumaOutputBody]:
    """ Update user priming metadata

     Partially updates the structured priming metadata for a user. New facts are auto-generated from
    metadata fields. Returns the updated metadata and the number of facts created.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        body (UpdateMetadataRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UpdateUserMetadataHumaOutputBody]
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
    body: UpdateMetadataRequest,

) -> ErrorModel | UpdateUserMetadataHumaOutputBody | None:
    """ Update user priming metadata

     Partially updates the structured priming metadata for a user. New facts are auto-generated from
    metadata fields. Returns the updated metadata and the number of facts created.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        body (UpdateMetadataRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UpdateUserMetadataHumaOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
body=body,

    )).parsed
