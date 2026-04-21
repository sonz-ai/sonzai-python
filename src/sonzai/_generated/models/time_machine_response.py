from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.big_5_assessment import Big5Assessment
  from ..models.personality_delta import PersonalityDelta
  from ..models.time_machine_mood_snapshot import TimeMachineMoodSnapshot





T = TypeVar("T", bound="TimeMachineResponse")



@_attrs_define
class TimeMachineResponse:
    """ 
        Attributes:
            current_personality (Big5Assessment):
            evolution_events (list[PersonalityDelta] | None):
            mood_at (TimeMachineMoodSnapshot):
            personality_at (Big5Assessment):
            requested_at (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    current_personality: Big5Assessment
    evolution_events: list[PersonalityDelta] | None
    mood_at: TimeMachineMoodSnapshot
    personality_at: Big5Assessment
    requested_at: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.big_5_assessment import Big5Assessment
        from ..models.personality_delta import PersonalityDelta
        from ..models.time_machine_mood_snapshot import TimeMachineMoodSnapshot
        current_personality = self.current_personality.to_dict()

        evolution_events: list[dict[str, Any]] | None
        if isinstance(self.evolution_events, list):
            evolution_events = []
            for evolution_events_type_0_item_data in self.evolution_events:
                evolution_events_type_0_item = evolution_events_type_0_item_data.to_dict()
                evolution_events.append(evolution_events_type_0_item)


        else:
            evolution_events = self.evolution_events

        mood_at = self.mood_at.to_dict()

        personality_at = self.personality_at.to_dict()

        requested_at = self.requested_at

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "current_personality": current_personality,
            "evolution_events": evolution_events,
            "mood_at": mood_at,
            "personality_at": personality_at,
            "requested_at": requested_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.big_5_assessment import Big5Assessment
        from ..models.personality_delta import PersonalityDelta
        from ..models.time_machine_mood_snapshot import TimeMachineMoodSnapshot
        d = dict(src_dict)
        current_personality = Big5Assessment.from_dict(d.pop("current_personality"))




        def _parse_evolution_events(data: object) -> list[PersonalityDelta] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                evolution_events_type_0 = []
                _evolution_events_type_0 = data
                for evolution_events_type_0_item_data in (_evolution_events_type_0):
                    evolution_events_type_0_item = PersonalityDelta.from_dict(evolution_events_type_0_item_data)



                    evolution_events_type_0.append(evolution_events_type_0_item)

                return evolution_events_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PersonalityDelta] | None, data)

        evolution_events = _parse_evolution_events(d.pop("evolution_events"))


        mood_at = TimeMachineMoodSnapshot.from_dict(d.pop("mood_at"))




        personality_at = Big5Assessment.from_dict(d.pop("personality_at"))




        requested_at = d.pop("requested_at")

        schema = d.pop("$schema", UNSET)

        time_machine_response = cls(
            current_personality=current_personality,
            evolution_events=evolution_events,
            mood_at=mood_at,
            personality_at=personality_at,
            requested_at=requested_at,
            schema=schema,
        )

        return time_machine_response

