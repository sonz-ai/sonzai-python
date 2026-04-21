from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="Dimensions")



@_attrs_define
class Dimensions:
    """ 
        Attributes:
            aesthetic (float):
            assertiveness (float):
            compassion (float):
            enthusiasm (float):
            industriousness (float):
            intellect (float):
            orderliness (float):
            politeness (float):
            volatility (float):
            withdrawal (float):
     """

    aesthetic: float
    assertiveness: float
    compassion: float
    enthusiasm: float
    industriousness: float
    intellect: float
    orderliness: float
    politeness: float
    volatility: float
    withdrawal: float





    def to_dict(self) -> dict[str, Any]:
        aesthetic = self.aesthetic

        assertiveness = self.assertiveness

        compassion = self.compassion

        enthusiasm = self.enthusiasm

        industriousness = self.industriousness

        intellect = self.intellect

        orderliness = self.orderliness

        politeness = self.politeness

        volatility = self.volatility

        withdrawal = self.withdrawal


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "aesthetic": aesthetic,
            "assertiveness": assertiveness,
            "compassion": compassion,
            "enthusiasm": enthusiasm,
            "industriousness": industriousness,
            "intellect": intellect,
            "orderliness": orderliness,
            "politeness": politeness,
            "volatility": volatility,
            "withdrawal": withdrawal,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        aesthetic = d.pop("aesthetic")

        assertiveness = d.pop("assertiveness")

        compassion = d.pop("compassion")

        enthusiasm = d.pop("enthusiasm")

        industriousness = d.pop("industriousness")

        intellect = d.pop("intellect")

        orderliness = d.pop("orderliness")

        politeness = d.pop("politeness")

        volatility = d.pop("volatility")

        withdrawal = d.pop("withdrawal")

        dimensions = cls(
            aesthetic=aesthetic,
            assertiveness=assertiveness,
            compassion=compassion,
            enthusiasm=enthusiasm,
            industriousness=industriousness,
            intellect=intellect,
            orderliness=orderliness,
            politeness=politeness,
            volatility=volatility,
            withdrawal=withdrawal,
        )

        return dimensions

