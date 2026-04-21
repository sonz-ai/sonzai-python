from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="WorkbenchStateMood")



@_attrs_define
class WorkbenchStateMood:
    """ 
        Attributes:
            affiliation (float):
            arousal (float):
            label (str):
            tension (float):
            valence (float):
     """

    affiliation: float
    arousal: float
    label: str
    tension: float
    valence: float





    def to_dict(self) -> dict[str, Any]:
        affiliation = self.affiliation

        arousal = self.arousal

        label = self.label

        tension = self.tension

        valence = self.valence


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "affiliation": affiliation,
            "arousal": arousal,
            "label": label,
            "tension": tension,
            "valence": valence,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        affiliation = d.pop("affiliation")

        arousal = d.pop("arousal")

        label = d.pop("label")

        tension = d.pop("tension")

        valence = d.pop("valence")

        workbench_state_mood = cls(
            affiliation=affiliation,
            arousal=arousal,
            label=label,
            tension=tension,
            valence=valence,
        )

        return workbench_state_mood

