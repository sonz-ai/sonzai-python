from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_record_feedback_input_body import KbRecordFeedbackInputBody
from ...models.kb_record_feedback_output_body import KbRecordFeedbackOutputBody
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    body: KbRecordFeedbackInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/knowledge/analytics/feedback".format(project_id=quote(str(project_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbRecordFeedbackOutputBody:
    if response.status_code == 200:
        response_200 = KbRecordFeedbackOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbRecordFeedbackOutputBody]:
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
    body: KbRecordFeedbackInputBody,

) -> Response[ErrorModel | KbRecordFeedbackOutputBody]:
    """ Record recommendation feedback

     Records that a recommendation was shown and optionally converted. Triggers conversion analysis when
    converted=true.

    Args:
        project_id (str): Project UUID
        body (KbRecordFeedbackInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbRecordFeedbackOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: KbRecordFeedbackInputBody,

) -> ErrorModel | KbRecordFeedbackOutputBody | None:
    """ Record recommendation feedback

     Records that a recommendation was shown and optionally converted. Triggers conversion analysis when
    converted=true.

    Args:
        project_id (str): Project UUID
        body (KbRecordFeedbackInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbRecordFeedbackOutputBody
     """


    return sync_detailed(
        project_id=project_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: KbRecordFeedbackInputBody,

) -> Response[ErrorModel | KbRecordFeedbackOutputBody]:
    """ Record recommendation feedback

     Records that a recommendation was shown and optionally converted. Triggers conversion analysis when
    converted=true.

    Args:
        project_id (str): Project UUID
        body (KbRecordFeedbackInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbRecordFeedbackOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: KbRecordFeedbackInputBody,

) -> ErrorModel | KbRecordFeedbackOutputBody | None:
    """ Record recommendation feedback

     Records that a recommendation was shown and optionally converted. Triggers conversion analysis when
    converted=true.

    Args:
        project_id (str): Project UUID
        body (KbRecordFeedbackInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbRecordFeedbackOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
body=body,

    )).parsed
