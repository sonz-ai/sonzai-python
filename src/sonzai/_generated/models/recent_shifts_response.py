from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.personality_shift import PersonalityShift





T = TypeVar("T", bound="RecentShiftsResponse")



@_attrs_define
class RecentShiftsResponse:
    """ 
        Attributes:
            shifts (list[PersonalityShift] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    shifts: list[PersonalityShift] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.personality_shift import PersonalityShift
        shifts: list[dict[str, Any]] | None
        if isinstance(self.shifts, list):
            shifts = []
            for shifts_type_0_item_data in self.shifts:
                shifts_type_0_item = shifts_type_0_item_data.to_dict()
                shifts.append(shifts_type_0_item)


        else:
            shifts = self.shifts

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "shifts": shifts,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.personality_shift import PersonalityShift
        d = dict(src_dict)
        def _parse_shifts(data: object) -> list[PersonalityShift] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                shifts_type_0 = []
                _shifts_type_0 = data
                for shifts_type_0_item_data in (_shifts_type_0):
                    shifts_type_0_item = PersonalityShift.from_dict(shifts_type_0_item_data)



                    shifts_type_0.append(shifts_type_0_item)

                return shifts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PersonalityShift] | None, data)

        shifts = _parse_shifts(d.pop("shifts"))


        schema = d.pop("$schema", UNSET)

        recent_shifts_response = cls(
            shifts=shifts,
            schema=schema,
        )

        return recent_shifts_response

