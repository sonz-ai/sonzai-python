from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.batch_personality_response_personalities import BatchPersonalityResponsePersonalities





T = TypeVar("T", bound="BatchPersonalityResponse")



@_attrs_define
class BatchPersonalityResponse:
    """ 
        Attributes:
            personalities (BatchPersonalityResponsePersonalities):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    personalities: BatchPersonalityResponsePersonalities
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_personality_response_personalities import BatchPersonalityResponsePersonalities
        personalities = self.personalities.to_dict()

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "personalities": personalities,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_personality_response_personalities import BatchPersonalityResponsePersonalities
        d = dict(src_dict)
        personalities = BatchPersonalityResponsePersonalities.from_dict(d.pop("personalities"))




        schema = d.pop("$schema", UNSET)

        batch_personality_response = cls(
            personalities=personalities,
            schema=schema,
        )

        return batch_personality_response

