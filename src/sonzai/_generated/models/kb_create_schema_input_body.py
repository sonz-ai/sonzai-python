from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_schema_field import KBSchemaField
  from ..models.kb_similarity_config import KBSimilarityConfig





T = TypeVar("T", bound="KbCreateSchemaInputBody")



@_attrs_define
class KbCreateSchemaInputBody:
    """ 
        Attributes:
            entity_type (str): Entity type name
            fields (list[KBSchemaField] | None): Schema field definitions
            schema (str | Unset): A URL to the JSON Schema for this object.
            description (str | Unset): Human-readable description
            similarity_config (KBSimilarityConfig | Unset):
     """

    entity_type: str
    fields: list[KBSchemaField] | None
    schema: str | Unset = UNSET
    description: str | Unset = UNSET
    similarity_config: KBSimilarityConfig | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_schema_field import KBSchemaField
        from ..models.kb_similarity_config import KBSimilarityConfig
        entity_type = self.entity_type

        fields: list[dict[str, Any]] | None
        if isinstance(self.fields, list):
            fields = []
            for fields_type_0_item_data in self.fields:
                fields_type_0_item = fields_type_0_item_data.to_dict()
                fields.append(fields_type_0_item)


        else:
            fields = self.fields

        schema = self.schema

        description = self.description

        similarity_config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.similarity_config, Unset):
            similarity_config = self.similarity_config.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "entity_type": entity_type,
            "fields": fields,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description
        if similarity_config is not UNSET:
            field_dict["similarity_config"] = similarity_config

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_schema_field import KBSchemaField
        from ..models.kb_similarity_config import KBSimilarityConfig
        d = dict(src_dict)
        entity_type = d.pop("entity_type")

        def _parse_fields(data: object) -> list[KBSchemaField] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                fields_type_0 = []
                _fields_type_0 = data
                for fields_type_0_item_data in (_fields_type_0):
                    fields_type_0_item = KBSchemaField.from_dict(fields_type_0_item_data)



                    fields_type_0.append(fields_type_0_item)

                return fields_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBSchemaField] | None, data)

        fields = _parse_fields(d.pop("fields"))


        schema = d.pop("$schema", UNSET)

        description = d.pop("description", UNSET)

        _similarity_config = d.pop("similarity_config", UNSET)
        similarity_config: KBSimilarityConfig | Unset
        if isinstance(_similarity_config,  Unset):
            similarity_config = UNSET
        else:
            similarity_config = KBSimilarityConfig.from_dict(_similarity_config)




        kb_create_schema_input_body = cls(
            entity_type=entity_type,
            fields=fields,
            schema=schema,
            description=description,
            similarity_config=similarity_config,
        )

        return kb_create_schema_input_body

