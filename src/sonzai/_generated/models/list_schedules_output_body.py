from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.schedule_dto import ScheduleDTO





T = TypeVar("T", bound="ListSchedulesOutputBody")



@_attrs_define
class ListSchedulesOutputBody:
    """ 
        Attributes:
            schedules (list[ScheduleDTO] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    schedules: list[ScheduleDTO] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.schedule_dto import ScheduleDTO
        schedules: list[dict[str, Any]] | None
        if isinstance(self.schedules, list):
            schedules = []
            for schedules_type_0_item_data in self.schedules:
                schedules_type_0_item = schedules_type_0_item_data.to_dict()
                schedules.append(schedules_type_0_item)


        else:
            schedules = self.schedules

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "schedules": schedules,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schedule_dto import ScheduleDTO
        d = dict(src_dict)
        def _parse_schedules(data: object) -> list[ScheduleDTO] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                schedules_type_0 = []
                _schedules_type_0 = data
                for schedules_type_0_item_data in (_schedules_type_0):
                    schedules_type_0_item = ScheduleDTO.from_dict(schedules_type_0_item_data)



                    schedules_type_0.append(schedules_type_0_item)

                return schedules_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ScheduleDTO] | None, data)

        schedules = _parse_schedules(d.pop("schedules"))


        schema = d.pop("$schema", UNSET)

        list_schedules_output_body = cls(
            schedules=schedules,
            schema=schema,
        )

        return list_schedules_output_body

