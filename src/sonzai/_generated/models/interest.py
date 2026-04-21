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






T = TypeVar("T", bound="Interest")



@_attrs_define
class Interest:
    """ 
        Attributes:
            agent_id (str):
            category (str):
            confidence (float):
            created_at (datetime.datetime):
            engagement_level (float):
            last_mentioned_at (datetime.datetime):
            mention_count (int):
            research_status (str):
            topic (str):
            updated_at (datetime.datetime):
            user_id (str):
            research_findings (str | Unset):
     """

    agent_id: str
    category: str
    confidence: float
    created_at: datetime.datetime
    engagement_level: float
    last_mentioned_at: datetime.datetime
    mention_count: int
    research_status: str
    topic: str
    updated_at: datetime.datetime
    user_id: str
    research_findings: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        category = self.category

        confidence = self.confidence

        created_at = self.created_at.isoformat()

        engagement_level = self.engagement_level

        last_mentioned_at = self.last_mentioned_at.isoformat()

        mention_count = self.mention_count

        research_status = self.research_status

        topic = self.topic

        updated_at = self.updated_at.isoformat()

        user_id = self.user_id

        research_findings = self.research_findings


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "category": category,
            "confidence": confidence,
            "created_at": created_at,
            "engagement_level": engagement_level,
            "last_mentioned_at": last_mentioned_at,
            "mention_count": mention_count,
            "research_status": research_status,
            "topic": topic,
            "updated_at": updated_at,
            "user_id": user_id,
        })
        if research_findings is not UNSET:
            field_dict["research_findings"] = research_findings

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        category = d.pop("category")

        confidence = d.pop("confidence")

        created_at = isoparse(d.pop("created_at"))




        engagement_level = d.pop("engagement_level")

        last_mentioned_at = isoparse(d.pop("last_mentioned_at"))




        mention_count = d.pop("mention_count")

        research_status = d.pop("research_status")

        topic = d.pop("topic")

        updated_at = isoparse(d.pop("updated_at"))




        user_id = d.pop("user_id")

        research_findings = d.pop("research_findings", UNSET)

        interest = cls(
            agent_id=agent_id,
            category=category,
            confidence=confidence,
            created_at=created_at,
            engagement_level=engagement_level,
            last_mentioned_at=last_mentioned_at,
            mention_count=mention_count,
            research_status=research_status,
            topic=topic,
            updated_at=updated_at,
            user_id=user_id,
            research_findings=research_findings,
        )

        return interest

