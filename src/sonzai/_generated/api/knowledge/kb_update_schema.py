from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_entity_schema import KBEntitySchema
from ...models.kb_update_schema_input_body import KbUpdateSchemaInputBody
from typing import cast



def _get_kwargs(
    project_id: str,
    schema_id: str,
    *,
    body: KbUpdateSchemaInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{project_id}/knowledge/schemas/{schema_id}".format(project_id=quote(str(project_id), safe=""),schema_id=quote(str(schema_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KBEntitySchema:
    if response.status_code == 200:
        response_200 = KBEntitySchema.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KBEntitySchema]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    schema_id: str,
    *,
    client: AuthenticatedClient,
    body: KbUpdateSchemaInputBody,

) -> Response[ErrorModel | KBEntitySchema]:
    """ Update an entity schema

     Updates an existing entity schema definition.

    Args:
        project_id (str): Project UUID
        schema_id (str): Schema UUID
        body (KbUpdateSchemaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBEntitySchema]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
schema_id=schema_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    schema_id: str,
    *,
    client: AuthenticatedClient,
    body: KbUpdateSchemaInputBody,

) -> ErrorModel | KBEntitySchema | None:
    """ Update an entity schema

     Updates an existing entity schema definition.

    Args:
        project_id (str): Project UUID
        schema_id (str): Schema UUID
        body (KbUpdateSchemaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBEntitySchema
     """


    return sync_detailed(
        project_id=project_id,
schema_id=schema_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    schema_id: str,
    *,
    client: AuthenticatedClient,
    body: KbUpdateSchemaInputBody,

) -> Response[ErrorModel | KBEntitySchema]:
    """ Update an entity schema

     Updates an existing entity schema definition.

    Args:
        project_id (str): Project UUID
        schema_id (str): Schema UUID
        body (KbUpdateSchemaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBEntitySchema]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
schema_id=schema_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    schema_id: str,
    *,
    client: AuthenticatedClient,
    body: KbUpdateSchemaInputBody,

) -> ErrorModel | KBEntitySchema | None:
    """ Update an entity schema

     Updates an existing entity schema definition.

    Args:
        project_id (str): Project UUID
        schema_id (str): Schema UUID
        body (KbUpdateSchemaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBEntitySchema
     """


    return (await asyncio_detailed(
        project_id=project_id,
schema_id=schema_id,
client=client,
body=body,

    )).parsed
