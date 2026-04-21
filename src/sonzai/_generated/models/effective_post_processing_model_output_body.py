from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="EffectivePostProcessingModelOutputBody")



@_attrs_define
class EffectivePostProcessingModelOutputBody:
    """ 
        Attributes:
            max_tokens (int):
            model (str):
            provider (str):
            temperature (float):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    max_tokens: int
    model: str
    provider: str
    temperature: float
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        max_tokens = self.max_tokens

        model = self.model

        provider = self.provider

        temperature = self.temperature

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "max_tokens": max_tokens,
            "model": model,
            "provider": provider,
            "temperature": temperature,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_tokens = d.pop("max_tokens")

        model = d.pop("model")

        provider = d.pop("provider")

        temperature = d.pop("temperature")

        schema = d.pop("$schema", UNSET)

        effective_post_processing_model_output_body = cls(
            max_tokens=max_tokens,
            model=model,
            provider=provider,
            temperature=temperature,
            schema=schema,
        )

        return effective_post_processing_model_output_body

