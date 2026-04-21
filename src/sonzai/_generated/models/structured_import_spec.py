from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.structured_import_spec_column_mapping import StructuredImportSpecColumnMapping





T = TypeVar("T", bound="StructuredImportSpec")



@_attrs_define
class StructuredImportSpec:
    """ 
        Attributes:
            column_mapping (StructuredImportSpecColumnMapping):
            content_csv (str):
            entity_type (str):
            project_id (str | Unset):
     """

    column_mapping: StructuredImportSpecColumnMapping
    content_csv: str
    entity_type: str
    project_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.structured_import_spec_column_mapping import StructuredImportSpecColumnMapping
        column_mapping = self.column_mapping.to_dict()

        content_csv = self.content_csv

        entity_type = self.entity_type

        project_id = self.project_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "column_mapping": column_mapping,
            "content_csv": content_csv,
            "entity_type": entity_type,
        })
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.structured_import_spec_column_mapping import StructuredImportSpecColumnMapping
        d = dict(src_dict)
        column_mapping = StructuredImportSpecColumnMapping.from_dict(d.pop("column_mapping"))




        content_csv = d.pop("content_csv")

        entity_type = d.pop("entity_type")

        project_id = d.pop("project_id", UNSET)

        structured_import_spec = cls(
            column_mapping=column_mapping,
            content_csv=content_csv,
            entity_type=entity_type,
            project_id=project_id,
        )

        return structured_import_spec

