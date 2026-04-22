"""Helpers that shape request payloads.

`encode_body` is the single site that marshals a user-supplied kwargs
dict through a spec-derived pydantic input body class. Using it means
(a) field typos raise ValidationError at the SDK boundary instead of
at the server, and (b) snake_case Python names round-trip to the wire's
camelCase aliases automatically.
"""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

M = TypeVar("M", bound=BaseModel)


def encode_body(model_cls: type[M], data: dict[str, Any]) -> dict[str, Any]:
    """Validate `data` against `model_cls` and return a wire-format dict.

    `model_cls` is a pydantic v2 class from `sonzai._generated.models`
    (e.g., `ChatInputBody`, `AddFactRequest`). `data` is the kwargs dict
    the resource method assembles from its parameters. Returns a dict
    ready to pass as `body=` to `_http.post` / `put` / `patch`.

    `by_alias=True` maps snake_case Python attrs to their camelCase
    wire aliases when declared via `Field(alias="camelCase")`.
    `exclude_none=True` drops optional fields the caller didn't set, so
    server-side defaults apply naturally.
    """
    validated = model_cls.model_validate(data)
    return validated.model_dump(by_alias=True, exclude_none=True)
