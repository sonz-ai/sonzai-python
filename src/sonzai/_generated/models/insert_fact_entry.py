from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.insert_fact_entry_properties import InsertFactEntryProperties





T = TypeVar("T", bound="InsertFactEntry")



@_attrs_define
class InsertFactEntry:
    """ 
        Attributes:
            entity_type (str):
            label (str):
            properties (InsertFactEntryProperties):
     """

    entity_type: str
    label: str
    properties: InsertFactEntryProperties





    def to_dict(self) -> dict[str, Any]:
        from ..models.insert_fact_entry_properties import InsertFactEntryProperties
        entity_type = self.entity_type

        label = self.label

        properties = self.properties.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "entity_type": entity_type,
            "label": label,
            "properties": properties,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.insert_fact_entry_properties import InsertFactEntryProperties
        d = dict(src_dict)
        entity_type = d.pop("entity_type")

        label = d.pop("label")

        properties = InsertFactEntryProperties.from_dict(d.pop("properties"))




        insert_fact_entry = cls(
            entity_type=entity_type,
            label=label,
            properties=properties,
        )

        return insert_fact_entry

