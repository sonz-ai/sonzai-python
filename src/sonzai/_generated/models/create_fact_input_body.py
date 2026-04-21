from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_fact_input_body_metadata import CreateFactInputBodyMetadata





T = TypeVar("T", bound="CreateFactInputBody")



@_attrs_define
class CreateFactInputBody:
    """ 
        Attributes:
            content (str): Fact content text
            fact_type (str): Fact type (defaults to user_fact)
            schema (str | Unset): A URL to the JSON Schema for this object.
            confidence (float | Unset): Confidence score (0.0-1.0)
            entities (list[str] | None | Unset): Related entity names
            importance (float | Unset): Importance score (0.0-1.0)
            metadata (CreateFactInputBodyMetadata | Unset): Arbitrary metadata
            node_id (str | Unset): Memory tree node ID
            user_id (str | Unset): User ID (required unless metadata.scope=agent_global)
     """

    content: str
    fact_type: str
    schema: str | Unset = UNSET
    confidence: float | Unset = UNSET
    entities: list[str] | None | Unset = UNSET
    importance: float | Unset = UNSET
    metadata: CreateFactInputBodyMetadata | Unset = UNSET
    node_id: str | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_fact_input_body_metadata import CreateFactInputBodyMetadata
        content = self.content

        fact_type = self.fact_type

        schema = self.schema

        confidence = self.confidence

        entities: list[str] | None | Unset
        if isinstance(self.entities, Unset):
            entities = UNSET
        elif isinstance(self.entities, list):
            entities = self.entities


        else:
            entities = self.entities

        importance = self.importance

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        node_id = self.node_id

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
            "fact_type": fact_type,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if entities is not UNSET:
            field_dict["entities"] = entities
        if importance is not UNSET:
            field_dict["importance"] = importance
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if node_id is not UNSET:
            field_dict["node_id"] = node_id
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_fact_input_body_metadata import CreateFactInputBodyMetadata
        d = dict(src_dict)
        content = d.pop("content")

        fact_type = d.pop("fact_type")

        schema = d.pop("$schema", UNSET)

        confidence = d.pop("confidence", UNSET)

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


        importance = d.pop("importance", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: CreateFactInputBodyMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = CreateFactInputBodyMetadata.from_dict(_metadata)




        node_id = d.pop("node_id", UNSET)

        user_id = d.pop("user_id", UNSET)

        create_fact_input_body = cls(
            content=content,
            fact_type=fact_type,
            schema=schema,
            confidence=confidence,
            entities=entities,
            importance=importance,
            metadata=metadata,
            node_id=node_id,
            user_id=user_id,
        )

        return create_fact_input_body

