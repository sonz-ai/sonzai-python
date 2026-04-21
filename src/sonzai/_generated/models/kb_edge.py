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
  from ..models.kb_edge_properties import KBEdgeProperties





T = TypeVar("T", bound="KBEdge")



@_attrs_define
class KBEdge:
    """ 
        Attributes:
            confidence (float):
            created_at (datetime.datetime):
            edge_id (str):
            edge_type (str):
            from_node_id (str):
            project_id (str):
            to_node_id (str):
            updated_at (datetime.datetime):
            label (str | Unset):
            properties (KBEdgeProperties | Unset):
            scope_id (str | Unset):
            source_doc (str | Unset):
            tenant_id (str | Unset):
     """

    confidence: float
    created_at: datetime.datetime
    edge_id: str
    edge_type: str
    from_node_id: str
    project_id: str
    to_node_id: str
    updated_at: datetime.datetime
    label: str | Unset = UNSET
    properties: KBEdgeProperties | Unset = UNSET
    scope_id: str | Unset = UNSET
    source_doc: str | Unset = UNSET
    tenant_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_edge_properties import KBEdgeProperties
        confidence = self.confidence

        created_at = self.created_at.isoformat()

        edge_id = self.edge_id

        edge_type = self.edge_type

        from_node_id = self.from_node_id

        project_id = self.project_id

        to_node_id = self.to_node_id

        updated_at = self.updated_at.isoformat()

        label = self.label

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        scope_id = self.scope_id

        source_doc = self.source_doc

        tenant_id = self.tenant_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "confidence": confidence,
            "created_at": created_at,
            "edge_id": edge_id,
            "edge_type": edge_type,
            "from_node_id": from_node_id,
            "project_id": project_id,
            "to_node_id": to_node_id,
            "updated_at": updated_at,
        })
        if label is not UNSET:
            field_dict["label"] = label
        if properties is not UNSET:
            field_dict["properties"] = properties
        if scope_id is not UNSET:
            field_dict["scope_id"] = scope_id
        if source_doc is not UNSET:
            field_dict["source_doc"] = source_doc
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_edge_properties import KBEdgeProperties
        d = dict(src_dict)
        confidence = d.pop("confidence")

        created_at = isoparse(d.pop("created_at"))




        edge_id = d.pop("edge_id")

        edge_type = d.pop("edge_type")

        from_node_id = d.pop("from_node_id")

        project_id = d.pop("project_id")

        to_node_id = d.pop("to_node_id")

        updated_at = isoparse(d.pop("updated_at"))




        label = d.pop("label", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: KBEdgeProperties | Unset
        if isinstance(_properties,  Unset):
            properties = UNSET
        else:
            properties = KBEdgeProperties.from_dict(_properties)




        scope_id = d.pop("scope_id", UNSET)

        source_doc = d.pop("source_doc", UNSET)

        tenant_id = d.pop("tenant_id", UNSET)

        kb_edge = cls(
            confidence=confidence,
            created_at=created_at,
            edge_id=edge_id,
            edge_type=edge_type,
            from_node_id=from_node_id,
            project_id=project_id,
            to_node_id=to_node_id,
            updated_at=updated_at,
            label=label,
            properties=properties,
            scope_id=scope_id,
            source_doc=source_doc,
            tenant_id=tenant_id,
        )

        return kb_edge

