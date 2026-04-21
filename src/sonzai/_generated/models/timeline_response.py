from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.timeline_session import TimelineSession





T = TypeVar("T", bound="TimelineResponse")



@_attrs_define
class TimelineResponse:
    """ 
        Attributes:
            sessions (list[TimelineSession] | None):
            total_facts (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    sessions: list[TimelineSession] | None
    total_facts: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.timeline_session import TimelineSession
        sessions: list[dict[str, Any]] | None
        if isinstance(self.sessions, list):
            sessions = []
            for sessions_type_0_item_data in self.sessions:
                sessions_type_0_item = sessions_type_0_item_data.to_dict()
                sessions.append(sessions_type_0_item)


        else:
            sessions = self.sessions

        total_facts = self.total_facts

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "sessions": sessions,
            "total_facts": total_facts,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.timeline_session import TimelineSession
        d = dict(src_dict)
        def _parse_sessions(data: object) -> list[TimelineSession] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sessions_type_0 = []
                _sessions_type_0 = data
                for sessions_type_0_item_data in (_sessions_type_0):
                    sessions_type_0_item = TimelineSession.from_dict(sessions_type_0_item_data)



                    sessions_type_0.append(sessions_type_0_item)

                return sessions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[TimelineSession] | None, data)

        sessions = _parse_sessions(d.pop("sessions"))


        total_facts = d.pop("total_facts")

        schema = d.pop("$schema", UNSET)

        timeline_response = cls(
            sessions=sessions,
            total_facts=total_facts,
            schema=schema,
        )

        return timeline_response

