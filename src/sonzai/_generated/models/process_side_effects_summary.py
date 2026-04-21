from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ProcessSideEffectsSummary")



@_attrs_define
class ProcessSideEffectsSummary:
    """ 
        Attributes:
            habits_observed (int):
            interests_detected (int):
            mood_updated (bool):
            personality_updated (bool):
     """

    habits_observed: int
    interests_detected: int
    mood_updated: bool
    personality_updated: bool





    def to_dict(self) -> dict[str, Any]:
        habits_observed = self.habits_observed

        interests_detected = self.interests_detected

        mood_updated = self.mood_updated

        personality_updated = self.personality_updated


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "habits_observed": habits_observed,
            "interests_detected": interests_detected,
            "mood_updated": mood_updated,
            "personality_updated": personality_updated,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        habits_observed = d.pop("habits_observed")

        interests_detected = d.pop("interests_detected")

        mood_updated = d.pop("mood_updated")

        personality_updated = d.pop("personality_updated")

        process_side_effects_summary = cls(
            habits_observed=habits_observed,
            interests_detected=interests_detected,
            mood_updated=mood_updated,
            personality_updated=personality_updated,
        )

        return process_side_effects_summary

