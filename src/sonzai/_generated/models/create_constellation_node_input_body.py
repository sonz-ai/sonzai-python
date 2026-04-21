from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateConstellationNodeInputBody")



@_attrs_define
class CreateConstellationNodeInputBody:
    """ 
        Attributes:
            label (str): Node label (must be unique per agent+user)
            schema (str | Unset): A URL to the JSON Schema for this object.
            description (str | Unset): Human-readable description
            node_type (str | Unset): Node type (defaults to theme)
            significance (float | Unset): Significance score (0-1, defaults to 0.5)
            user_id (str | Unset): Optional user ID for per-user nodes
     """

    label: str
    schema: str | Unset = UNSET
    description: str | Unset = UNSET
    node_type: str | Unset = UNSET
    significance: float | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        label = self.label

        schema = self.schema

        description = self.description

        node_type = self.node_type

        significance = self.significance

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "label": label,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description
        if node_type is not UNSET:
            field_dict["node_type"] = node_type
        if significance is not UNSET:
            field_dict["significance"] = significance
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        schema = d.pop("$schema", UNSET)

        description = d.pop("description", UNSET)

        node_type = d.pop("node_type", UNSET)

        significance = d.pop("significance", UNSET)

        user_id = d.pop("user_id", UNSET)

        create_constellation_node_input_body = cls(
            label=label,
            schema=schema,
            description=description,
            node_type=node_type,
            significance=significance,
            user_id=user_id,
        )

        return create_constellation_node_input_body

