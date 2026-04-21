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






T = TypeVar("T", bound="Habit")



@_attrs_define
class Habit:
    """ 
        Attributes:
            agent_id (str):
            category (str):
            created_at (datetime.datetime):
            daily_reinforced (float):
            description (str):
            display_name (str):
            formed (bool):
            last_reinforced_at (datetime.datetime):
            name (str):
            observation_count (int):
            strength (float):
            updated_at (datetime.datetime):
            schema (str | Unset): A URL to the JSON Schema for this object.
            formed_at (datetime.datetime | Unset):
            id (str | Unset):
            user_id (str | Unset):
     """

    agent_id: str
    category: str
    created_at: datetime.datetime
    daily_reinforced: float
    description: str
    display_name: str
    formed: bool
    last_reinforced_at: datetime.datetime
    name: str
    observation_count: int
    strength: float
    updated_at: datetime.datetime
    schema: str | Unset = UNSET
    formed_at: datetime.datetime | Unset = UNSET
    id: str | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        category = self.category

        created_at = self.created_at.isoformat()

        daily_reinforced = self.daily_reinforced

        description = self.description

        display_name = self.display_name

        formed = self.formed

        last_reinforced_at = self.last_reinforced_at.isoformat()

        name = self.name

        observation_count = self.observation_count

        strength = self.strength

        updated_at = self.updated_at.isoformat()

        schema = self.schema

        formed_at: str | Unset = UNSET
        if not isinstance(self.formed_at, Unset):
            formed_at = self.formed_at.isoformat()

        id = self.id

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "category": category,
            "created_at": created_at,
            "daily_reinforced": daily_reinforced,
            "description": description,
            "display_name": display_name,
            "formed": formed,
            "last_reinforced_at": last_reinforced_at,
            "name": name,
            "observation_count": observation_count,
            "strength": strength,
            "updated_at": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if formed_at is not UNSET:
            field_dict["formed_at"] = formed_at
        if id is not UNSET:
            field_dict["id"] = id
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        category = d.pop("category")

        created_at = isoparse(d.pop("created_at"))




        daily_reinforced = d.pop("daily_reinforced")

        description = d.pop("description")

        display_name = d.pop("display_name")

        formed = d.pop("formed")

        last_reinforced_at = isoparse(d.pop("last_reinforced_at"))




        name = d.pop("name")

        observation_count = d.pop("observation_count")

        strength = d.pop("strength")

        updated_at = isoparse(d.pop("updated_at"))




        schema = d.pop("$schema", UNSET)

        _formed_at = d.pop("formed_at", UNSET)
        formed_at: datetime.datetime | Unset
        if isinstance(_formed_at,  Unset):
            formed_at = UNSET
        else:
            formed_at = isoparse(_formed_at)




        id = d.pop("id", UNSET)

        user_id = d.pop("user_id", UNSET)

        habit = cls(
            agent_id=agent_id,
            category=category,
            created_at=created_at,
            daily_reinforced=daily_reinforced,
            description=description,
            display_name=display_name,
            formed=formed,
            last_reinforced_at=last_reinforced_at,
            name=name,
            observation_count=observation_count,
            strength=strength,
            updated_at=updated_at,
            schema=schema,
            formed_at=formed_at,
            id=id,
            user_id=user_id,
        )

        return habit

