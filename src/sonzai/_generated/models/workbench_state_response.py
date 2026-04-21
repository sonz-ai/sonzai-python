from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.workbench_state_big_5 import WorkbenchStateBig5
  from ..models.workbench_state_diary_entry import WorkbenchStateDiaryEntry
  from ..models.workbench_state_dimensions import WorkbenchStateDimensions
  from ..models.workbench_state_fact import WorkbenchStateFact
  from ..models.workbench_state_habit import WorkbenchStateHabit
  from ..models.workbench_state_interest import WorkbenchStateInterest
  from ..models.workbench_state_mood import WorkbenchStateMood
  from ..models.workbench_state_relation import WorkbenchStateRelation





T = TypeVar("T", bound="WorkbenchStateResponse")



@_attrs_define
class WorkbenchStateResponse:
    """ 
        Attributes:
            diary_entries (list[WorkbenchStateDiaryEntry] | None):
            facts (list[WorkbenchStateFact] | None):
            habits (list[WorkbenchStateHabit] | None):
            interests (list[WorkbenchStateInterest] | None):
            next_event_hours (float):
            schema (str | Unset): A URL to the JSON Schema for this object.
            big5 (WorkbenchStateBig5 | Unset):
            dimensions (WorkbenchStateDimensions | Unset):
            mood (WorkbenchStateMood | Unset):
            relationship (WorkbenchStateRelation | Unset):
     """

    diary_entries: list[WorkbenchStateDiaryEntry] | None
    facts: list[WorkbenchStateFact] | None
    habits: list[WorkbenchStateHabit] | None
    interests: list[WorkbenchStateInterest] | None
    next_event_hours: float
    schema: str | Unset = UNSET
    big5: WorkbenchStateBig5 | Unset = UNSET
    dimensions: WorkbenchStateDimensions | Unset = UNSET
    mood: WorkbenchStateMood | Unset = UNSET
    relationship: WorkbenchStateRelation | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.workbench_state_big_5 import WorkbenchStateBig5
        from ..models.workbench_state_diary_entry import WorkbenchStateDiaryEntry
        from ..models.workbench_state_dimensions import WorkbenchStateDimensions
        from ..models.workbench_state_fact import WorkbenchStateFact
        from ..models.workbench_state_habit import WorkbenchStateHabit
        from ..models.workbench_state_interest import WorkbenchStateInterest
        from ..models.workbench_state_mood import WorkbenchStateMood
        from ..models.workbench_state_relation import WorkbenchStateRelation
        diary_entries: list[dict[str, Any]] | None
        if isinstance(self.diary_entries, list):
            diary_entries = []
            for diary_entries_type_0_item_data in self.diary_entries:
                diary_entries_type_0_item = diary_entries_type_0_item_data.to_dict()
                diary_entries.append(diary_entries_type_0_item)


        else:
            diary_entries = self.diary_entries

        facts: list[dict[str, Any]] | None
        if isinstance(self.facts, list):
            facts = []
            for facts_type_0_item_data in self.facts:
                facts_type_0_item = facts_type_0_item_data.to_dict()
                facts.append(facts_type_0_item)


        else:
            facts = self.facts

        habits: list[dict[str, Any]] | None
        if isinstance(self.habits, list):
            habits = []
            for habits_type_0_item_data in self.habits:
                habits_type_0_item = habits_type_0_item_data.to_dict()
                habits.append(habits_type_0_item)


        else:
            habits = self.habits

        interests: list[dict[str, Any]] | None
        if isinstance(self.interests, list):
            interests = []
            for interests_type_0_item_data in self.interests:
                interests_type_0_item = interests_type_0_item_data.to_dict()
                interests.append(interests_type_0_item)


        else:
            interests = self.interests

        next_event_hours = self.next_event_hours

        schema = self.schema

        big5: dict[str, Any] | Unset = UNSET
        if not isinstance(self.big5, Unset):
            big5 = self.big5.to_dict()

        dimensions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dimensions, Unset):
            dimensions = self.dimensions.to_dict()

        mood: dict[str, Any] | Unset = UNSET
        if not isinstance(self.mood, Unset):
            mood = self.mood.to_dict()

        relationship: dict[str, Any] | Unset = UNSET
        if not isinstance(self.relationship, Unset):
            relationship = self.relationship.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "diary_entries": diary_entries,
            "facts": facts,
            "habits": habits,
            "interests": interests,
            "next_event_hours": next_event_hours,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if big5 is not UNSET:
            field_dict["big5"] = big5
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions
        if mood is not UNSET:
            field_dict["mood"] = mood
        if relationship is not UNSET:
            field_dict["relationship"] = relationship

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workbench_state_big_5 import WorkbenchStateBig5
        from ..models.workbench_state_diary_entry import WorkbenchStateDiaryEntry
        from ..models.workbench_state_dimensions import WorkbenchStateDimensions
        from ..models.workbench_state_fact import WorkbenchStateFact
        from ..models.workbench_state_habit import WorkbenchStateHabit
        from ..models.workbench_state_interest import WorkbenchStateInterest
        from ..models.workbench_state_mood import WorkbenchStateMood
        from ..models.workbench_state_relation import WorkbenchStateRelation
        d = dict(src_dict)
        def _parse_diary_entries(data: object) -> list[WorkbenchStateDiaryEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                diary_entries_type_0 = []
                _diary_entries_type_0 = data
                for diary_entries_type_0_item_data in (_diary_entries_type_0):
                    diary_entries_type_0_item = WorkbenchStateDiaryEntry.from_dict(diary_entries_type_0_item_data)



                    diary_entries_type_0.append(diary_entries_type_0_item)

                return diary_entries_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WorkbenchStateDiaryEntry] | None, data)

        diary_entries = _parse_diary_entries(d.pop("diary_entries"))


        def _parse_facts(data: object) -> list[WorkbenchStateFact] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                facts_type_0 = []
                _facts_type_0 = data
                for facts_type_0_item_data in (_facts_type_0):
                    facts_type_0_item = WorkbenchStateFact.from_dict(facts_type_0_item_data)



                    facts_type_0.append(facts_type_0_item)

                return facts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WorkbenchStateFact] | None, data)

        facts = _parse_facts(d.pop("facts"))


        def _parse_habits(data: object) -> list[WorkbenchStateHabit] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                habits_type_0 = []
                _habits_type_0 = data
                for habits_type_0_item_data in (_habits_type_0):
                    habits_type_0_item = WorkbenchStateHabit.from_dict(habits_type_0_item_data)



                    habits_type_0.append(habits_type_0_item)

                return habits_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WorkbenchStateHabit] | None, data)

        habits = _parse_habits(d.pop("habits"))


        def _parse_interests(data: object) -> list[WorkbenchStateInterest] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                interests_type_0 = []
                _interests_type_0 = data
                for interests_type_0_item_data in (_interests_type_0):
                    interests_type_0_item = WorkbenchStateInterest.from_dict(interests_type_0_item_data)



                    interests_type_0.append(interests_type_0_item)

                return interests_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WorkbenchStateInterest] | None, data)

        interests = _parse_interests(d.pop("interests"))


        next_event_hours = d.pop("next_event_hours")

        schema = d.pop("$schema", UNSET)

        _big5 = d.pop("big5", UNSET)
        big5: WorkbenchStateBig5 | Unset
        if isinstance(_big5,  Unset):
            big5 = UNSET
        else:
            big5 = WorkbenchStateBig5.from_dict(_big5)




        _dimensions = d.pop("dimensions", UNSET)
        dimensions: WorkbenchStateDimensions | Unset
        if isinstance(_dimensions,  Unset):
            dimensions = UNSET
        else:
            dimensions = WorkbenchStateDimensions.from_dict(_dimensions)




        _mood = d.pop("mood", UNSET)
        mood: WorkbenchStateMood | Unset
        if isinstance(_mood,  Unset):
            mood = UNSET
        else:
            mood = WorkbenchStateMood.from_dict(_mood)




        _relationship = d.pop("relationship", UNSET)
        relationship: WorkbenchStateRelation | Unset
        if isinstance(_relationship,  Unset):
            relationship = UNSET
        else:
            relationship = WorkbenchStateRelation.from_dict(_relationship)




        workbench_state_response = cls(
            diary_entries=diary_entries,
            facts=facts,
            habits=habits,
            interests=interests,
            next_event_hours=next_event_hours,
            schema=schema,
            big5=big5,
            dimensions=dimensions,
            mood=mood,
            relationship=relationship,
        )

        return workbench_state_response

