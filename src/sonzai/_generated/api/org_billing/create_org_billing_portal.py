from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.org_billing_url_body import OrgBillingURLBody
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/org/billing/portal",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | OrgBillingURLBody:
    if response.status_code == 200:
        response_200 = OrgBillingURLBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | OrgBillingURLBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | OrgBillingURLBody]:
    """ Create Stripe billing-portal session

     Creates a Stripe Customer Portal session. Dashboard redirects the user there to manage payment
    methods and subscriptions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | OrgBillingURLBody]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> ErrorModel | OrgBillingURLBody | None:
    """ Create Stripe billing-portal session

     Creates a Stripe Customer Portal session. Dashboard redirects the user there to manage payment
    methods and subscriptions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | OrgBillingURLBody
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | OrgBillingURLBody]:
    """ Create Stripe billing-portal session

     Creates a Stripe Customer Portal session. Dashboard redirects the user there to manage payment
    methods and subscriptions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | OrgBillingURLBody]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> ErrorModel | OrgBillingURLBody | None:
    """ Create Stripe billing-portal session

     Creates a Stripe Customer Portal session. Dashboard redirects the user there to manage payment
    methods and subscriptions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | OrgBillingURLBody
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
