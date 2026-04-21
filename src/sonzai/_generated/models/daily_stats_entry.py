from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="DailyStatsEntry")



@_attrs_define
class DailyStatsEntry:
    """ 
        Attributes:
            date (str):
            messages (int):
            sessions (int):
     """

    date: str
    messages: int
    sessions: int





    def to_dict(self) -> dict[str, Any]:
        date = self.date

        messages = self.messages

        sessions = self.sessions


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "date": date,
            "messages": messages,
            "sessions": sessions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        messages = d.pop("messages")

        sessions = d.pop("sessions")

        daily_stats_entry = cls(
            date=date,
            messages=messages,
            sessions=sessions,
        )

        return daily_stats_entry

