from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="PatchScheduleInputBody")



@_attrs_define
class PatchScheduleInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            active_window (Any | Unset):
            cadence (Any | Unset):
            check_type (str | Unset):
            enabled (bool | Unset):
            ends_at (str | Unset):
            intent (str | Unset):
            metadata (Any | Unset):
            starts_at (str | Unset):
     """

    schema: str | Unset = UNSET
    active_window: Any | Unset = UNSET
    cadence: Any | Unset = UNSET
    check_type: str | Unset = UNSET
    enabled: bool | Unset = UNSET
    ends_at: str | Unset = UNSET
    intent: str | Unset = UNSET
    metadata: Any | Unset = UNSET
    starts_at: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        active_window = self.active_window

        cadence = self.cadence

        check_type = self.check_type

        enabled = self.enabled

        ends_at = self.ends_at

        intent = self.intent

        metadata = self.metadata

        starts_at = self.starts_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if active_window is not UNSET:
            field_dict["active_window"] = active_window
        if cadence is not UNSET:
            field_dict["cadence"] = cadence
        if check_type is not UNSET:
            field_dict["check_type"] = check_type
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if ends_at is not UNSET:
            field_dict["ends_at"] = ends_at
        if intent is not UNSET:
            field_dict["intent"] = intent
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if starts_at is not UNSET:
            field_dict["starts_at"] = starts_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        active_window = d.pop("active_window", UNSET)

        cadence = d.pop("cadence", UNSET)

        check_type = d.pop("check_type", UNSET)

        enabled = d.pop("enabled", UNSET)

        ends_at = d.pop("ends_at", UNSET)

        intent = d.pop("intent", UNSET)

        metadata = d.pop("metadata", UNSET)

        starts_at = d.pop("starts_at", UNSET)

        patch_schedule_input_body = cls(
            schema=schema,
            active_window=active_window,
            cadence=cadence,
            check_type=check_type,
            enabled=enabled,
            ends_at=ends_at,
            intent=intent,
            metadata=metadata,
            starts_at=starts_at,
        )

        return patch_schedule_input_body

