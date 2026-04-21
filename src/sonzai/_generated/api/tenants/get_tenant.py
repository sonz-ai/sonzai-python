from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.tenant import Tenant
from typing import cast



def _get_kwargs(
    tenant_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tenants/{tenant_id}".format(tenant_id=quote(str(tenant_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | Tenant:
    if response.status_code == 200:
        response_200 = Tenant.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | Tenant]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | Tenant]:
    """ Get a tenant

     Returns tenant metadata (name, slug, created_at) for the given tenant ID.

    Args:
        tenant_id (str): Tenant UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | Tenant]
     """


    kwargs = _get_kwargs(
        tenant_id=tenant_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    tenant_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | Tenant | None:
    """ Get a tenant

     Returns tenant metadata (name, slug, created_at) for the given tenant ID.

    Args:
        tenant_id (str): Tenant UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | Tenant
     """


    return sync_detailed(
        tenant_id=tenant_id,
client=client,

    ).parsed

async def asyncio_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | Tenant]:
    """ Get a tenant

     Returns tenant metadata (name, slug, created_at) for the given tenant ID.

    Args:
        tenant_id (str): Tenant UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | Tenant]
     """


    kwargs = _get_kwargs(
        tenant_id=tenant_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    tenant_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | Tenant | None:
    """ Get a tenant

     Returns tenant metadata (name, slug, created_at) for the given tenant ID.

    Args:
        tenant_id (str): Tenant UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | Tenant
     """


    return (await asyncio_detailed(
        tenant_id=tenant_id,
client=client,

    )).parsed
