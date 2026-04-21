from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="WakeupEntry")



@_attrs_define
class WakeupEntry:
    """ 
        Attributes:
            agent_id (str):
            check_type (str):
            created_at (str):
            scheduled_at (str):
            status (str):
            user_id (str):
            wakeup_id (str):
            event_description (str | Unset):
            executed_at (str | Unset):
            intent (str | Unset):
            interest_topic (str | Unset):
            last_topic (str | Unset):
            occasion (str | Unset):
            research_summary (str | Unset):
     """

    agent_id: str
    check_type: str
    created_at: str
    scheduled_at: str
    status: str
    user_id: str
    wakeup_id: str
    event_description: str | Unset = UNSET
    executed_at: str | Unset = UNSET
    intent: str | Unset = UNSET
    interest_topic: str | Unset = UNSET
    last_topic: str | Unset = UNSET
    occasion: str | Unset = UNSET
    research_summary: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        check_type = self.check_type

        created_at = self.created_at

        scheduled_at = self.scheduled_at

        status = self.status

        user_id = self.user_id

        wakeup_id = self.wakeup_id

        event_description = self.event_description

        executed_at = self.executed_at

        intent = self.intent

        interest_topic = self.interest_topic

        last_topic = self.last_topic

        occasion = self.occasion

        research_summary = self.research_summary


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "check_type": check_type,
            "created_at": created_at,
            "scheduled_at": scheduled_at,
            "status": status,
            "user_id": user_id,
            "wakeup_id": wakeup_id,
        })
        if event_description is not UNSET:
            field_dict["event_description"] = event_description
        if executed_at is not UNSET:
            field_dict["executed_at"] = executed_at
        if intent is not UNSET:
            field_dict["intent"] = intent
        if interest_topic is not UNSET:
            field_dict["interest_topic"] = interest_topic
        if last_topic is not UNSET:
            field_dict["last_topic"] = last_topic
        if occasion is not UNSET:
            field_dict["occasion"] = occasion
        if research_summary is not UNSET:
            field_dict["research_summary"] = research_summary

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        check_type = d.pop("check_type")

        created_at = d.pop("created_at")

        scheduled_at = d.pop("scheduled_at")

        status = d.pop("status")

        user_id = d.pop("user_id")

        wakeup_id = d.pop("wakeup_id")

        event_description = d.pop("event_description", UNSET)

        executed_at = d.pop("executed_at", UNSET)

        intent = d.pop("intent", UNSET)

        interest_topic = d.pop("interest_topic", UNSET)

        last_topic = d.pop("last_topic", UNSET)

        occasion = d.pop("occasion", UNSET)

        research_summary = d.pop("research_summary", UNSET)

        wakeup_entry = cls(
            agent_id=agent_id,
            check_type=check_type,
            created_at=created_at,
            scheduled_at=scheduled_at,
            status=status,
            user_id=user_id,
            wakeup_id=wakeup_id,
            event_description=event_description,
            executed_at=executed_at,
            intent=intent,
            interest_topic=interest_topic,
            last_topic=last_topic,
            occasion=occasion,
            research_summary=research_summary,
        )

        return wakeup_entry

