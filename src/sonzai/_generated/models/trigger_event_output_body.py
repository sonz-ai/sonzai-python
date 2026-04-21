from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="TriggerEventOutputBody")



@_attrs_define
class TriggerEventOutputBody:
    """ 
        Attributes:
            accepted (bool): Whether the event was accepted for processing
            event_id (str): Unique identifier for the accepted event
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    accepted: bool
    event_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        accepted = self.accepted

        event_id = self.event_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "accepted": accepted,
            "event_id": event_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        accepted = d.pop("accepted")

        event_id = d.pop("event_id")

        schema = d.pop("$schema", UNSET)

        trigger_event_output_body = cls(
            accepted=accepted,
            event_id=event_id,
            schema=schema,
        )

        return trigger_event_output_body

