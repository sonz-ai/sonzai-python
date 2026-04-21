from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="WorkbenchGenerateCharacterBig5")



@_attrs_define
class WorkbenchGenerateCharacterBig5:
    """ 
        Attributes:
            agreeableness (float):
            conscientiousness (float):
            extraversion (float):
            neuroticism (float):
            openness (float):
            confidence (float | Unset):
     """

    agreeableness: float
    conscientiousness: float
    extraversion: float
    neuroticism: float
    openness: float
    confidence: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agreeableness = self.agreeableness

        conscientiousness = self.conscientiousness

        extraversion = self.extraversion

        neuroticism = self.neuroticism

        openness = self.openness

        confidence = self.confidence


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agreeableness": agreeableness,
            "conscientiousness": conscientiousness,
            "extraversion": extraversion,
            "neuroticism": neuroticism,
            "openness": openness,
        })
        if confidence is not UNSET:
            field_dict["confidence"] = confidence

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agreeableness = d.pop("agreeableness")

        conscientiousness = d.pop("conscientiousness")

        extraversion = d.pop("extraversion")

        neuroticism = d.pop("neuroticism")

        openness = d.pop("openness")

        confidence = d.pop("confidence", UNSET)

        workbench_generate_character_big_5 = cls(
            agreeableness=agreeableness,
            conscientiousness=conscientiousness,
            extraversion=extraversion,
            neuroticism=neuroticism,
            openness=openness,
            confidence=confidence,
        )

        return workbench_generate_character_big_5

