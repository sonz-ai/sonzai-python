from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.org_model_price_item import OrgModelPriceItem
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/org/model-pricing",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | list[OrgModelPriceItem] | None:
    if response.status_code == 200:
        def _parse_response_200(data: object) -> list[OrgModelPriceItem] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                response_200_type_0 = []
                _response_200_type_0 = data
                for response_200_type_0_item_data in (_response_200_type_0):
                    response_200_type_0_item = OrgModelPriceItem.from_dict(response_200_type_0_item_data)



                    response_200_type_0.append(response_200_type_0_item)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[OrgModelPriceItem] | None, data)

        response_200 = _parse_response_200(response.json())

        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | list[OrgModelPriceItem] | None]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | list[OrgModelPriceItem] | None]:
    """ Get active model pricing

     Returns current per-token model pricing (base and tenant-specific overrides).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | list[OrgModelPriceItem] | None]
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

) -> ErrorModel | list[OrgModelPriceItem] | None | None:
    """ Get active model pricing

     Returns current per-token model pricing (base and tenant-specific overrides).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | list[OrgModelPriceItem] | None
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | list[OrgModelPriceItem] | None]:
    """ Get active model pricing

     Returns current per-token model pricing (base and tenant-specific overrides).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | list[OrgModelPriceItem] | None]
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

) -> ErrorModel | list[OrgModelPriceItem] | None | None:
    """ Get active model pricing

     Returns current per-token model pricing (base and tenant-specific overrides).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | list[OrgModelPriceItem] | None
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
