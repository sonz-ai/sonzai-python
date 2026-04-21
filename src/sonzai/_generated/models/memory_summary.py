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






T = TypeVar("T", bound="MemorySummary")



@_attrs_define
class MemorySummary:
    """ 
        Attributes:
            agent_id (str):
            created_at (datetime.datetime):
            period_end (datetime.datetime):
            period_start (datetime.datetime):
            stage (str):
            summary (str):
            summary_id (str):
            session_id (str | Unset):
            topics (list[str] | None | Unset):
            user_id (str | Unset):
     """

    agent_id: str
    created_at: datetime.datetime
    period_end: datetime.datetime
    period_start: datetime.datetime
    stage: str
    summary: str
    summary_id: str
    session_id: str | Unset = UNSET
    topics: list[str] | None | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        created_at = self.created_at.isoformat()

        period_end = self.period_end.isoformat()

        period_start = self.period_start.isoformat()

        stage = self.stage

        summary = self.summary

        summary_id = self.summary_id

        session_id = self.session_id

        topics: list[str] | None | Unset
        if isinstance(self.topics, Unset):
            topics = UNSET
        elif isinstance(self.topics, list):
            topics = self.topics


        else:
            topics = self.topics

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "created_at": created_at,
            "period_end": period_end,
            "period_start": period_start,
            "stage": stage,
            "summary": summary,
            "summary_id": summary_id,
        })
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if topics is not UNSET:
            field_dict["topics"] = topics
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        created_at = isoparse(d.pop("created_at"))




        period_end = isoparse(d.pop("period_end"))




        period_start = isoparse(d.pop("period_start"))




        stage = d.pop("stage")

        summary = d.pop("summary")

        summary_id = d.pop("summary_id")

        session_id = d.pop("session_id", UNSET)

        def _parse_topics(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                topics_type_0 = cast(list[str], data)

                return topics_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        topics = _parse_topics(d.pop("topics", UNSET))


        user_id = d.pop("user_id", UNSET)

        memory_summary = cls(
            agent_id=agent_id,
            created_at=created_at,
            period_end=period_end,
            period_start=period_start,
            stage=stage,
            summary=summary,
            summary_id=summary_id,
            session_id=session_id,
            topics=topics,
            user_id=user_id,
        )

        return memory_summary

