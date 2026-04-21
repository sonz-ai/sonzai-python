from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ColumnMappingSpec")



@_attrs_define
class ColumnMappingSpec:
    """ 
        Attributes:
            property_ (str):
            is_label (bool | Unset):
            type_ (str | Unset):
     """

    property_: str
    is_label: bool | Unset = UNSET
    type_: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        property_ = self.property_

        is_label = self.is_label

        type_ = self.type_


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "property": property_,
        })
        if is_label is not UNSET:
            field_dict["is_label"] = is_label
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        property_ = d.pop("property")

        is_label = d.pop("is_label", UNSET)

        type_ = d.pop("type", UNSET)

        column_mapping_spec = cls(
            property_=property_,
            is_label=is_label,
            type_=type_,
        )

        return column_mapping_spec

