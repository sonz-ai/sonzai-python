from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.column_mapping_spec import ColumnMappingSpec





T = TypeVar("T", bound="StructuredImportSpecColumnMapping")



@_attrs_define
class StructuredImportSpecColumnMapping:
    """ 
     """

    additional_properties: dict[str, ColumnMappingSpec] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.column_mapping_spec import ColumnMappingSpec
        
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()


        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.column_mapping_spec import ColumnMappingSpec
        d = dict(src_dict)
        structured_import_spec_column_mapping = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ColumnMappingSpec.from_dict(prop_dict)



            additional_properties[prop_name] = additional_property

        structured_import_spec_column_mapping.additional_properties = additional_properties
        return structured_import_spec_column_mapping

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> ColumnMappingSpec:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: ColumnMappingSpec) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
