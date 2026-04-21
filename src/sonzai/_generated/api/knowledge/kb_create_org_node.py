from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_create_org_node_input_body import KbCreateOrgNodeInputBody
from ...models.kb_node import KBNode
from typing import cast



def _get_kwargs(
    tenant_id: str,
    *,
    body: KbCreateOrgNodeInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tenants/{tenant_id}/knowledge/org-nodes".format(tenant_id=quote(str(tenant_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KBNode:
    if response.status_code == 200:
        response_200 = KBNode.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KBNode]:
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
    body: KbCreateOrgNodeInputBody,

) -> Response[ErrorModel | KBNode]:
    r""" Create a knowledge-base node in the organization-global scope

     Writes a node at scope_id=\"\" so every project under the tenant can read it via cascade / union
    scope modes. Idempotency is the caller's responsibility; a dashboard should look up by label before
    calling this.

    Args:
        tenant_id (str): Tenant UUID — scope_id for the write is the empty string so the node
            lives in the organization-global scope.
        body (KbCreateOrgNodeInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBNode]
     """


    kwargs = _get_kwargs(
        tenant_id=tenant_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: KbCreateOrgNodeInputBody,

) -> ErrorModel | KBNode | None:
    r""" Create a knowledge-base node in the organization-global scope

     Writes a node at scope_id=\"\" so every project under the tenant can read it via cascade / union
    scope modes. Idempotency is the caller's responsibility; a dashboard should look up by label before
    calling this.

    Args:
        tenant_id (str): Tenant UUID — scope_id for the write is the empty string so the node
            lives in the organization-global scope.
        body (KbCreateOrgNodeInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBNode
     """


    return sync_detailed(
        tenant_id=tenant_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: KbCreateOrgNodeInputBody,

) -> Response[ErrorModel | KBNode]:
    r""" Create a knowledge-base node in the organization-global scope

     Writes a node at scope_id=\"\" so every project under the tenant can read it via cascade / union
    scope modes. Idempotency is the caller's responsibility; a dashboard should look up by label before
    calling this.

    Args:
        tenant_id (str): Tenant UUID — scope_id for the write is the empty string so the node
            lives in the organization-global scope.
        body (KbCreateOrgNodeInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBNode]
     """


    kwargs = _get_kwargs(
        tenant_id=tenant_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: KbCreateOrgNodeInputBody,

) -> ErrorModel | KBNode | None:
    r""" Create a knowledge-base node in the organization-global scope

     Writes a node at scope_id=\"\" so every project under the tenant can read it via cascade / union
    scope modes. Idempotency is the caller's responsibility; a dashboard should look up by label before
    calling this.

    Args:
        tenant_id (str): Tenant UUID — scope_id for the write is the empty string so the node
            lives in the organization-global scope.
        body (KbCreateOrgNodeInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBNode
     """


    return (await asyncio_detailed(
        tenant_id=tenant_id,
client=client,
body=body,

    )).parsed
