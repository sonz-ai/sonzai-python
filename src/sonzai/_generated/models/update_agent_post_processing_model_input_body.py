from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateAgentPostProcessingModelInputBody")



@_attrs_define
class UpdateAgentPostProcessingModelInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            post_processing_model (str | Unset): Model for post-processing. Empty string clears the override.
            post_processing_provider (str | Unset): Provider for post-processing (e.g. 'gemini', 'openrouter'). Empty string
                clears the override.
     """

    schema: str | Unset = UNSET
    post_processing_model: str | Unset = UNSET
    post_processing_provider: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        post_processing_model = self.post_processing_model

        post_processing_provider = self.post_processing_provider


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if post_processing_model is not UNSET:
            field_dict["post_processing_model"] = post_processing_model
        if post_processing_provider is not UNSET:
            field_dict["post_processing_provider"] = post_processing_provider

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        post_processing_model = d.pop("post_processing_model", UNSET)

        post_processing_provider = d.pop("post_processing_provider", UNSET)

        update_agent_post_processing_model_input_body = cls(
            schema=schema,
            post_processing_model=post_processing_model,
            post_processing_provider=post_processing_provider,
        )

        return update_agent_post_processing_model_input_body

