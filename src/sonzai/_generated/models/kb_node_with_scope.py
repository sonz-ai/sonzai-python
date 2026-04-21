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
  from ..models.kb_node_with_scope_properties import KBNodeWithScopeProperties
  from ..models.kb_node_with_scope_property_sources import KBNodeWithScopePropertySources





T = TypeVar("T", bound="KBNodeWithScope")



@_attrs_define
class KBNodeWithScope:
    """ 
        Attributes:
            confidence (float):
            created_at (datetime.datetime):
            is_active (bool):
            label (str):
            node_id (str):
            node_type (str):
            norm_label (str):
            project_id (str):
            properties (KBNodeWithScopeProperties):
            relevance (float):
            scope_type (str):
            source_docs (list[str] | None):
            source_type (str):
            updated_at (datetime.datetime):
            version (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
            property_sources (KBNodeWithScopePropertySources | Unset):
            scope_id (str | Unset):
            tenant_id (str | Unset):
     """

    confidence: float
    created_at: datetime.datetime
    is_active: bool
    label: str
    node_id: str
    node_type: str
    norm_label: str
    project_id: str
    properties: KBNodeWithScopeProperties
    relevance: float
    scope_type: str
    source_docs: list[str] | None
    source_type: str
    updated_at: datetime.datetime
    version: int
    schema: str | Unset = UNSET
    property_sources: KBNodeWithScopePropertySources | Unset = UNSET
    scope_id: str | Unset = UNSET
    tenant_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_node_with_scope_properties import KBNodeWithScopeProperties
        from ..models.kb_node_with_scope_property_sources import KBNodeWithScopePropertySources
        confidence = self.confidence

        created_at = self.created_at.isoformat()

        is_active = self.is_active

        label = self.label

        node_id = self.node_id

        node_type = self.node_type

        norm_label = self.norm_label

        project_id = self.project_id

        properties = self.properties.to_dict()

        relevance = self.relevance

        scope_type = self.scope_type

        source_docs: list[str] | None
        if isinstance(self.source_docs, list):
            source_docs = self.source_docs


        else:
            source_docs = self.source_docs

        source_type = self.source_type

        updated_at = self.updated_at.isoformat()

        version = self.version

        schema = self.schema

        property_sources: dict[str, Any] | Unset = UNSET
        if not isinstance(self.property_sources, Unset):
            property_sources = self.property_sources.to_dict()

        scope_id = self.scope_id

        tenant_id = self.tenant_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "confidence": confidence,
            "created_at": created_at,
            "is_active": is_active,
            "label": label,
            "node_id": node_id,
            "node_type": node_type,
            "norm_label": norm_label,
            "project_id": project_id,
            "properties": properties,
            "relevance": relevance,
            "scope_type": scope_type,
            "source_docs": source_docs,
            "source_type": source_type,
            "updated_at": updated_at,
            "version": version,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if property_sources is not UNSET:
            field_dict["property_sources"] = property_sources
        if scope_id is not UNSET:
            field_dict["scope_id"] = scope_id
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_node_with_scope_properties import KBNodeWithScopeProperties
        from ..models.kb_node_with_scope_property_sources import KBNodeWithScopePropertySources
        d = dict(src_dict)
        confidence = d.pop("confidence")

        created_at = isoparse(d.pop("created_at"))




        is_active = d.pop("is_active")

        label = d.pop("label")

        node_id = d.pop("node_id")

        node_type = d.pop("node_type")

        norm_label = d.pop("norm_label")

        project_id = d.pop("project_id")

        properties = KBNodeWithScopeProperties.from_dict(d.pop("properties"))




        relevance = d.pop("relevance")

        scope_type = d.pop("scope_type")

        def _parse_source_docs(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                source_docs_type_0 = cast(list[str], data)

                return source_docs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        source_docs = _parse_source_docs(d.pop("source_docs"))


        source_type = d.pop("source_type")

        updated_at = isoparse(d.pop("updated_at"))




        version = d.pop("version")

        schema = d.pop("$schema", UNSET)

        _property_sources = d.pop("property_sources", UNSET)
        property_sources: KBNodeWithScopePropertySources | Unset
        if isinstance(_property_sources,  Unset):
            property_sources = UNSET
        else:
            property_sources = KBNodeWithScopePropertySources.from_dict(_property_sources)




        scope_id = d.pop("scope_id", UNSET)

        tenant_id = d.pop("tenant_id", UNSET)

        kb_node_with_scope = cls(
            confidence=confidence,
            created_at=created_at,
            is_active=is_active,
            label=label,
            node_id=node_id,
            node_type=node_type,
            norm_label=norm_label,
            project_id=project_id,
            properties=properties,
            relevance=relevance,
            scope_type=scope_type,
            source_docs=source_docs,
            source_type=source_type,
            updated_at=updated_at,
            version=version,
            schema=schema,
            property_sources=property_sources,
            scope_id=scope_id,
            tenant_id=tenant_id,
        )

        return kb_node_with_scope

