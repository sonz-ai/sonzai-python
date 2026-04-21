from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateConstellationNodeInputBody")



@_attrs_define
class UpdateConstellationNodeInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            description (str | Unset): Updated description
            label (str | Unset): Updated label
            node_type (str | Unset): Updated node type
            significance (float | Unset): Updated significance (0-1)
     """

    schema: str | Unset = UNSET
    description: str | Unset = UNSET
    label: str | Unset = UNSET
    node_type: str | Unset = UNSET
    significance: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        description = self.description

        label = self.label

        node_type = self.node_type

        significance = self.significance


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description
        if label is not UNSET:
            field_dict["label"] = label
        if node_type is not UNSET:
            field_dict["node_type"] = node_type
        if significance is not UNSET:
            field_dict["significance"] = significance

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        description = d.pop("description", UNSET)

        label = d.pop("label", UNSET)

        node_type = d.pop("node_type", UNSET)

        significance = d.pop("significance", UNSET)

        update_constellation_node_input_body = cls(
            schema=schema,
            description=description,
            label=label,
            node_type=node_type,
            significance=significance,
        )

        return update_constellation_node_input_body

