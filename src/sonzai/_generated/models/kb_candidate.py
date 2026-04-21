from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_candidate_properties import KbCandidateProperties





T = TypeVar("T", bound="KbCandidate")



@_attrs_define
class KbCandidate:
    """ 
        Attributes:
            kb_node_id (str):
            label (str):
            properties (KbCandidateProperties | Unset):
     """

    kb_node_id: str
    label: str
    properties: KbCandidateProperties | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_candidate_properties import KbCandidateProperties
        kb_node_id = self.kb_node_id

        label = self.label

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kb_node_id": kb_node_id,
            "label": label,
        })
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_candidate_properties import KbCandidateProperties
        d = dict(src_dict)
        kb_node_id = d.pop("kb_node_id")

        label = d.pop("label")

        _properties = d.pop("properties", UNSET)
        properties: KbCandidateProperties | Unset
        if isinstance(_properties,  Unset):
            properties = UNSET
        else:
            properties = KbCandidateProperties.from_dict(_properties)




        kb_candidate = cls(
            kb_node_id=kb_node_id,
            label=label,
            properties=properties,
        )

        return kb_candidate

