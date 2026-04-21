from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.custom_llm_config_response import CustomLLMConfigResponse
from ...models.error_model import ErrorModel
from ...models.set_custom_llm_config_input_body import SetCustomLLMConfigInputBody
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    body: SetCustomLLMConfigInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{project_id}/custom-llm".format(project_id=quote(str(project_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CustomLLMConfigResponse | ErrorModel:
    if response.status_code == 200:
        response_200 = CustomLLMConfigResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CustomLLMConfigResponse | ErrorModel]:
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
    body: SetCustomLLMConfigInputBody,

) -> Response[CustomLLMConfigResponse | ErrorModel]:
    """ Set custom LLM config for a project

     Stores the endpoint and an encrypted API key. The endpoint is validated against the SSRF deny-list
    (private networks, metadata IPs). Requires `CUSTOM_LLM_ENCRYPTION_KEY` to be configured on the
    server.

    Args:
        project_id (str): Project UUID
        body (SetCustomLLMConfigInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomLLMConfigResponse | ErrorModel]
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
    body: SetCustomLLMConfigInputBody,

) -> CustomLLMConfigResponse | ErrorModel | None:
    """ Set custom LLM config for a project

     Stores the endpoint and an encrypted API key. The endpoint is validated against the SSRF deny-list
    (private networks, metadata IPs). Requires `CUSTOM_LLM_ENCRYPTION_KEY` to be configured on the
    server.

    Args:
        project_id (str): Project UUID
        body (SetCustomLLMConfigInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomLLMConfigResponse | ErrorModel
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
    body: SetCustomLLMConfigInputBody,

) -> Response[CustomLLMConfigResponse | ErrorModel]:
    """ Set custom LLM config for a project

     Stores the endpoint and an encrypted API key. The endpoint is validated against the SSRF deny-list
    (private networks, metadata IPs). Requires `CUSTOM_LLM_ENCRYPTION_KEY` to be configured on the
    server.

    Args:
        project_id (str): Project UUID
        body (SetCustomLLMConfigInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomLLMConfigResponse | ErrorModel]
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
    body: SetCustomLLMConfigInputBody,

) -> CustomLLMConfigResponse | ErrorModel | None:
    """ Set custom LLM config for a project

     Stores the endpoint and an encrypted API key. The endpoint is validated against the SSRF deny-list
    (private networks, metadata IPs). Requires `CUSTOM_LLM_ENCRYPTION_KEY` to be configured on the
    server.

    Args:
        project_id (str): Project UUID
        body (SetCustomLLMConfigInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomLLMConfigResponse | ErrorModel
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
body=body,

    )).parsed
