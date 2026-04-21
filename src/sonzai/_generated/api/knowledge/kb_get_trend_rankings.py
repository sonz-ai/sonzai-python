from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_get_trend_rankings_output_body import KbGetTrendRankingsOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    rule_id: str,
    type_: str,
    window: str,
    limit: int | Unset = 10,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["rule_id"] = rule_id

    params["type"] = type_

    params["window"] = window

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/analytics/rankings".format(project_id=quote(str(project_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbGetTrendRankingsOutputBody:
    if response.status_code == 200:
        response_200 = KbGetTrendRankingsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbGetTrendRankingsOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    rule_id: str,
    type_: str,
    window: str,
    limit: int | Unset = 10,

) -> Response[ErrorModel | KbGetTrendRankingsOutputBody]:
    """ Get trend rankings

     Returns ranked trends for a specific rule, type, and time window.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule ID
        type_ (str): Ranking type
        window (str): Time window
        limit (int | Unset): Max results Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetTrendRankingsOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
rule_id=rule_id,
type_=type_,
window=window,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    rule_id: str,
    type_: str,
    window: str,
    limit: int | Unset = 10,

) -> ErrorModel | KbGetTrendRankingsOutputBody | None:
    """ Get trend rankings

     Returns ranked trends for a specific rule, type, and time window.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule ID
        type_ (str): Ranking type
        window (str): Time window
        limit (int | Unset): Max results Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetTrendRankingsOutputBody
     """


    return sync_detailed(
        project_id=project_id,
client=client,
rule_id=rule_id,
type_=type_,
window=window,
limit=limit,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    rule_id: str,
    type_: str,
    window: str,
    limit: int | Unset = 10,

) -> Response[ErrorModel | KbGetTrendRankingsOutputBody]:
    """ Get trend rankings

     Returns ranked trends for a specific rule, type, and time window.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule ID
        type_ (str): Ranking type
        window (str): Time window
        limit (int | Unset): Max results Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetTrendRankingsOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
rule_id=rule_id,
type_=type_,
window=window,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    rule_id: str,
    type_: str,
    window: str,
    limit: int | Unset = 10,

) -> ErrorModel | KbGetTrendRankingsOutputBody | None:
    """ Get trend rankings

     Returns ranked trends for a specific rule, type, and time window.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule ID
        type_ (str): Ranking type
        window (str): Time window
        limit (int | Unset): Max results Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetTrendRankingsOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
rule_id=rule_id,
type_=type_,
window=window,
limit=limit,

    )).parsed
