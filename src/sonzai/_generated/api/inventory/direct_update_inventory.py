from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.direct_update_request import DirectUpdateRequest
from ...models.direct_update_response import DirectUpdateResponse
from ...models.error_model import ErrorModel
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,
    fact_id: str,
    *,
    body: DirectUpdateRequest,
    instance_id: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["instance_id"] = instance_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/agents/{agent_id}/users/{user_id}/inventory/{fact_id}".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),fact_id=quote(str(fact_id), safe=""),),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DirectUpdateResponse | ErrorModel:
    if response.status_code == 200:
        response_200 = DirectUpdateResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DirectUpdateResponse | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    user_id: str,
    fact_id: str,
    *,
    client: AuthenticatedClient,
    body: DirectUpdateRequest,
    instance_id: str | Unset = UNSET,

) -> Response[DirectUpdateResponse | ErrorModel]:
    """ Update a specific inventory fact

     Updates a specific inventory item by fact ID, merging new properties into the existing metadata.
    Creates a superseding fact.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        fact_id (str): Inventory fact UUID
        instance_id (str | Unset): Optional instance ID for user scoping
        body (DirectUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DirectUpdateResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
fact_id=fact_id,
body=body,
instance_id=instance_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    user_id: str,
    fact_id: str,
    *,
    client: AuthenticatedClient,
    body: DirectUpdateRequest,
    instance_id: str | Unset = UNSET,

) -> DirectUpdateResponse | ErrorModel | None:
    """ Update a specific inventory fact

     Updates a specific inventory item by fact ID, merging new properties into the existing metadata.
    Creates a superseding fact.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        fact_id (str): Inventory fact UUID
        instance_id (str | Unset): Optional instance ID for user scoping
        body (DirectUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DirectUpdateResponse | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
user_id=user_id,
fact_id=fact_id,
client=client,
body=body,
instance_id=instance_id,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    user_id: str,
    fact_id: str,
    *,
    client: AuthenticatedClient,
    body: DirectUpdateRequest,
    instance_id: str | Unset = UNSET,

) -> Response[DirectUpdateResponse | ErrorModel]:
    """ Update a specific inventory fact

     Updates a specific inventory item by fact ID, merging new properties into the existing metadata.
    Creates a superseding fact.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        fact_id (str): Inventory fact UUID
        instance_id (str | Unset): Optional instance ID for user scoping
        body (DirectUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DirectUpdateResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
fact_id=fact_id,
body=body,
instance_id=instance_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    user_id: str,
    fact_id: str,
    *,
    client: AuthenticatedClient,
    body: DirectUpdateRequest,
    instance_id: str | Unset = UNSET,

) -> DirectUpdateResponse | ErrorModel | None:
    """ Update a specific inventory fact

     Updates a specific inventory item by fact ID, merging new properties into the existing metadata.
    Creates a superseding fact.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        fact_id (str): Inventory fact UUID
        instance_id (str | Unset): Optional instance ID for user scoping
        body (DirectUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DirectUpdateResponse | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
fact_id=fact_id,
client=client,
body=body,
instance_id=instance_id,

    )).parsed
