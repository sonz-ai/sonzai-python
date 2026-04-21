from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ScheduleDTO")



@_attrs_define
class ScheduleDTO:
    """ 
        Attributes:
            cadence (str):
            cadence_type (str):
            check_type (str):
            created_at (str):
            enabled (bool):
            intent (str):
            next_fire_at (str):
            schedule_id (str):
            timezone (str):
            updated_at (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            active_window (str | Unset):
            ends_at (str | Unset):
            inventory_item_id (str | Unset):
            metadata (str | Unset):
            starts_at (str | Unset):
     """

    cadence: str
    cadence_type: str
    check_type: str
    created_at: str
    enabled: bool
    intent: str
    next_fire_at: str
    schedule_id: str
    timezone: str
    updated_at: str
    schema: str | Unset = UNSET
    active_window: str | Unset = UNSET
    ends_at: str | Unset = UNSET
    inventory_item_id: str | Unset = UNSET
    metadata: str | Unset = UNSET
    starts_at: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        cadence = self.cadence

        cadence_type = self.cadence_type

        check_type = self.check_type

        created_at = self.created_at

        enabled = self.enabled

        intent = self.intent

        next_fire_at = self.next_fire_at

        schedule_id = self.schedule_id

        timezone = self.timezone

        updated_at = self.updated_at

        schema = self.schema

        active_window = self.active_window

        ends_at = self.ends_at

        inventory_item_id = self.inventory_item_id

        metadata = self.metadata

        starts_at = self.starts_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "cadence": cadence,
            "cadence_type": cadence_type,
            "check_type": check_type,
            "created_at": created_at,
            "enabled": enabled,
            "intent": intent,
            "next_fire_at": next_fire_at,
            "schedule_id": schedule_id,
            "timezone": timezone,
            "updated_at": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if active_window is not UNSET:
            field_dict["active_window"] = active_window
        if ends_at is not UNSET:
            field_dict["ends_at"] = ends_at
        if inventory_item_id is not UNSET:
            field_dict["inventory_item_id"] = inventory_item_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if starts_at is not UNSET:
            field_dict["starts_at"] = starts_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cadence = d.pop("cadence")

        cadence_type = d.pop("cadence_type")

        check_type = d.pop("check_type")

        created_at = d.pop("created_at")

        enabled = d.pop("enabled")

        intent = d.pop("intent")

        next_fire_at = d.pop("next_fire_at")

        schedule_id = d.pop("schedule_id")

        timezone = d.pop("timezone")

        updated_at = d.pop("updated_at")

        schema = d.pop("$schema", UNSET)

        active_window = d.pop("active_window", UNSET)

        ends_at = d.pop("ends_at", UNSET)

        inventory_item_id = d.pop("inventory_item_id", UNSET)

        metadata = d.pop("metadata", UNSET)

        starts_at = d.pop("starts_at", UNSET)

        schedule_dto = cls(
            cadence=cadence,
            cadence_type=cadence_type,
            check_type=check_type,
            created_at=created_at,
            enabled=enabled,
            intent=intent,
            next_fire_at=next_fire_at,
            schedule_id=schedule_id,
            timezone=timezone,
            updated_at=updated_at,
            schema=schema,
            active_window=active_window,
            ends_at=ends_at,
            inventory_item_id=inventory_item_id,
            metadata=metadata,
            starts_at=starts_at,
        )

        return schedule_dto

