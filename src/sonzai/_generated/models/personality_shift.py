from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="PersonalityShift")



@_attrs_define
class PersonalityShift:
    """ 
        Attributes:
            direction (str):
            magnitude (str):
            timeframe_days (int):
            trait_name (str):
            trigger_types (list[str] | None):
            reasoning (str | Unset):
            timestamp (str | Unset):
     """

    direction: str
    magnitude: str
    timeframe_days: int
    trait_name: str
    trigger_types: list[str] | None
    reasoning: str | Unset = UNSET
    timestamp: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        direction = self.direction

        magnitude = self.magnitude

        timeframe_days = self.timeframe_days

        trait_name = self.trait_name

        trigger_types: list[str] | None
        if isinstance(self.trigger_types, list):
            trigger_types = self.trigger_types


        else:
            trigger_types = self.trigger_types

        reasoning = self.reasoning

        timestamp = self.timestamp


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "direction": direction,
            "magnitude": magnitude,
            "timeframe_days": timeframe_days,
            "trait_name": trait_name,
            "trigger_types": trigger_types,
        })
        if reasoning is not UNSET:
            field_dict["reasoning"] = reasoning
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        direction = d.pop("direction")

        magnitude = d.pop("magnitude")

        timeframe_days = d.pop("timeframe_days")

        trait_name = d.pop("trait_name")

        def _parse_trigger_types(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                trigger_types_type_0 = cast(list[str], data)

                return trigger_types_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        trigger_types = _parse_trigger_types(d.pop("trigger_types"))


        reasoning = d.pop("reasoning", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        personality_shift = cls(
            direction=direction,
            magnitude=magnitude,
            timeframe_days=timeframe_days,
            trait_name=trait_name,
            trigger_types=trigger_types,
            reasoning=reasoning,
            timestamp=timestamp,
        )

        return personality_shift

