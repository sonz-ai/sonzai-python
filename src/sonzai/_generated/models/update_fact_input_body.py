from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.update_fact_input_body_metadata import UpdateFactInputBodyMetadata





T = TypeVar("T", bound="UpdateFactInputBody")



@_attrs_define
class UpdateFactInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            confidence (float | Unset): Updated confidence score
            content (str | Unset): Updated content text
            entities (list[str] | None | Unset): Updated entity names
            fact_type (str | Unset): Updated fact type
            importance (float | Unset): Updated importance score
            metadata (UpdateFactInputBodyMetadata | Unset): Metadata fields to merge
     """

    schema: str | Unset = UNSET
    confidence: float | Unset = UNSET
    content: str | Unset = UNSET
    entities: list[str] | None | Unset = UNSET
    fact_type: str | Unset = UNSET
    importance: float | Unset = UNSET
    metadata: UpdateFactInputBodyMetadata | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_fact_input_body_metadata import UpdateFactInputBodyMetadata
        schema = self.schema

        confidence = self.confidence

        content = self.content

        entities: list[str] | None | Unset
        if isinstance(self.entities, Unset):
            entities = UNSET
        elif isinstance(self.entities, list):
            entities = self.entities


        else:
            entities = self.entities

        fact_type = self.fact_type

        importance = self.importance

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if content is not UNSET:
            field_dict["content"] = content
        if entities is not UNSET:
            field_dict["entities"] = entities
        if fact_type is not UNSET:
            field_dict["fact_type"] = fact_type
        if importance is not UNSET:
            field_dict["importance"] = importance
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_fact_input_body_metadata import UpdateFactInputBodyMetadata
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        confidence = d.pop("confidence", UNSET)

        content = d.pop("content", UNSET)

        def _parse_entities(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                entities_type_0 = cast(list[str], data)

                return entities_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        entities = _parse_entities(d.pop("entities", UNSET))


        fact_type = d.pop("fact_type", UNSET)

        importance = d.pop("importance", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: UpdateFactInputBodyMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = UpdateFactInputBodyMetadata.from_dict(_metadata)




        update_fact_input_body = cls(
            schema=schema,
            confidence=confidence,
            content=content,
            entities=entities,
            fact_type=fact_type,
            importance=importance,
            metadata=metadata,
        )

        return update_fact_input_body

