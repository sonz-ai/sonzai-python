from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="InsertFactDetail")



@_attrs_define
class InsertFactDetail:
    """ 
        Attributes:
            action (str):
            label (str):
            node_id (str):
            type_ (str):
            version (int):
     """

    action: str
    label: str
    node_id: str
    type_: str
    version: int





    def to_dict(self) -> dict[str, Any]:
        action = self.action

        label = self.label

        node_id = self.node_id

        type_ = self.type_

        version = self.version


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "action": action,
            "label": label,
            "node_id": node_id,
            "type": type_,
            "version": version,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = d.pop("action")

        label = d.pop("label")

        node_id = d.pop("node_id")

        type_ = d.pop("type")

        version = d.pop("version")

        insert_fact_detail = cls(
            action=action,
            label=label,
            node_id=node_id,
            type_=type_,
            version=version,
        )

        return insert_fact_detail

