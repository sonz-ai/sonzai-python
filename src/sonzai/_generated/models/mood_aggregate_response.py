from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="MoodAggregateResponse")



@_attrs_define
class MoodAggregateResponse:
    """ 
        Attributes:
            affiliation (float):
            arousal (float):
            days_window (int):
            label (str):
            tension (float):
            user_count (int):
            valence (float):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    affiliation: float
    arousal: float
    days_window: int
    label: str
    tension: float
    user_count: int
    valence: float
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        affiliation = self.affiliation

        arousal = self.arousal

        days_window = self.days_window

        label = self.label

        tension = self.tension

        user_count = self.user_count

        valence = self.valence

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "affiliation": affiliation,
            "arousal": arousal,
            "days_window": days_window,
            "label": label,
            "tension": tension,
            "user_count": user_count,
            "valence": valence,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        affiliation = d.pop("affiliation")

        arousal = d.pop("arousal")

        days_window = d.pop("days_window")

        label = d.pop("label")

        tension = d.pop("tension")

        user_count = d.pop("user_count")

        valence = d.pop("valence")

        schema = d.pop("$schema", UNSET)

        mood_aggregate_response = cls(
            affiliation=affiliation,
            arousal=arousal,
            days_window=days_window,
            label=label,
            tension=tension,
            user_count=user_count,
            valence=valence,
            schema=schema,
        )

        return mood_aggregate_response

