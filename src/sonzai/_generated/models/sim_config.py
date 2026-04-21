from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="SimConfig")



@_attrs_define
class SimConfig:
    """ 
        Attributes:
            enable_consolidation (bool):
            enable_diary (bool):
            enable_proactive (bool):
            max_sessions (int):
            max_turns_per_session (int):
            simulated_duration_hours (int):
            disable_ce_enrichment (bool | Unset):
            inter_session_gap_hours (int | Unset):
            model (str | Unset):
            playback_speed (float | Unset):
     """

    enable_consolidation: bool
    enable_diary: bool
    enable_proactive: bool
    max_sessions: int
    max_turns_per_session: int
    simulated_duration_hours: int
    disable_ce_enrichment: bool | Unset = UNSET
    inter_session_gap_hours: int | Unset = UNSET
    model: str | Unset = UNSET
    playback_speed: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        enable_consolidation = self.enable_consolidation

        enable_diary = self.enable_diary

        enable_proactive = self.enable_proactive

        max_sessions = self.max_sessions

        max_turns_per_session = self.max_turns_per_session

        simulated_duration_hours = self.simulated_duration_hours

        disable_ce_enrichment = self.disable_ce_enrichment

        inter_session_gap_hours = self.inter_session_gap_hours

        model = self.model

        playback_speed = self.playback_speed


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "enable_consolidation": enable_consolidation,
            "enable_diary": enable_diary,
            "enable_proactive": enable_proactive,
            "max_sessions": max_sessions,
            "max_turns_per_session": max_turns_per_session,
            "simulated_duration_hours": simulated_duration_hours,
        })
        if disable_ce_enrichment is not UNSET:
            field_dict["disable_ce_enrichment"] = disable_ce_enrichment
        if inter_session_gap_hours is not UNSET:
            field_dict["inter_session_gap_hours"] = inter_session_gap_hours
        if model is not UNSET:
            field_dict["model"] = model
        if playback_speed is not UNSET:
            field_dict["playback_speed"] = playback_speed

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enable_consolidation = d.pop("enable_consolidation")

        enable_diary = d.pop("enable_diary")

        enable_proactive = d.pop("enable_proactive")

        max_sessions = d.pop("max_sessions")

        max_turns_per_session = d.pop("max_turns_per_session")

        simulated_duration_hours = d.pop("simulated_duration_hours")

        disable_ce_enrichment = d.pop("disable_ce_enrichment", UNSET)

        inter_session_gap_hours = d.pop("inter_session_gap_hours", UNSET)

        model = d.pop("model", UNSET)

        playback_speed = d.pop("playback_speed", UNSET)

        sim_config = cls(
            enable_consolidation=enable_consolidation,
            enable_diary=enable_diary,
            enable_proactive=enable_proactive,
            max_sessions=max_sessions,
            max_turns_per_session=max_turns_per_session,
            simulated_duration_hours=simulated_duration_hours,
            disable_ce_enrichment=disable_ce_enrichment,
            inter_session_gap_hours=inter_session_gap_hours,
            model=model,
            playback_speed=playback_speed,
        )

        return sim_config

