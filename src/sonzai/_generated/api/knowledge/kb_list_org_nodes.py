from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_list_org_nodes_output_body import KbListOrgNodesOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    tenant_id: str,
    *,
    limit: int | Unset = 200,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tenants/{tenant_id}/knowledge/org-nodes".format(tenant_id=quote(str(tenant_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbListOrgNodesOutputBody:
    if response.status_code == 200:
        response_200 = KbListOrgNodesOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbListOrgNodesOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 200,

) -> Response[ErrorModel | KbListOrgNodesOutputBody]:
    r""" List nodes in the organization-global KB scope

     Returns active nodes stored at scope_id=\"\" for the given tenant. Used by the admin dashboard's
    cascade browser.

    Args:
        tenant_id (str): Tenant UUID whose organization-global KB scope is listed.
        limit (int | Unset): Max number of nodes to return; 0 = all rows in the partition.
            Default: 200.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbListOrgNodesOutputBody]
     """


    kwargs = _get_kwargs(
        tenant_id=tenant_id,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 200,

) -> ErrorModel | KbListOrgNodesOutputBody | None:
    r""" List nodes in the organization-global KB scope

     Returns active nodes stored at scope_id=\"\" for the given tenant. Used by the admin dashboard's
    cascade browser.

    Args:
        tenant_id (str): Tenant UUID whose organization-global KB scope is listed.
        limit (int | Unset): Max number of nodes to return; 0 = all rows in the partition.
            Default: 200.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbListOrgNodesOutputBody
     """


    return sync_detailed(
        tenant_id=tenant_id,
client=client,
limit=limit,

    ).parsed

async def asyncio_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 200,

) -> Response[ErrorModel | KbListOrgNodesOutputBody]:
    r""" List nodes in the organization-global KB scope

     Returns active nodes stored at scope_id=\"\" for the given tenant. Used by the admin dashboard's
    cascade browser.

    Args:
        tenant_id (str): Tenant UUID whose organization-global KB scope is listed.
        limit (int | Unset): Max number of nodes to return; 0 = all rows in the partition.
            Default: 200.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbListOrgNodesOutputBody]
     """


    kwargs = _get_kwargs(
        tenant_id=tenant_id,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 200,

) -> ErrorModel | KbListOrgNodesOutputBody | None:
    r""" List nodes in the organization-global KB scope

     Returns active nodes stored at scope_id=\"\" for the given tenant. Used by the admin dashboard's
    cascade browser.

    Args:
        tenant_id (str): Tenant UUID whose organization-global KB scope is listed.
        limit (int | Unset): Max number of nodes to return; 0 = all rows in the partition.
            Default: 200.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbListOrgNodesOutputBody
     """


    return (await asyncio_detailed(
        tenant_id=tenant_id,
client=client,
limit=limit,

    )).parsed
