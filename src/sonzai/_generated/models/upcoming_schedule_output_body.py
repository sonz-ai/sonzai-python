from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpcomingScheduleOutputBody")



@_attrs_define
class UpcomingScheduleOutputBody:
    """ 
        Attributes:
            upcoming (list[str] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    upcoming: list[str] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        upcoming: list[str] | None
        if isinstance(self.upcoming, list):
            upcoming = self.upcoming


        else:
            upcoming = self.upcoming

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "upcoming": upcoming,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_upcoming(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                upcoming_type_0 = cast(list[str], data)

                return upcoming_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        upcoming = _parse_upcoming(d.pop("upcoming"))


        schema = d.pop("$schema", UNSET)

        upcoming_schedule_output_body = cls(
            upcoming=upcoming,
            schema=schema,
        )

        return upcoming_schedule_output_body

