from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateScheduleInputBody")



@_attrs_define
class CreateScheduleInputBody:
    """ 
        Attributes:
            cadence (Any): Cadence spec: {simple:{...}}|{cron:"..."} with required timezone field.
            check_type (str):
            intent (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            active_window (Any | Unset): Optional quiet-hours/days filter: {hours:{start,end},days_of_week}.
            ends_at (str | Unset): RFC3339.
            inventory_item_id (str | Unset):
            metadata (Any | Unset):
            starts_at (str | Unset): RFC3339.
     """

    cadence: Any
    check_type: str
    intent: str
    schema: str | Unset = UNSET
    active_window: Any | Unset = UNSET
    ends_at: str | Unset = UNSET
    inventory_item_id: str | Unset = UNSET
    metadata: Any | Unset = UNSET
    starts_at: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        cadence = self.cadence

        check_type = self.check_type

        intent = self.intent

        schema = self.schema

        active_window = self.active_window

        ends_at = self.ends_at

        inventory_item_id = self.inventory_item_id

        metadata = self.metadata

        starts_at = self.starts_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "cadence": cadence,
            "check_type": check_type,
            "intent": intent,
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

        check_type = d.pop("check_type")

        intent = d.pop("intent")

        schema = d.pop("$schema", UNSET)

        active_window = d.pop("active_window", UNSET)

        ends_at = d.pop("ends_at", UNSET)

        inventory_item_id = d.pop("inventory_item_id", UNSET)

        metadata = d.pop("metadata", UNSET)

        starts_at = d.pop("starts_at", UNSET)

        create_schedule_input_body = cls(
            cadence=cadence,
            check_type=check_type,
            intent=intent,
            schema=schema,
            active_window=active_window,
            ends_at=ends_at,
            inventory_item_id=inventory_item_id,
            metadata=metadata,
            starts_at=starts_at,
        )

        return create_schedule_input_body

