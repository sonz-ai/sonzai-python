from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="Big5")



@_attrs_define
class Big5:
    """ 
        Attributes:
            agreeableness (float):
            conscientiousness (float):
            extraversion (float):
            neuroticism (float):
            openness (float):
     """

    agreeableness: float
    conscientiousness: float
    extraversion: float
    neuroticism: float
    openness: float





    def to_dict(self) -> dict[str, Any]:
        agreeableness = self.agreeableness

        conscientiousness = self.conscientiousness

        extraversion = self.extraversion

        neuroticism = self.neuroticism

        openness = self.openness


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agreeableness": agreeableness,
            "conscientiousness": conscientiousness,
            "extraversion": extraversion,
            "neuroticism": neuroticism,
            "openness": openness,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agreeableness = d.pop("agreeableness")

        conscientiousness = d.pop("conscientiousness")

        extraversion = d.pop("extraversion")

        neuroticism = d.pop("neuroticism")

        openness = d.pop("openness")

        big_5 = cls(
            agreeableness=agreeableness,
            conscientiousness=conscientiousness,
            extraversion=extraversion,
            neuroticism=neuroticism,
            openness=openness,
        )

        return big_5

