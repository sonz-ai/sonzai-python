from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.big_5_trait import Big5Trait





T = TypeVar("T", bound="Big5Assessment")



@_attrs_define
class Big5Assessment:
    """ 
        Attributes:
            agreeableness (Big5Trait):
            conscientiousness (Big5Trait):
            extraversion (Big5Trait):
            neuroticism (Big5Trait):
            openness (Big5Trait):
     """

    agreeableness: Big5Trait
    conscientiousness: Big5Trait
    extraversion: Big5Trait
    neuroticism: Big5Trait
    openness: Big5Trait





    def to_dict(self) -> dict[str, Any]:
        from ..models.big_5_trait import Big5Trait
        agreeableness = self.agreeableness.to_dict()

        conscientiousness = self.conscientiousness.to_dict()

        extraversion = self.extraversion.to_dict()

        neuroticism = self.neuroticism.to_dict()

        openness = self.openness.to_dict()


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
        from ..models.big_5_trait import Big5Trait
        d = dict(src_dict)
        agreeableness = Big5Trait.from_dict(d.pop("agreeableness"))




        conscientiousness = Big5Trait.from_dict(d.pop("conscientiousness"))




        extraversion = Big5Trait.from_dict(d.pop("extraversion"))




        neuroticism = Big5Trait.from_dict(d.pop("neuroticism"))




        openness = Big5Trait.from_dict(d.pop("openness"))




        big_5_assessment = cls(
            agreeableness=agreeableness,
            conscientiousness=conscientiousness,
            extraversion=extraversion,
            neuroticism=neuroticism,
            openness=openness,
        )

        return big_5_assessment

