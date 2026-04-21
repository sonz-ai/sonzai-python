from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="TraitPrecision")



@_attrs_define
class TraitPrecision:
    """ 
        Attributes:
            last_updated_at (datetime.datetime):
            observation_count (int):
            precision (float):
     """

    last_updated_at: datetime.datetime
    observation_count: int
    precision: float





    def to_dict(self) -> dict[str, Any]:
        last_updated_at = self.last_updated_at.isoformat()

        observation_count = self.observation_count

        precision = self.precision


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "last_updated_at": last_updated_at,
            "observation_count": observation_count,
            "precision": precision,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        last_updated_at = isoparse(d.pop("last_updated_at"))




        observation_count = d.pop("observation_count")

        precision = d.pop("precision")

        trait_precision = cls(
            last_updated_at=last_updated_at,
            observation_count=observation_count,
            precision=precision,
        )

        return trait_precision

