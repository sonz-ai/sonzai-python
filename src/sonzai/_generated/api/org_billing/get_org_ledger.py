from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.tenant_billing_ledger_entry import TenantBillingLedgerEntry
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    days: int | Unset = 30,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["days"] = days


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/org/ledger",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | list[TenantBillingLedgerEntry] | None:
    if response.status_code == 200:
        def _parse_response_200(data: object) -> list[TenantBillingLedgerEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                response_200_type_0 = []
                _response_200_type_0 = data
                for response_200_type_0_item_data in (_response_200_type_0):
                    response_200_type_0_item = TenantBillingLedgerEntry.from_dict(response_200_type_0_item_data)



                    response_200_type_0.append(response_200_type_0_item)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[TenantBillingLedgerEntry] | None, data)

        response_200 = _parse_response_200(response.json())

        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | list[TenantBillingLedgerEntry] | None]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Response[ErrorModel | list[TenantBillingLedgerEntry] | None]:
    """ Get org billing ledger

     Returns the tenant billing ledger — credits, debits, adjustments over time.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | list[TenantBillingLedgerEntry] | None]
     """


    kwargs = _get_kwargs(
        days=days,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> ErrorModel | list[TenantBillingLedgerEntry] | None | None:
    """ Get org billing ledger

     Returns the tenant billing ledger — credits, debits, adjustments over time.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | list[TenantBillingLedgerEntry] | None
     """


    return sync_detailed(
        client=client,
days=days,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Response[ErrorModel | list[TenantBillingLedgerEntry] | None]:
    """ Get org billing ledger

     Returns the tenant billing ledger — credits, debits, adjustments over time.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | list[TenantBillingLedgerEntry] | None]
     """


    kwargs = _get_kwargs(
        days=days,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> ErrorModel | list[TenantBillingLedgerEntry] | None | None:
    """ Get org billing ledger

     Returns the tenant billing ledger — credits, debits, adjustments over time.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | list[TenantBillingLedgerEntry] | None
     """


    return (await asyncio_detailed(
        client=client,
days=days,

    )).parsed
