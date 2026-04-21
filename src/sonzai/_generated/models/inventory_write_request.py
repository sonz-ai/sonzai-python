from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.inventory_write_request_properties import InventoryWriteRequestProperties





T = TypeVar("T", bound="InventoryWriteRequest")



@_attrs_define
class InventoryWriteRequest:
    """ 
        Attributes:
            action (str):
            item_type (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            description (str | Unset):
            kb_node_id (str | Unset):
            project_id (str | Unset):
            properties (InventoryWriteRequestProperties | Unset):
     """

    action: str
    item_type: str
    schema: str | Unset = UNSET
    description: str | Unset = UNSET
    kb_node_id: str | Unset = UNSET
    project_id: str | Unset = UNSET
    properties: InventoryWriteRequestProperties | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.inventory_write_request_properties import InventoryWriteRequestProperties
        action = self.action

        item_type = self.item_type

        schema = self.schema

        description = self.description

        kb_node_id = self.kb_node_id

        project_id = self.project_id

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "action": action,
            "item_type": item_type,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description
        if kb_node_id is not UNSET:
            field_dict["kb_node_id"] = kb_node_id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inventory_write_request_properties import InventoryWriteRequestProperties
        d = dict(src_dict)
        action = d.pop("action")

        item_type = d.pop("item_type")

        schema = d.pop("$schema", UNSET)

        description = d.pop("description", UNSET)

        kb_node_id = d.pop("kb_node_id", UNSET)

        project_id = d.pop("project_id", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: InventoryWriteRequestProperties | Unset
        if isinstance(_properties,  Unset):
            properties = UNSET
        else:
            properties = InventoryWriteRequestProperties.from_dict(_properties)




        inventory_write_request = cls(
            action=action,
            item_type=item_type,
            schema=schema,
            description=description,
            kb_node_id=kb_node_id,
            project_id=project_id,
            properties=properties,
        )

        return inventory_write_request

