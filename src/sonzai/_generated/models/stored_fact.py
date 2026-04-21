from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.stored_fact_metadata import StoredFactMetadata





T = TypeVar("T", bound="StoredFact")



@_attrs_define
class StoredFact:
    """
        Attributes:
            confidence (float):
            content (str):
            created_at (str):
            fact_id (str):
            fact_type (str):
            importance (float):
            mention_count (int):
            updated_at (str):
            entity (str | Unset):
            metadata (StoredFactMetadata | Unset):
            session_id (str | Unset):
            source_id (str | Unset):
            source_type (str | Unset):
     """

    confidence: float
    content: str
    created_at: str
    fact_id: str
    fact_type: str
    importance: float
    mention_count: int
    updated_at: str
    entity: str | Unset = UNSET
    metadata: StoredFactMetadata | Unset = UNSET
    session_id: str | Unset = UNSET
    source_id: str | Unset = UNSET
    source_type: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.stored_fact_metadata import StoredFactMetadata
        confidence = self.confidence

        content = self.content

        created_at = self.created_at

        fact_id = self.fact_id

        fact_type = self.fact_type

        importance = self.importance

        mention_count = self.mention_count

        updated_at = self.updated_at

        entity = self.entity

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        session_id = self.session_id

        source_id = self.source_id

        source_type = self.source_type


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "confidence": confidence,
            "content": content,
            "created_at": created_at,
            "fact_id": fact_id,
            "fact_type": fact_type,
            "importance": importance,
            "mention_count": mention_count,
            "updated_at": updated_at,
        })
        if entity is not UNSET:
            field_dict["entity"] = entity
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if source_id is not UNSET:
            field_dict["source_id"] = source_id
        if source_type is not UNSET:
            field_dict["source_type"] = source_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.stored_fact_metadata import StoredFactMetadata
        d = dict(src_dict)
        confidence = d.pop("confidence")

        content = d.pop("content")

        created_at = d.pop("created_at")

        fact_id = d.pop("fact_id")

        fact_type = d.pop("fact_type")

        importance = d.pop("importance")

        mention_count = d.pop("mention_count")

        updated_at = d.pop("updated_at")

        entity = d.pop("entity", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: StoredFactMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = StoredFactMetadata.from_dict(_metadata)




        session_id = d.pop("session_id", UNSET)

        source_id = d.pop("source_id", UNSET)

        source_type = d.pop("source_type", UNSET)

        stored_fact = cls(
            confidence=confidence,
            content=content,
            created_at=created_at,
            fact_id=fact_id,
            fact_type=fact_type,
            importance=importance,
            mention_count=mention_count,
            updated_at=updated_at,
            entity=entity,
            metadata=metadata,
            session_id=session_id,
            source_id=source_id,
            source_type=source_type,
        )

        return stored_fact

