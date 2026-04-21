from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="AcknowledgeAllProjectNotificationsOutputBody")



@_attrs_define
class AcknowledgeAllProjectNotificationsOutputBody:
    """ 
        Attributes:
            acknowledged (int): Number of notifications acknowledged
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    acknowledged: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        acknowledged = self.acknowledged

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "acknowledged": acknowledged,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        acknowledged = d.pop("acknowledged")

        schema = d.pop("$schema", UNSET)

        acknowledge_all_project_notifications_output_body = cls(
            acknowledged=acknowledged,
            schema=schema,
        )

        return acknowledge_all_project_notifications_output_body

