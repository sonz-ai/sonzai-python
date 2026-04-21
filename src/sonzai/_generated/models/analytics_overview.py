from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="AnalyticsOverview")



@_attrs_define
class AnalyticsOverview:
    """ 
        Attributes:
            active_agents (int):
            active_sessions (int):
            total_agents (int):
            total_messages (int):
            total_sessions (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    active_agents: int
    active_sessions: int
    total_agents: int
    total_messages: int
    total_sessions: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        active_agents = self.active_agents

        active_sessions = self.active_sessions

        total_agents = self.total_agents

        total_messages = self.total_messages

        total_sessions = self.total_sessions

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "activeAgents": active_agents,
            "activeSessions": active_sessions,
            "totalAgents": total_agents,
            "totalMessages": total_messages,
            "totalSessions": total_sessions,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active_agents = d.pop("activeAgents")

        active_sessions = d.pop("activeSessions")

        total_agents = d.pop("totalAgents")

        total_messages = d.pop("totalMessages")

        total_sessions = d.pop("totalSessions")

        schema = d.pop("$schema", UNSET)

        analytics_overview = cls(
            active_agents=active_agents,
            active_sessions=active_sessions,
            total_agents=total_agents,
            total_messages=total_messages,
            total_sessions=total_sessions,
            schema=schema,
        )

        return analytics_overview

