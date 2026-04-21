from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_create_org_node_input_body_properties import KbCreateOrgNodeInputBodyProperties





T = TypeVar("T", bound="KbCreateOrgNodeInputBody")



@_attrs_define
class KbCreateOrgNodeInputBody:
    """ 
        Attributes:
            label (str): Human-readable display label
            node_type (str): Open-string entity type (policy, product, playbook, ...)
            schema (str | Unset): A URL to the JSON Schema for this object.
            confidence (float | Unset): Optional 0.0–1.0 confidence; default 1.0 for hand-authored org knowledge
            properties (KbCreateOrgNodeInputBodyProperties | Unset): Flexible key-value payload
     """

    label: str
    node_type: str
    schema: str | Unset = UNSET
    confidence: float | Unset = UNSET
    properties: KbCreateOrgNodeInputBodyProperties | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_create_org_node_input_body_properties import KbCreateOrgNodeInputBodyProperties
        label = self.label

        node_type = self.node_type

        schema = self.schema

        confidence = self.confidence

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "label": label,
            "node_type": node_type,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_create_org_node_input_body_properties import KbCreateOrgNodeInputBodyProperties
        d = dict(src_dict)
        label = d.pop("label")

        node_type = d.pop("node_type")

        schema = d.pop("$schema", UNSET)

        confidence = d.pop("confidence", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: KbCreateOrgNodeInputBodyProperties | Unset
        if isinstance(_properties,  Unset):
            properties = UNSET
        else:
            properties = KbCreateOrgNodeInputBodyProperties.from_dict(_properties)




        kb_create_org_node_input_body = cls(
            label=label,
            node_type=node_type,
            schema=schema,
            confidence=confidence,
            properties=properties,
        )

        return kb_create_org_node_input_body

