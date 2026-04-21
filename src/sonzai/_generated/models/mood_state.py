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






T = TypeVar("T", bound="MoodState")



@_attrs_define
class MoodState:
    """ 
        Attributes:
            affiliation (float):
            agent_id (str):
            arousal (float):
            baseline_affiliation (float):
            baseline_arousal (float):
            baseline_tension (float):
            baseline_valence (float):
            created_at (datetime.datetime):
            label (str):
            last_decay_at (datetime.datetime):
            last_interaction_at (datetime.datetime):
            tension (float):
            updated_at (datetime.datetime):
            valence (float):
            user_id (str | Unset):
     """

    affiliation: float
    agent_id: str
    arousal: float
    baseline_affiliation: float
    baseline_arousal: float
    baseline_tension: float
    baseline_valence: float
    created_at: datetime.datetime
    label: str
    last_decay_at: datetime.datetime
    last_interaction_at: datetime.datetime
    tension: float
    updated_at: datetime.datetime
    valence: float
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        affiliation = self.affiliation

        agent_id = self.agent_id

        arousal = self.arousal

        baseline_affiliation = self.baseline_affiliation

        baseline_arousal = self.baseline_arousal

        baseline_tension = self.baseline_tension

        baseline_valence = self.baseline_valence

        created_at = self.created_at.isoformat()

        label = self.label

        last_decay_at = self.last_decay_at.isoformat()

        last_interaction_at = self.last_interaction_at.isoformat()

        tension = self.tension

        updated_at = self.updated_at.isoformat()

        valence = self.valence

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "affiliation": affiliation,
            "agent_id": agent_id,
            "arousal": arousal,
            "baseline_affiliation": baseline_affiliation,
            "baseline_arousal": baseline_arousal,
            "baseline_tension": baseline_tension,
            "baseline_valence": baseline_valence,
            "created_at": created_at,
            "label": label,
            "last_decay_at": last_decay_at,
            "last_interaction_at": last_interaction_at,
            "tension": tension,
            "updated_at": updated_at,
            "valence": valence,
        })
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        affiliation = d.pop("affiliation")

        agent_id = d.pop("agent_id")

        arousal = d.pop("arousal")

        baseline_affiliation = d.pop("baseline_affiliation")

        baseline_arousal = d.pop("baseline_arousal")

        baseline_tension = d.pop("baseline_tension")

        baseline_valence = d.pop("baseline_valence")

        created_at = isoparse(d.pop("created_at"))




        label = d.pop("label")

        last_decay_at = isoparse(d.pop("last_decay_at"))




        last_interaction_at = isoparse(d.pop("last_interaction_at"))




        tension = d.pop("tension")

        updated_at = isoparse(d.pop("updated_at"))




        valence = d.pop("valence")

        user_id = d.pop("user_id", UNSET)

        mood_state = cls(
            affiliation=affiliation,
            agent_id=agent_id,
            arousal=arousal,
            baseline_affiliation=baseline_affiliation,
            baseline_arousal=baseline_arousal,
            baseline_tension=baseline_tension,
            baseline_valence=baseline_valence,
            created_at=created_at,
            label=label,
            last_decay_at=last_decay_at,
            last_interaction_at=last_interaction_at,
            tension=tension,
            updated_at=updated_at,
            valence=valence,
            user_id=user_id,
        )

        return mood_state

