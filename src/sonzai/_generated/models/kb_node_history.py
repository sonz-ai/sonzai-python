from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.kb_node_history_properties import KBNodeHistoryProperties





T = TypeVar("T", bound="KBNodeHistory")



@_attrs_define
class KBNodeHistory:
    """ 
        Attributes:
            change_type (str):
            changed_at (datetime.datetime):
            changed_by (str):
            node_id (str):
            project_id (str):
            properties (KBNodeHistoryProperties):
            version (int):
     """

    change_type: str
    changed_at: datetime.datetime
    changed_by: str
    node_id: str
    project_id: str
    properties: KBNodeHistoryProperties
    version: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_node_history_properties import KBNodeHistoryProperties
        change_type = self.change_type

        changed_at = self.changed_at.isoformat()

        changed_by = self.changed_by

        node_id = self.node_id

        project_id = self.project_id

        properties = self.properties.to_dict()

        version = self.version


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "change_type": change_type,
            "changed_at": changed_at,
            "changed_by": changed_by,
            "node_id": node_id,
            "project_id": project_id,
            "properties": properties,
            "version": version,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_node_history_properties import KBNodeHistoryProperties
        d = dict(src_dict)
        change_type = d.pop("change_type")

        changed_at = isoparse(d.pop("changed_at"))




        changed_by = d.pop("changed_by")

        node_id = d.pop("node_id")

        project_id = d.pop("project_id")

        properties = KBNodeHistoryProperties.from_dict(d.pop("properties"))




        version = d.pop("version")

        kb_node_history = cls(
            change_type=change_type,
            changed_at=changed_at,
            changed_by=changed_by,
            node_id=node_id,
            project_id=project_id,
            properties=properties,
            version=version,
        )

        return kb_node_history

