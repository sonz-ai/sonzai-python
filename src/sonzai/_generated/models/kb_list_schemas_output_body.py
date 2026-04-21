from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_entity_schema import KBEntitySchema





T = TypeVar("T", bound="KbListSchemasOutputBody")



@_attrs_define
class KbListSchemasOutputBody:
    """ 
        Attributes:
            schemas (list[KBEntitySchema] | None): List of schemas
            total (int): Total count
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    schemas: list[KBEntitySchema] | None
    total: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_entity_schema import KBEntitySchema
        schemas: list[dict[str, Any]] | None
        if isinstance(self.schemas, list):
            schemas = []
            for schemas_type_0_item_data in self.schemas:
                schemas_type_0_item = schemas_type_0_item_data.to_dict()
                schemas.append(schemas_type_0_item)


        else:
            schemas = self.schemas

        total = self.total

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "schemas": schemas,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_entity_schema import KBEntitySchema
        d = dict(src_dict)
        def _parse_schemas(data: object) -> list[KBEntitySchema] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                schemas_type_0 = []
                _schemas_type_0 = data
                for schemas_type_0_item_data in (_schemas_type_0):
                    schemas_type_0_item = KBEntitySchema.from_dict(schemas_type_0_item_data)



                    schemas_type_0.append(schemas_type_0_item)

                return schemas_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBEntitySchema] | None, data)

        schemas = _parse_schemas(d.pop("schemas"))


        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        kb_list_schemas_output_body = cls(
            schemas=schemas,
            total=total,
            schema=schema,
        )

        return kb_list_schemas_output_body

