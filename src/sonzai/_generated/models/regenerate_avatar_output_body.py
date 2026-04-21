from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="RegenerateAvatarOutputBody")



@_attrs_define
class RegenerateAvatarOutputBody:
    """ 
        Attributes:
            avatar_url (str): Public URL of generated avatar
            generation_time_ms (int): Time spent generating in milliseconds
            prompt (str): Prompt used for generation
            success (bool): Whether avatar was generated
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    avatar_url: str
    generation_time_ms: int
    prompt: str
    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        avatar_url = self.avatar_url

        generation_time_ms = self.generation_time_ms

        prompt = self.prompt

        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "avatar_url": avatar_url,
            "generation_time_ms": generation_time_ms,
            "prompt": prompt,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        avatar_url = d.pop("avatar_url")

        generation_time_ms = d.pop("generation_time_ms")

        prompt = d.pop("prompt")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        regenerate_avatar_output_body = cls(
            avatar_url=avatar_url,
            generation_time_ms=generation_time_ms,
            prompt=prompt,
            success=success,
            schema=schema,
        )

        return regenerate_avatar_output_body

