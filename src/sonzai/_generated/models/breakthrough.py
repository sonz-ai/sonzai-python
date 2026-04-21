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






T = TypeVar("T", bound="Breakthrough")



@_attrs_define
class Breakthrough:
    """ 
        Attributes:
            achieved_goals (list[str] | None):
            acknowledged (bool):
            agent_id (str):
            breakthrough_id (str):
            breakthrough_number (int):
            created_at (datetime.datetime):
            level_at_breakthrough (int):
            narrative (str):
            new_goals (list[str] | None):
            personality_shifts (list[str] | None):
            skill_points_awarded (int):
            user_id (str):
            trait_evolved (str | Unset):
     """

    achieved_goals: list[str] | None
    acknowledged: bool
    agent_id: str
    breakthrough_id: str
    breakthrough_number: int
    created_at: datetime.datetime
    level_at_breakthrough: int
    narrative: str
    new_goals: list[str] | None
    personality_shifts: list[str] | None
    skill_points_awarded: int
    user_id: str
    trait_evolved: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        achieved_goals: list[str] | None
        if isinstance(self.achieved_goals, list):
            achieved_goals = self.achieved_goals


        else:
            achieved_goals = self.achieved_goals

        acknowledged = self.acknowledged

        agent_id = self.agent_id

        breakthrough_id = self.breakthrough_id

        breakthrough_number = self.breakthrough_number

        created_at = self.created_at.isoformat()

        level_at_breakthrough = self.level_at_breakthrough

        narrative = self.narrative

        new_goals: list[str] | None
        if isinstance(self.new_goals, list):
            new_goals = self.new_goals


        else:
            new_goals = self.new_goals

        personality_shifts: list[str] | None
        if isinstance(self.personality_shifts, list):
            personality_shifts = self.personality_shifts


        else:
            personality_shifts = self.personality_shifts

        skill_points_awarded = self.skill_points_awarded

        user_id = self.user_id

        trait_evolved = self.trait_evolved


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "achieved_goals": achieved_goals,
            "acknowledged": acknowledged,
            "agent_id": agent_id,
            "breakthrough_id": breakthrough_id,
            "breakthrough_number": breakthrough_number,
            "created_at": created_at,
            "level_at_breakthrough": level_at_breakthrough,
            "narrative": narrative,
            "new_goals": new_goals,
            "personality_shifts": personality_shifts,
            "skill_points_awarded": skill_points_awarded,
            "user_id": user_id,
        })
        if trait_evolved is not UNSET:
            field_dict["trait_evolved"] = trait_evolved

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_achieved_goals(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                achieved_goals_type_0 = cast(list[str], data)

                return achieved_goals_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        achieved_goals = _parse_achieved_goals(d.pop("achieved_goals"))


        acknowledged = d.pop("acknowledged")

        agent_id = d.pop("agent_id")

        breakthrough_id = d.pop("breakthrough_id")

        breakthrough_number = d.pop("breakthrough_number")

        created_at = isoparse(d.pop("created_at"))




        level_at_breakthrough = d.pop("level_at_breakthrough")

        narrative = d.pop("narrative")

        def _parse_new_goals(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                new_goals_type_0 = cast(list[str], data)

                return new_goals_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        new_goals = _parse_new_goals(d.pop("new_goals"))


        def _parse_personality_shifts(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                personality_shifts_type_0 = cast(list[str], data)

                return personality_shifts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        personality_shifts = _parse_personality_shifts(d.pop("personality_shifts"))


        skill_points_awarded = d.pop("skill_points_awarded")

        user_id = d.pop("user_id")

        trait_evolved = d.pop("trait_evolved", UNSET)

        breakthrough = cls(
            achieved_goals=achieved_goals,
            acknowledged=acknowledged,
            agent_id=agent_id,
            breakthrough_id=breakthrough_id,
            breakthrough_number=breakthrough_number,
            created_at=created_at,
            level_at_breakthrough=level_at_breakthrough,
            narrative=narrative,
            new_goals=new_goals,
            personality_shifts=personality_shifts,
            skill_points_awarded=skill_points_awarded,
            user_id=user_id,
            trait_evolved=trait_evolved,
        )

        return breakthrough

