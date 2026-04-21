from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.mood_state import MoodState





T = TypeVar("T", bound="MoodResponse")



@_attrs_define
class MoodResponse:
    """ 
        Attributes:
            mood (MoodState):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    mood: MoodState
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.mood_state import MoodState
        mood = self.mood.to_dict()

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "mood": mood,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mood_state import MoodState
        d = dict(src_dict)
        mood = MoodState.from_dict(d.pop("mood"))




        schema = d.pop("$schema", UNSET)

        mood_response = cls(
            mood=mood,
            schema=schema,
        )

        return mood_response

