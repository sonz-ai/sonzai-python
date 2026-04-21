from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="MoodHistoryEntry")



@_attrs_define
class MoodHistoryEntry:
    """ 
        Attributes:
            affiliation (float):
            arousal (float):
            tension (float):
            timestamp (str):
            valence (float):
            delta_affiliation (float | Unset):
            delta_arousal (float | Unset):
            delta_tension (float | Unset):
            delta_valence (float | Unset):
            label (str | Unset):
            trigger_reason (str | Unset):
            trigger_type (str | Unset):
     """

    affiliation: float
    arousal: float
    tension: float
    timestamp: str
    valence: float
    delta_affiliation: float | Unset = UNSET
    delta_arousal: float | Unset = UNSET
    delta_tension: float | Unset = UNSET
    delta_valence: float | Unset = UNSET
    label: str | Unset = UNSET
    trigger_reason: str | Unset = UNSET
    trigger_type: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        affiliation = self.affiliation

        arousal = self.arousal

        tension = self.tension

        timestamp = self.timestamp

        valence = self.valence

        delta_affiliation = self.delta_affiliation

        delta_arousal = self.delta_arousal

        delta_tension = self.delta_tension

        delta_valence = self.delta_valence

        label = self.label

        trigger_reason = self.trigger_reason

        trigger_type = self.trigger_type


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "affiliation": affiliation,
            "arousal": arousal,
            "tension": tension,
            "timestamp": timestamp,
            "valence": valence,
        })
        if delta_affiliation is not UNSET:
            field_dict["delta_affiliation"] = delta_affiliation
        if delta_arousal is not UNSET:
            field_dict["delta_arousal"] = delta_arousal
        if delta_tension is not UNSET:
            field_dict["delta_tension"] = delta_tension
        if delta_valence is not UNSET:
            field_dict["delta_valence"] = delta_valence
        if label is not UNSET:
            field_dict["label"] = label
        if trigger_reason is not UNSET:
            field_dict["trigger_reason"] = trigger_reason
        if trigger_type is not UNSET:
            field_dict["trigger_type"] = trigger_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        affiliation = d.pop("affiliation")

        arousal = d.pop("arousal")

        tension = d.pop("tension")

        timestamp = d.pop("timestamp")

        valence = d.pop("valence")

        delta_affiliation = d.pop("delta_affiliation", UNSET)

        delta_arousal = d.pop("delta_arousal", UNSET)

        delta_tension = d.pop("delta_tension", UNSET)

        delta_valence = d.pop("delta_valence", UNSET)

        label = d.pop("label", UNSET)

        trigger_reason = d.pop("trigger_reason", UNSET)

        trigger_type = d.pop("trigger_type", UNSET)

        mood_history_entry = cls(
            affiliation=affiliation,
            arousal=arousal,
            tension=tension,
            timestamp=timestamp,
            valence=valence,
            delta_affiliation=delta_affiliation,
            delta_arousal=delta_arousal,
            delta_tension=delta_tension,
            delta_valence=delta_valence,
            label=label,
            trigger_reason=trigger_reason,
            trigger_type=trigger_type,
        )

        return mood_history_entry

