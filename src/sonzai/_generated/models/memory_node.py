from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.memory_node_metadata import MemoryNodeMetadata





T = TypeVar("T", bound="MemoryNode")



@_attrs_define
class MemoryNode:
    """ 
        Attributes:
            agent_id (str):
            created_at (datetime.datetime):
            description (str):
            memory_type (str):
            name (str):
            node_id (str):
            path (str):
            updated_at (datetime.datetime):
            access_count (int | Unset):
            child_count (int | Unset):
            content_count (int | Unset):
            content_refs (list[str] | None | Unset):
            cross_refs (list[str] | None | Unset):
            depth (int | Unset):
            importance (float | Unset):
            is_deleted (bool | Unset):
            is_prunable (bool | Unset):
            last_accessed_at (datetime.datetime | Unset):
            metadata (MemoryNodeMetadata | Unset):
            parent_id (str | Unset):
            recency (float | Unset):
            user_id (str | Unset):
     """

    agent_id: str
    created_at: datetime.datetime
    description: str
    memory_type: str
    name: str
    node_id: str
    path: str
    updated_at: datetime.datetime
    access_count: int | Unset = UNSET
    child_count: int | Unset = UNSET
    content_count: int | Unset = UNSET
    content_refs: list[str] | None | Unset = UNSET
    cross_refs: list[str] | None | Unset = UNSET
    depth: int | Unset = UNSET
    importance: float | Unset = UNSET
    is_deleted: bool | Unset = UNSET
    is_prunable: bool | Unset = UNSET
    last_accessed_at: datetime.datetime | Unset = UNSET
    metadata: MemoryNodeMetadata | Unset = UNSET
    parent_id: str | Unset = UNSET
    recency: float | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.memory_node_metadata import MemoryNodeMetadata
        agent_id = self.agent_id

        created_at = self.created_at.isoformat()

        description = self.description

        memory_type = self.memory_type

        name = self.name

        node_id = self.node_id

        path = self.path

        updated_at = self.updated_at.isoformat()

        access_count = self.access_count

        child_count = self.child_count

        content_count = self.content_count

        content_refs: list[str] | None | Unset
        if isinstance(self.content_refs, Unset):
            content_refs = UNSET
        elif isinstance(self.content_refs, list):
            content_refs = self.content_refs


        else:
            content_refs = self.content_refs

        cross_refs: list[str] | None | Unset
        if isinstance(self.cross_refs, Unset):
            cross_refs = UNSET
        elif isinstance(self.cross_refs, list):
            cross_refs = self.cross_refs


        else:
            cross_refs = self.cross_refs

        depth = self.depth

        importance = self.importance

        is_deleted = self.is_deleted

        is_prunable = self.is_prunable

        last_accessed_at: str | Unset = UNSET
        if not isinstance(self.last_accessed_at, Unset):
            last_accessed_at = self.last_accessed_at.isoformat()

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        parent_id = self.parent_id

        recency = self.recency

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "created_at": created_at,
            "description": description,
            "memory_type": memory_type,
            "name": name,
            "node_id": node_id,
            "path": path,
            "updated_at": updated_at,
        })
        if access_count is not UNSET:
            field_dict["access_count"] = access_count
        if child_count is not UNSET:
            field_dict["child_count"] = child_count
        if content_count is not UNSET:
            field_dict["content_count"] = content_count
        if content_refs is not UNSET:
            field_dict["content_refs"] = content_refs
        if cross_refs is not UNSET:
            field_dict["cross_refs"] = cross_refs
        if depth is not UNSET:
            field_dict["depth"] = depth
        if importance is not UNSET:
            field_dict["importance"] = importance
        if is_deleted is not UNSET:
            field_dict["is_deleted"] = is_deleted
        if is_prunable is not UNSET:
            field_dict["is_prunable"] = is_prunable
        if last_accessed_at is not UNSET:
            field_dict["last_accessed_at"] = last_accessed_at
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if recency is not UNSET:
            field_dict["recency"] = recency
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.memory_node_metadata import MemoryNodeMetadata
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        created_at = isoparse(d.pop("created_at"))




        description = d.pop("description")

        memory_type = d.pop("memory_type")

        name = d.pop("name")

        node_id = d.pop("node_id")

        path = d.pop("path")

        updated_at = isoparse(d.pop("updated_at"))




        access_count = d.pop("access_count", UNSET)

        child_count = d.pop("child_count", UNSET)

        content_count = d.pop("content_count", UNSET)

        def _parse_content_refs(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_refs_type_0 = cast(list[str], data)

                return content_refs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        content_refs = _parse_content_refs(d.pop("content_refs", UNSET))


        def _parse_cross_refs(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                cross_refs_type_0 = cast(list[str], data)

                return cross_refs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        cross_refs = _parse_cross_refs(d.pop("cross_refs", UNSET))


        depth = d.pop("depth", UNSET)

        importance = d.pop("importance", UNSET)

        is_deleted = d.pop("is_deleted", UNSET)

        is_prunable = d.pop("is_prunable", UNSET)

        _last_accessed_at = d.pop("last_accessed_at", UNSET)
        last_accessed_at: datetime.datetime | Unset
        if isinstance(_last_accessed_at,  Unset):
            last_accessed_at = UNSET
        else:
            last_accessed_at = isoparse(_last_accessed_at)




        _metadata = d.pop("metadata", UNSET)
        metadata: MemoryNodeMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = MemoryNodeMetadata.from_dict(_metadata)




        parent_id = d.pop("parent_id", UNSET)

        recency = d.pop("recency", UNSET)

        user_id = d.pop("user_id", UNSET)

        memory_node = cls(
            agent_id=agent_id,
            created_at=created_at,
            description=description,
            memory_type=memory_type,
            name=name,
            node_id=node_id,
            path=path,
            updated_at=updated_at,
            access_count=access_count,
            child_count=child_count,
            content_count=content_count,
            content_refs=content_refs,
            cross_refs=cross_refs,
            depth=depth,
            importance=importance,
            is_deleted=is_deleted,
            is_prunable=is_prunable,
            last_accessed_at=last_accessed_at,
            metadata=metadata,
            parent_id=parent_id,
            recency=recency,
            user_id=user_id,
        )

        return memory_node

