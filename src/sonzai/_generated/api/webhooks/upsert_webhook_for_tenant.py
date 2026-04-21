from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.upsert_webhook_for_tenant_input_body import UpsertWebhookForTenantInputBody
from ...models.upsert_webhook_output_body import UpsertWebhookOutputBody
from typing import cast



def _get_kwargs(
    event_type: str,
    *,
    body: UpsertWebhookForTenantInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/webhooks/{event_type}".format(event_type=quote(str(event_type), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | UpsertWebhookOutputBody:
    if response.status_code == 200:
        response_200 = UpsertWebhookOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | UpsertWebhookOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    event_type: str,
    *,
    client: AuthenticatedClient,
    body: UpsertWebhookForTenantInputBody,

) -> Response[ErrorModel | UpsertWebhookOutputBody]:
    """ Register or update a webhook (tenant-scoped)

     Creates or updates a webhook for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type (e.g. session.end, memory.created)
        body (UpsertWebhookForTenantInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UpsertWebhookOutputBody]
     """


    kwargs = _get_kwargs(
        event_type=event_type,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    event_type: str,
    *,
    client: AuthenticatedClient,
    body: UpsertWebhookForTenantInputBody,

) -> ErrorModel | UpsertWebhookOutputBody | None:
    """ Register or update a webhook (tenant-scoped)

     Creates or updates a webhook for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type (e.g. session.end, memory.created)
        body (UpsertWebhookForTenantInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UpsertWebhookOutputBody
     """


    return sync_detailed(
        event_type=event_type,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    event_type: str,
    *,
    client: AuthenticatedClient,
    body: UpsertWebhookForTenantInputBody,

) -> Response[ErrorModel | UpsertWebhookOutputBody]:
    """ Register or update a webhook (tenant-scoped)

     Creates or updates a webhook for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type (e.g. session.end, memory.created)
        body (UpsertWebhookForTenantInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UpsertWebhookOutputBody]
     """


    kwargs = _get_kwargs(
        event_type=event_type,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    event_type: str,
    *,
    client: AuthenticatedClient,
    body: UpsertWebhookForTenantInputBody,

) -> ErrorModel | UpsertWebhookOutputBody | None:
    """ Register or update a webhook (tenant-scoped)

     Creates or updates a webhook for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type (e.g. session.end, memory.created)
        body (UpsertWebhookForTenantInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UpsertWebhookOutputBody
     """


    return (await asyncio_detailed(
        event_type=event_type,
client=client,
body=body,

    )).parsed
