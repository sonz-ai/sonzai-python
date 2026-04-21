from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="GenerateImageInputBody")



@_attrs_define
class GenerateImageInputBody:
    """ 
        Attributes:
            prompt (str): Image generation prompt
            schema (str | Unset): A URL to the JSON Schema for this object.
            model (str | Unset): Model to use (default: gemini-3.1-flash-image-preview)
            negative_prompt (str | Unset): Negative prompt (things to avoid)
            output_path (str | Unset): GCS output path
            provider (str | Unset): Provider to use (default: gemini)
     """

    prompt: str
    schema: str | Unset = UNSET
    model: str | Unset = UNSET
    negative_prompt: str | Unset = UNSET
    output_path: str | Unset = UNSET
    provider: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        schema = self.schema

        model = self.model

        negative_prompt = self.negative_prompt

        output_path = self.output_path

        provider = self.provider


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "prompt": prompt,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if model is not UNSET:
            field_dict["model"] = model
        if negative_prompt is not UNSET:
            field_dict["negative_prompt"] = negative_prompt
        if output_path is not UNSET:
            field_dict["output_path"] = output_path
        if provider is not UNSET:
            field_dict["provider"] = provider

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        prompt = d.pop("prompt")

        schema = d.pop("$schema", UNSET)

        model = d.pop("model", UNSET)

        negative_prompt = d.pop("negative_prompt", UNSET)

        output_path = d.pop("output_path", UNSET)

        provider = d.pop("provider", UNSET)

        generate_image_input_body = cls(
            prompt=prompt,
            schema=schema,
            model=model,
            negative_prompt=negative_prompt,
            output_path=output_path,
            provider=provider,
        )

        return generate_image_input_body

