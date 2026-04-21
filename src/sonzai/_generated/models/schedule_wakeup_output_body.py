from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ScheduleWakeupOutputBody")



@_attrs_define
class ScheduleWakeupOutputBody:
    """ 
        Attributes:
            scheduled_at (str): ISO 8601 timestamp when the wakeup is scheduled
            wakeup_id (str): Unique ID of the scheduled wakeup
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    scheduled_at: str
    wakeup_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        scheduled_at = self.scheduled_at

        wakeup_id = self.wakeup_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "scheduled_at": scheduled_at,
            "wakeup_id": wakeup_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scheduled_at = d.pop("scheduled_at")

        wakeup_id = d.pop("wakeup_id")

        schema = d.pop("$schema", UNSET)

        schedule_wakeup_output_body = cls(
            scheduled_at=scheduled_at,
            wakeup_id=wakeup_id,
            schema=schema,
        )

        return schedule_wakeup_output_body

