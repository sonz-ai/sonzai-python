from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_analytics_rule import KBAnalyticsRule
from ...models.kb_update_analytics_rule_input_body import KbUpdateAnalyticsRuleInputBody
from typing import cast



def _get_kwargs(
    project_id: str,
    rule_id: str,
    *,
    body: KbUpdateAnalyticsRuleInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{project_id}/knowledge/analytics/rules/{rule_id}".format(project_id=quote(str(project_id), safe=""),rule_id=quote(str(rule_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KBAnalyticsRule:
    if response.status_code == 200:
        response_200 = KBAnalyticsRule.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KBAnalyticsRule]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,
    body: KbUpdateAnalyticsRuleInputBody,

) -> Response[ErrorModel | KBAnalyticsRule]:
    """ Update an analytics rule

     Updates an existing analytics rule's name, config, schedule, or enabled state.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID
        body (KbUpdateAnalyticsRuleInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBAnalyticsRule]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
rule_id=rule_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,
    body: KbUpdateAnalyticsRuleInputBody,

) -> ErrorModel | KBAnalyticsRule | None:
    """ Update an analytics rule

     Updates an existing analytics rule's name, config, schedule, or enabled state.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID
        body (KbUpdateAnalyticsRuleInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBAnalyticsRule
     """


    return sync_detailed(
        project_id=project_id,
rule_id=rule_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,
    body: KbUpdateAnalyticsRuleInputBody,

) -> Response[ErrorModel | KBAnalyticsRule]:
    """ Update an analytics rule

     Updates an existing analytics rule's name, config, schedule, or enabled state.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID
        body (KbUpdateAnalyticsRuleInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBAnalyticsRule]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
rule_id=rule_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,
    body: KbUpdateAnalyticsRuleInputBody,

) -> ErrorModel | KBAnalyticsRule | None:
    """ Update an analytics rule

     Updates an existing analytics rule's name, config, schedule, or enabled state.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID
        body (KbUpdateAnalyticsRuleInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBAnalyticsRule
     """


    return (await asyncio_detailed(
        project_id=project_id,
rule_id=rule_id,
client=client,
body=body,

    )).parsed
