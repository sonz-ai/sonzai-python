from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_node_with_scope import KBNodeWithScope
from ...models.kb_promote_node_input_body import KbPromoteNodeInputBody
from typing import cast



def _get_kwargs(
    project_id: str,
    node_id: str,
    *,
    body: KbPromoteNodeInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/knowledge/nodes/{node_id}/promote-to-org".format(project_id=quote(str(project_id), safe=""),node_id=quote(str(node_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KBNodeWithScope:
    if response.status_code == 200:
        response_200 = KBNodeWithScope.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KBNodeWithScope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: KbPromoteNodeInputBody,

) -> Response[ErrorModel | KBNodeWithScope]:
    r""" Promote a project-scoped node to the organization-global scope

     Copies the node into scope_id=\"\"; the project copy is kept. If an org node with the same
    (node_type, norm_label) already exists, returns that one instead of writing a duplicate.

    Args:
        project_id (str): Project UUID that currently owns the node
        node_id (str): Node UUID to promote
        body (KbPromoteNodeInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBNodeWithScope]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
node_id=node_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: KbPromoteNodeInputBody,

) -> ErrorModel | KBNodeWithScope | None:
    r""" Promote a project-scoped node to the organization-global scope

     Copies the node into scope_id=\"\"; the project copy is kept. If an org node with the same
    (node_type, norm_label) already exists, returns that one instead of writing a duplicate.

    Args:
        project_id (str): Project UUID that currently owns the node
        node_id (str): Node UUID to promote
        body (KbPromoteNodeInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBNodeWithScope
     """


    return sync_detailed(
        project_id=project_id,
node_id=node_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: KbPromoteNodeInputBody,

) -> Response[ErrorModel | KBNodeWithScope]:
    r""" Promote a project-scoped node to the organization-global scope

     Copies the node into scope_id=\"\"; the project copy is kept. If an org node with the same
    (node_type, norm_label) already exists, returns that one instead of writing a duplicate.

    Args:
        project_id (str): Project UUID that currently owns the node
        node_id (str): Node UUID to promote
        body (KbPromoteNodeInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBNodeWithScope]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
node_id=node_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: KbPromoteNodeInputBody,

) -> ErrorModel | KBNodeWithScope | None:
    r""" Promote a project-scoped node to the organization-global scope

     Copies the node into scope_id=\"\"; the project copy is kept. If an org node with the same
    (node_type, norm_label) already exists, returns that one instead of writing a duplicate.

    Args:
        project_id (str): Project UUID that currently owns the node
        node_id (str): Node UUID to promote
        body (KbPromoteNodeInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBNodeWithScope
     """


    return (await asyncio_detailed(
        project_id=project_id,
node_id=node_id,
client=client,
body=body,

    )).parsed
