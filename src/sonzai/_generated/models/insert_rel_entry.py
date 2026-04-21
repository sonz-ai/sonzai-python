from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="InsertRelEntry")



@_attrs_define
class InsertRelEntry:
    """ 
        Attributes:
            edge_type (str):
            from_label (str):
            to_label (str):
     """

    edge_type: str
    from_label: str
    to_label: str





    def to_dict(self) -> dict[str, Any]:
        edge_type = self.edge_type

        from_label = self.from_label

        to_label = self.to_label


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "edge_type": edge_type,
            "from_label": from_label,
            "to_label": to_label,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        edge_type = d.pop("edge_type")

        from_label = d.pop("from_label")

        to_label = d.pop("to_label")

        insert_rel_entry = cls(
            edge_type=edge_type,
            from_label=from_label,
            to_label=to_label,
        )

        return insert_rel_entry

