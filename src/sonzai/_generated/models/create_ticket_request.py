from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateTicketRequest")



@_attrs_define
class CreateTicketRequest:
    """ 
        Attributes:
            description (str):
            title (str):
            type_ (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            priority (str | Unset):
     """

    description: str
    title: str
    type_: str
    schema: str | Unset = UNSET
    priority: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        title = self.title

        type_ = self.type_

        schema = self.schema

        priority = self.priority


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "description": description,
            "title": title,
            "type": type_,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if priority is not UNSET:
            field_dict["priority"] = priority

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        title = d.pop("title")

        type_ = d.pop("type")

        schema = d.pop("$schema", UNSET)

        priority = d.pop("priority", UNSET)

        create_ticket_request = cls(
            description=description,
            title=title,
            type_=type_,
            schema=schema,
            priority=priority,
        )

        return create_ticket_request

