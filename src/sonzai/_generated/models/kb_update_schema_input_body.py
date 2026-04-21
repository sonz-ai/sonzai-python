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





T = TypeVar("T", bound="KbUpdateSchemaInputBody")



@_attrs_define
class KbUpdateSchemaInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            description (str | Unset): Updated description
            entity_type (str | Unset): Updated entity type name
            fields (list[KBSchemaField] | None | Unset): Updated field definitions
            similarity_config (KBSimilarityConfig | Unset):
     """

    schema: str | Unset = UNSET
    description: str | Unset = UNSET
    entity_type: str | Unset = UNSET
    fields: list[KBSchemaField] | None | Unset = UNSET
    similarity_config: KBSimilarityConfig | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_schema_field import KBSchemaField
        from ..models.kb_similarity_config import KBSimilarityConfig
        schema = self.schema

        description = self.description

        entity_type = self.entity_type

        fields: list[dict[str, Any]] | None | Unset
        if isinstance(self.fields, Unset):
            fields = UNSET
        elif isinstance(self.fields, list):
            fields = []
            for fields_type_0_item_data in self.fields:
                fields_type_0_item = fields_type_0_item_data.to_dict()
                fields.append(fields_type_0_item)


        else:
            fields = self.fields

        similarity_config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.similarity_config, Unset):
            similarity_config = self.similarity_config.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description
        if entity_type is not UNSET:
            field_dict["entity_type"] = entity_type
        if fields is not UNSET:
            field_dict["fields"] = fields
        if similarity_config is not UNSET:
            field_dict["similarity_config"] = similarity_config

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_schema_field import KBSchemaField
        from ..models.kb_similarity_config import KBSimilarityConfig
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        description = d.pop("description", UNSET)

        entity_type = d.pop("entity_type", UNSET)

        def _parse_fields(data: object) -> list[KBSchemaField] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
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
            return cast(list[KBSchemaField] | None | Unset, data)

        fields = _parse_fields(d.pop("fields", UNSET))


        _similarity_config = d.pop("similarity_config", UNSET)
        similarity_config: KBSimilarityConfig | Unset
        if isinstance(_similarity_config,  Unset):
            similarity_config = UNSET
        else:
            similarity_config = KBSimilarityConfig.from_dict(_similarity_config)




        kb_update_schema_input_body = cls(
            schema=schema,
            description=description,
            entity_type=entity_type,
            fields=fields,
            similarity_config=similarity_config,
        )

        return kb_update_schema_input_body

