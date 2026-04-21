from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="KBSchemaField")



@_attrs_define
class KBSchemaField:
    """ 
        Attributes:
            name (str):
            required (bool):
            type_ (str):
            description (str | Unset):
            enum_values (list[str] | None | Unset):
     """

    name: str
    required: bool
    type_: str
    description: str | Unset = UNSET
    enum_values: list[str] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        required = self.required

        type_ = self.type_

        description = self.description

        enum_values: list[str] | None | Unset
        if isinstance(self.enum_values, Unset):
            enum_values = UNSET
        elif isinstance(self.enum_values, list):
            enum_values = self.enum_values


        else:
            enum_values = self.enum_values


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "required": required,
            "type": type_,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if enum_values is not UNSET:
            field_dict["enum_values"] = enum_values

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        required = d.pop("required")

        type_ = d.pop("type")

        description = d.pop("description", UNSET)

        def _parse_enum_values(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                enum_values_type_0 = cast(list[str], data)

                return enum_values_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        enum_values = _parse_enum_values(d.pop("enum_values", UNSET))


        kb_schema_field = cls(
            name=name,
            required=required,
            type_=type_,
            description=description,
            enum_values=enum_values,
        )

        return kb_schema_field

