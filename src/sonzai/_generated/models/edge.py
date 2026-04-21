from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="Edge")



@_attrs_define
class Edge:
    """ 
        Attributes:
            agent_id (str):
            co_occurrence_count (int):
            created_at (datetime.datetime):
            edge_id (str):
            edge_type (str):
            from_node_id (str):
            strength (float):
            to_node_id (str):
            updated_at (datetime.datetime):
     """

    agent_id: str
    co_occurrence_count: int
    created_at: datetime.datetime
    edge_id: str
    edge_type: str
    from_node_id: str
    strength: float
    to_node_id: str
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        co_occurrence_count = self.co_occurrence_count

        created_at = self.created_at.isoformat()

        edge_id = self.edge_id

        edge_type = self.edge_type

        from_node_id = self.from_node_id

        strength = self.strength

        to_node_id = self.to_node_id

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "AgentID": agent_id,
            "CoOccurrenceCount": co_occurrence_count,
            "CreatedAt": created_at,
            "EdgeID": edge_id,
            "EdgeType": edge_type,
            "FromNodeID": from_node_id,
            "Strength": strength,
            "ToNodeID": to_node_id,
            "UpdatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("AgentID")

        co_occurrence_count = d.pop("CoOccurrenceCount")

        created_at = isoparse(d.pop("CreatedAt"))




        edge_id = d.pop("EdgeID")

        edge_type = d.pop("EdgeType")

        from_node_id = d.pop("FromNodeID")

        strength = d.pop("Strength")

        to_node_id = d.pop("ToNodeID")

        updated_at = isoparse(d.pop("UpdatedAt"))




        edge = cls(
            agent_id=agent_id,
            co_occurrence_count=co_occurrence_count,
            created_at=created_at,
            edge_id=edge_id,
            edge_type=edge_type,
            from_node_id=from_node_id,
            strength=strength,
            to_node_id=to_node_id,
            updated_at=updated_at,
        )

        return edge

