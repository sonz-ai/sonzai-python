from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateAgentPostProcessingModelOutputBody")



@_attrs_define
class UpdateAgentPostProcessingModelOutputBody:
    """ 
        Attributes:
            post_processing_model (str):
            post_processing_provider (str):
            success (bool):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    post_processing_model: str
    post_processing_provider: str
    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        post_processing_model = self.post_processing_model

        post_processing_provider = self.post_processing_provider

        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "post_processing_model": post_processing_model,
            "post_processing_provider": post_processing_provider,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        post_processing_model = d.pop("post_processing_model")

        post_processing_provider = d.pop("post_processing_provider")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        update_agent_post_processing_model_output_body = cls(
            post_processing_model=post_processing_model,
            post_processing_provider=post_processing_provider,
            success=success,
            schema=schema,
        )

        return update_agent_post_processing_model_output_body

