from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_resolution_info_kb_properties import KbResolutionInfoKbProperties





T = TypeVar("T", bound="KbResolutionInfo")



@_attrs_define
class KbResolutionInfo:
    """ 
        Attributes:
            resolved (bool):
            kb_label (str | Unset):
            kb_node_id (str | Unset):
            kb_properties (KbResolutionInfoKbProperties | Unset):
     """

    resolved: bool
    kb_label: str | Unset = UNSET
    kb_node_id: str | Unset = UNSET
    kb_properties: KbResolutionInfoKbProperties | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_resolution_info_kb_properties import KbResolutionInfoKbProperties
        resolved = self.resolved

        kb_label = self.kb_label

        kb_node_id = self.kb_node_id

        kb_properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.kb_properties, Unset):
            kb_properties = self.kb_properties.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "resolved": resolved,
        })
        if kb_label is not UNSET:
            field_dict["kb_label"] = kb_label
        if kb_node_id is not UNSET:
            field_dict["kb_node_id"] = kb_node_id
        if kb_properties is not UNSET:
            field_dict["kb_properties"] = kb_properties

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_resolution_info_kb_properties import KbResolutionInfoKbProperties
        d = dict(src_dict)
        resolved = d.pop("resolved")

        kb_label = d.pop("kb_label", UNSET)

        kb_node_id = d.pop("kb_node_id", UNSET)

        _kb_properties = d.pop("kb_properties", UNSET)
        kb_properties: KbResolutionInfoKbProperties | Unset
        if isinstance(_kb_properties,  Unset):
            kb_properties = UNSET
        else:
            kb_properties = KbResolutionInfoKbProperties.from_dict(_kb_properties)




        kb_resolution_info = cls(
            resolved=resolved,
            kb_label=kb_label,
            kb_node_id=kb_node_id,
            kb_properties=kb_properties,
        )

        return kb_resolution_info

