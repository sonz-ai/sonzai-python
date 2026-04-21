from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="SetCustomLLMConfigInputBody")



@_attrs_define
class SetCustomLLMConfigInputBody:
    """ 
        Attributes:
            api_key (str): Plaintext API key for the endpoint (encrypted at rest)
            endpoint (str): HTTPS URL of the custom LLM endpoint (validated against SSRF targets)
            schema (str | Unset): A URL to the JSON Schema for this object.
            display_name (str | Unset): Human label for the dashboard
            is_active (bool | Unset): Activate the config immediately (default true)
            model (str | Unset): Model name to request at the endpoint
     """

    api_key: str
    endpoint: str
    schema: str | Unset = UNSET
    display_name: str | Unset = UNSET
    is_active: bool | Unset = UNSET
    model: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        api_key = self.api_key

        endpoint = self.endpoint

        schema = self.schema

        display_name = self.display_name

        is_active = self.is_active

        model = self.model


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "api_key": api_key,
            "endpoint": endpoint,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_key = d.pop("api_key")

        endpoint = d.pop("endpoint")

        schema = d.pop("$schema", UNSET)

        display_name = d.pop("display_name", UNSET)

        is_active = d.pop("is_active", UNSET)

        model = d.pop("model", UNSET)

        set_custom_llm_config_input_body = cls(
            api_key=api_key,
            endpoint=endpoint,
            schema=schema,
            display_name=display_name,
            is_active=is_active,
            model=model,
        )

        return set_custom_llm_config_input_body

