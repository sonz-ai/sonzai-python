from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_get_recommendations_output_body import KbGetRecommendationsOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    source_id: str,
    rule_id: str,
    limit: int | Unset = 10,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["source_id"] = source_id

    params["rule_id"] = rule_id

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/analytics/recommendations".format(project_id=quote(str(project_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbGetRecommendationsOutputBody:
    if response.status_code == 200:
        response_200 = KbGetRecommendationsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbGetRecommendationsOutputBody]:
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
    source_id: str,
    rule_id: str,
    limit: int | Unset = 10,

) -> Response[ErrorModel | KbGetRecommendationsOutputBody]:
    """ Get knowledge base recommendations

     Returns scored recommendations for a source node based on a recommendation rule.

    Args:
        project_id (str): Project UUID
        source_id (str): Source node ID
        rule_id (str): Rule ID
        limit (int | Unset): Max results Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetRecommendationsOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
source_id=source_id,
rule_id=rule_id,
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
    source_id: str,
    rule_id: str,
    limit: int | Unset = 10,

) -> ErrorModel | KbGetRecommendationsOutputBody | None:
    """ Get knowledge base recommendations

     Returns scored recommendations for a source node based on a recommendation rule.

    Args:
        project_id (str): Project UUID
        source_id (str): Source node ID
        rule_id (str): Rule ID
        limit (int | Unset): Max results Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetRecommendationsOutputBody
     """


    return sync_detailed(
        project_id=project_id,
client=client,
source_id=source_id,
rule_id=rule_id,
limit=limit,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    source_id: str,
    rule_id: str,
    limit: int | Unset = 10,

) -> Response[ErrorModel | KbGetRecommendationsOutputBody]:
    """ Get knowledge base recommendations

     Returns scored recommendations for a source node based on a recommendation rule.

    Args:
        project_id (str): Project UUID
        source_id (str): Source node ID
        rule_id (str): Rule ID
        limit (int | Unset): Max results Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetRecommendationsOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
source_id=source_id,
rule_id=rule_id,
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
    source_id: str,
    rule_id: str,
    limit: int | Unset = 10,

) -> ErrorModel | KbGetRecommendationsOutputBody | None:
    """ Get knowledge base recommendations

     Returns scored recommendations for a source node based on a recommendation rule.

    Args:
        project_id (str): Project UUID
        source_id (str): Source node ID
        rule_id (str): Rule ID
        limit (int | Unset): Max results Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetRecommendationsOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
source_id=source_id,
rule_id=rule_id,
limit=limit,

    )).parsed
