from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="Insight")



@_attrs_define
class Insight:
    """ 
        Attributes:
            agent_id (str):
            confidence (float):
            content (str):
            created_at (datetime.datetime):
            insight_id (str):
            insight_type (str):
            priority (int):
            related_nodes (list[str] | None):
            surfaced (bool):
            updated_at (datetime.datetime):
            user_id (str):
     """

    agent_id: str
    confidence: float
    content: str
    created_at: datetime.datetime
    insight_id: str
    insight_type: str
    priority: int
    related_nodes: list[str] | None
    surfaced: bool
    updated_at: datetime.datetime
    user_id: str





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        confidence = self.confidence

        content = self.content

        created_at = self.created_at.isoformat()

        insight_id = self.insight_id

        insight_type = self.insight_type

        priority = self.priority

        related_nodes: list[str] | None
        if isinstance(self.related_nodes, list):
            related_nodes = self.related_nodes


        else:
            related_nodes = self.related_nodes

        surfaced = self.surfaced

        updated_at = self.updated_at.isoformat()

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "AgentID": agent_id,
            "Confidence": confidence,
            "Content": content,
            "CreatedAt": created_at,
            "InsightID": insight_id,
            "InsightType": insight_type,
            "Priority": priority,
            "RelatedNodes": related_nodes,
            "Surfaced": surfaced,
            "UpdatedAt": updated_at,
            "UserID": user_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("AgentID")

        confidence = d.pop("Confidence")

        content = d.pop("Content")

        created_at = isoparse(d.pop("CreatedAt"))




        insight_id = d.pop("InsightID")

        insight_type = d.pop("InsightType")

        priority = d.pop("Priority")

        def _parse_related_nodes(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                related_nodes_type_0 = cast(list[str], data)

                return related_nodes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        related_nodes = _parse_related_nodes(d.pop("RelatedNodes"))


        surfaced = d.pop("Surfaced")

        updated_at = isoparse(d.pop("UpdatedAt"))




        user_id = d.pop("UserID")

        insight = cls(
            agent_id=agent_id,
            confidence=confidence,
            content=content,
            created_at=created_at,
            insight_id=insight_id,
            insight_type=insight_type,
            priority=priority,
            related_nodes=related_nodes,
            surfaced=surfaced,
            updated_at=updated_at,
            user_id=user_id,
        )

        return insight

