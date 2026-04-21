from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_get_conversion_stats_output_body import KbGetConversionStatsOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    rule_id: str,
    segment: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["rule_id"] = rule_id

    params["segment"] = segment


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/analytics/conversions".format(project_id=quote(str(project_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbGetConversionStatsOutputBody:
    if response.status_code == 200:
        response_200 = KbGetConversionStatsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbGetConversionStatsOutputBody]:
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
    segment: str | Unset = UNSET,

) -> Response[ErrorModel | KbGetConversionStatsOutputBody]:
    """ Get conversion statistics

     Returns conversion statistics for a recommendation rule, optionally filtered by segment.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule ID
        segment (str | Unset): Optional segment key filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetConversionStatsOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
rule_id=rule_id,
segment=segment,

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
    segment: str | Unset = UNSET,

) -> ErrorModel | KbGetConversionStatsOutputBody | None:
    """ Get conversion statistics

     Returns conversion statistics for a recommendation rule, optionally filtered by segment.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule ID
        segment (str | Unset): Optional segment key filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetConversionStatsOutputBody
     """


    return sync_detailed(
        project_id=project_id,
client=client,
rule_id=rule_id,
segment=segment,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    rule_id: str,
    segment: str | Unset = UNSET,

) -> Response[ErrorModel | KbGetConversionStatsOutputBody]:
    """ Get conversion statistics

     Returns conversion statistics for a recommendation rule, optionally filtered by segment.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule ID
        segment (str | Unset): Optional segment key filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetConversionStatsOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
rule_id=rule_id,
segment=segment,

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
    segment: str | Unset = UNSET,

) -> ErrorModel | KbGetConversionStatsOutputBody | None:
    """ Get conversion statistics

     Returns conversion statistics for a recommendation rule, optionally filtered by segment.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule ID
        segment (str | Unset): Optional segment key filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetConversionStatsOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
rule_id=rule_id,
segment=segment,

    )).parsed
