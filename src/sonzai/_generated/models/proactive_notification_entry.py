from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ProactiveNotificationEntry")



@_attrs_define
class ProactiveNotificationEntry:
    """ 
        Attributes:
            agent_id (str):
            check_type (str):
            created_at (str):
            generated_message (str):
            message_id (str):
            status (str):
            user_id (str):
            consumed_at (str | Unset):
            intent (str | Unset):
            wakeup_id (str | Unset):
     """

    agent_id: str
    check_type: str
    created_at: str
    generated_message: str
    message_id: str
    status: str
    user_id: str
    consumed_at: str | Unset = UNSET
    intent: str | Unset = UNSET
    wakeup_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        check_type = self.check_type

        created_at = self.created_at

        generated_message = self.generated_message

        message_id = self.message_id

        status = self.status

        user_id = self.user_id

        consumed_at = self.consumed_at

        intent = self.intent

        wakeup_id = self.wakeup_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "check_type": check_type,
            "created_at": created_at,
            "generated_message": generated_message,
            "message_id": message_id,
            "status": status,
            "user_id": user_id,
        })
        if consumed_at is not UNSET:
            field_dict["consumed_at"] = consumed_at
        if intent is not UNSET:
            field_dict["intent"] = intent
        if wakeup_id is not UNSET:
            field_dict["wakeup_id"] = wakeup_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        check_type = d.pop("check_type")

        created_at = d.pop("created_at")

        generated_message = d.pop("generated_message")

        message_id = d.pop("message_id")

        status = d.pop("status")

        user_id = d.pop("user_id")

        consumed_at = d.pop("consumed_at", UNSET)

        intent = d.pop("intent", UNSET)

        wakeup_id = d.pop("wakeup_id", UNSET)

        proactive_notification_entry = cls(
            agent_id=agent_id,
            check_type=check_type,
            created_at=created_at,
            generated_message=generated_message,
            message_id=message_id,
            status=status,
            user_id=user_id,
            consumed_at=consumed_at,
            intent=intent,
            wakeup_id=wakeup_id,
        )

        return proactive_notification_entry

