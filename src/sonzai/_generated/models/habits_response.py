from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.habit import Habit





T = TypeVar("T", bound="HabitsResponse")



@_attrs_define
class HabitsResponse:
    """ 
        Attributes:
            habits (list[Habit] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    habits: list[Habit] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.habit import Habit
        habits: list[dict[str, Any]] | None
        if isinstance(self.habits, list):
            habits = []
            for habits_type_0_item_data in self.habits:
                habits_type_0_item = habits_type_0_item_data.to_dict()
                habits.append(habits_type_0_item)


        else:
            habits = self.habits

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "habits": habits,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.habit import Habit
        d = dict(src_dict)
        def _parse_habits(data: object) -> list[Habit] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                habits_type_0 = []
                _habits_type_0 = data
                for habits_type_0_item_data in (_habits_type_0):
                    habits_type_0_item = Habit.from_dict(habits_type_0_item_data)



                    habits_type_0.append(habits_type_0_item)

                return habits_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Habit] | None, data)

        habits = _parse_habits(d.pop("habits"))


        schema = d.pop("$schema", UNSET)

        habits_response = cls(
            habits=habits,
            schema=schema,
        )

        return habits_response

