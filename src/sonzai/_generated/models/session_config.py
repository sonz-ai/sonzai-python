from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.turn import Turn





T = TypeVar("T", bound="SessionConfig")



@_attrs_define
class SessionConfig:
    """ 
        Attributes:
            name (str):
            time_gap_hours (int):
            turns (list[Turn] | None):
     """

    name: str
    time_gap_hours: int
    turns: list[Turn] | None





    def to_dict(self) -> dict[str, Any]:
        from ..models.turn import Turn
        name = self.name

        time_gap_hours = self.time_gap_hours

        turns: list[dict[str, Any]] | None
        if isinstance(self.turns, list):
            turns = []
            for turns_type_0_item_data in self.turns:
                turns_type_0_item = turns_type_0_item_data.to_dict()
                turns.append(turns_type_0_item)


        else:
            turns = self.turns


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "time_gap_hours": time_gap_hours,
            "turns": turns,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.turn import Turn
        d = dict(src_dict)
        name = d.pop("name")

        time_gap_hours = d.pop("time_gap_hours")

        def _parse_turns(data: object) -> list[Turn] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                turns_type_0 = []
                _turns_type_0 = data
                for turns_type_0_item_data in (_turns_type_0):
                    turns_type_0_item = Turn.from_dict(turns_type_0_item_data)



                    turns_type_0.append(turns_type_0_item)

                return turns_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Turn] | None, data)

        turns = _parse_turns(d.pop("turns"))


        session_config = cls(
            name=name,
            time_gap_hours=time_gap_hours,
            turns=turns,
        )

        return session_config

