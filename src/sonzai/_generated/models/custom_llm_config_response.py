from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CustomLLMConfigResponse")



@_attrs_define
class CustomLLMConfigResponse:
    """ 
        Attributes:
            api_key_prefix (str):
            configured (bool):
            display_name (str):
            endpoint (str):
            is_active (bool):
            model (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    api_key_prefix: str
    configured: bool
    display_name: str
    endpoint: str
    is_active: bool
    model: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        api_key_prefix = self.api_key_prefix

        configured = self.configured

        display_name = self.display_name

        endpoint = self.endpoint

        is_active = self.is_active

        model = self.model

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "api_key_prefix": api_key_prefix,
            "configured": configured,
            "display_name": display_name,
            "endpoint": endpoint,
            "is_active": is_active,
            "model": model,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_key_prefix = d.pop("api_key_prefix")

        configured = d.pop("configured")

        display_name = d.pop("display_name")

        endpoint = d.pop("endpoint")

        is_active = d.pop("is_active")

        model = d.pop("model")

        schema = d.pop("$schema", UNSET)

        custom_llm_config_response = cls(
            api_key_prefix=api_key_prefix,
            configured=configured,
            display_name=display_name,
            endpoint=endpoint,
            is_active=is_active,
            model=model,
            schema=schema,
        )

        return custom_llm_config_response

