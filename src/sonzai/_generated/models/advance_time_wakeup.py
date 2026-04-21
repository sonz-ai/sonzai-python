from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="AdvanceTimeWakeup")



@_attrs_define
class AdvanceTimeWakeup:
    """ 
        Attributes:
            agent_id (str):
            check_type (str):
            intent (str):
            user_id (str):
            wakeup_id (str):
            generated_message (str | Unset):
     """

    agent_id: str
    check_type: str
    intent: str
    user_id: str
    wakeup_id: str
    generated_message: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        check_type = self.check_type

        intent = self.intent

        user_id = self.user_id

        wakeup_id = self.wakeup_id

        generated_message = self.generated_message


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "check_type": check_type,
            "intent": intent,
            "user_id": user_id,
            "wakeup_id": wakeup_id,
        })
        if generated_message is not UNSET:
            field_dict["generated_message"] = generated_message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        check_type = d.pop("check_type")

        intent = d.pop("intent")

        user_id = d.pop("user_id")

        wakeup_id = d.pop("wakeup_id")

        generated_message = d.pop("generated_message", UNSET)

        advance_time_wakeup = cls(
            agent_id=agent_id,
            check_type=check_type,
            intent=intent,
            user_id=user_id,
            wakeup_id=wakeup_id,
            generated_message=generated_message,
        )

        return advance_time_wakeup

