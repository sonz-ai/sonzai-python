from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.inventory_write_request import InventoryWriteRequest
from ...models.inventory_write_response import InventoryWriteResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,
    *,
    body: InventoryWriteRequest,
    instance_id: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["instance_id"] = instance_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/users/{user_id}/inventory".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | InventoryWriteResponse:
    if response.status_code == 200:
        response_200 = InventoryWriteResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | InventoryWriteResponse]:
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
    body: InventoryWriteRequest,
    instance_id: str | Unset = UNSET,

) -> Response[ErrorModel | InventoryWriteResponse]:
    """ Add, update, or remove an inventory item

     Performs an inventory write operation (add, update, or remove). For add operations, searches the
    knowledge base to resolve the item. Returns disambiguation candidates if multiple KB matches are
    found.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID for user scoping
        body (InventoryWriteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | InventoryWriteResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
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
    *,
    client: AuthenticatedClient,
    body: InventoryWriteRequest,
    instance_id: str | Unset = UNSET,

) -> ErrorModel | InventoryWriteResponse | None:
    """ Add, update, or remove an inventory item

     Performs an inventory write operation (add, update, or remove). For add operations, searches the
    knowledge base to resolve the item. Returns disambiguation candidates if multiple KB matches are
    found.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID for user scoping
        body (InventoryWriteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | InventoryWriteResponse
     """


    return sync_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
body=body,
instance_id=instance_id,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: InventoryWriteRequest,
    instance_id: str | Unset = UNSET,

) -> Response[ErrorModel | InventoryWriteResponse]:
    """ Add, update, or remove an inventory item

     Performs an inventory write operation (add, update, or remove). For add operations, searches the
    knowledge base to resolve the item. Returns disambiguation candidates if multiple KB matches are
    found.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID for user scoping
        body (InventoryWriteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | InventoryWriteResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
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
    *,
    client: AuthenticatedClient,
    body: InventoryWriteRequest,
    instance_id: str | Unset = UNSET,

) -> ErrorModel | InventoryWriteResponse | None:
    """ Add, update, or remove an inventory item

     Performs an inventory write operation (add, update, or remove). For add operations, searches the
    knowledge base to resolve the item. Returns disambiguation candidates if multiple KB matches are
    found.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID
        instance_id (str | Unset): Optional instance ID for user scoping
        body (InventoryWriteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | InventoryWriteResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
body=body,
instance_id=instance_id,

    )).parsed
