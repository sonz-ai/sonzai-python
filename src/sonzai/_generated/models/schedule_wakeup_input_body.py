from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ScheduleWakeupInputBody")



@_attrs_define
class ScheduleWakeupInputBody:
    """ 
        Attributes:
            check_type (str): Type of check to perform on wakeup
            delay_hours (int): Hours to delay before wakeup fires
            intent (str): Intent/reason for the wakeup
            user_id (str): ID of the user to wake up for
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    check_type: str
    delay_hours: int
    intent: str
    user_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        check_type = self.check_type

        delay_hours = self.delay_hours

        intent = self.intent

        user_id = self.user_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "check_type": check_type,
            "delay_hours": delay_hours,
            "intent": intent,
            "user_id": user_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        check_type = d.pop("check_type")

        delay_hours = d.pop("delay_hours")

        intent = d.pop("intent")

        user_id = d.pop("user_id")

        schema = d.pop("$schema", UNSET)

        schedule_wakeup_input_body = cls(
            check_type=check_type,
            delay_hours=delay_hours,
            intent=intent,
            user_id=user_id,
            schema=schema,
        )

        return schedule_wakeup_input_body

