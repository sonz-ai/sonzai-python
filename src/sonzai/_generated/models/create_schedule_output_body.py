from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateScheduleOutputBody")



@_attrs_define
class CreateScheduleOutputBody:
    """ 
        Attributes:
            enabled (bool):
            next_fire_at (str):
            next_fire_at_local (str):
            schedule_id (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    enabled: bool
    next_fire_at: str
    next_fire_at_local: str
    schedule_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        next_fire_at = self.next_fire_at

        next_fire_at_local = self.next_fire_at_local

        schedule_id = self.schedule_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "enabled": enabled,
            "next_fire_at": next_fire_at,
            "next_fire_at_local": next_fire_at_local,
            "schedule_id": schedule_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        next_fire_at = d.pop("next_fire_at")

        next_fire_at_local = d.pop("next_fire_at_local")

        schedule_id = d.pop("schedule_id")

        schema = d.pop("$schema", UNSET)

        create_schedule_output_body = cls(
            enabled=enabled,
            next_fire_at=next_fire_at,
            next_fire_at_local=next_fire_at_local,
            schedule_id=schedule_id,
            schema=schema,
        )

        return create_schedule_output_body

