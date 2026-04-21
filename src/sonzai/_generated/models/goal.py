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






T = TypeVar("T", bound="Goal")



@_attrs_define
class Goal:
    """ 
        Attributes:
            agent_id (str):
            created_at (datetime.datetime):
            description (str):
            goal_id (str):
            priority (int):
            status (str):
            title (str):
            type_ (str):
            updated_at (datetime.datetime):
            schema (str | Unset): A URL to the JSON Schema for this object.
            achieved_at (datetime.datetime | Unset):
            related_traits (list[str] | None | Unset):
            user_id (str | Unset):
     """

    agent_id: str
    created_at: datetime.datetime
    description: str
    goal_id: str
    priority: int
    status: str
    title: str
    type_: str
    updated_at: datetime.datetime
    schema: str | Unset = UNSET
    achieved_at: datetime.datetime | Unset = UNSET
    related_traits: list[str] | None | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        created_at = self.created_at.isoformat()

        description = self.description

        goal_id = self.goal_id

        priority = self.priority

        status = self.status

        title = self.title

        type_ = self.type_

        updated_at = self.updated_at.isoformat()

        schema = self.schema

        achieved_at: str | Unset = UNSET
        if not isinstance(self.achieved_at, Unset):
            achieved_at = self.achieved_at.isoformat()

        related_traits: list[str] | None | Unset
        if isinstance(self.related_traits, Unset):
            related_traits = UNSET
        elif isinstance(self.related_traits, list):
            related_traits = self.related_traits


        else:
            related_traits = self.related_traits

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "created_at": created_at,
            "description": description,
            "goal_id": goal_id,
            "priority": priority,
            "status": status,
            "title": title,
            "type": type_,
            "updated_at": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if achieved_at is not UNSET:
            field_dict["achieved_at"] = achieved_at
        if related_traits is not UNSET:
            field_dict["related_traits"] = related_traits
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        created_at = isoparse(d.pop("created_at"))




        description = d.pop("description")

        goal_id = d.pop("goal_id")

        priority = d.pop("priority")

        status = d.pop("status")

        title = d.pop("title")

        type_ = d.pop("type")

        updated_at = isoparse(d.pop("updated_at"))




        schema = d.pop("$schema", UNSET)

        _achieved_at = d.pop("achieved_at", UNSET)
        achieved_at: datetime.datetime | Unset
        if isinstance(_achieved_at,  Unset):
            achieved_at = UNSET
        else:
            achieved_at = isoparse(_achieved_at)




        def _parse_related_traits(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                related_traits_type_0 = cast(list[str], data)

                return related_traits_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        related_traits = _parse_related_traits(d.pop("related_traits", UNSET))


        user_id = d.pop("user_id", UNSET)

        goal = cls(
            agent_id=agent_id,
            created_at=created_at,
            description=description,
            goal_id=goal_id,
            priority=priority,
            status=status,
            title=title,
            type_=type_,
            updated_at=updated_at,
            schema=schema,
            achieved_at=achieved_at,
            related_traits=related_traits,
            user_id=user_id,
        )

        return goal

