from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="Big5Trait")



@_attrs_define
class Big5Trait:
    """ 
        Attributes:
            confidence (float):
            score (float):
            facets (list[str] | None | Unset):
            level (str | Unset):
     """

    confidence: float
    score: float
    facets: list[str] | None | Unset = UNSET
    level: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        confidence = self.confidence

        score = self.score

        facets: list[str] | None | Unset
        if isinstance(self.facets, Unset):
            facets = UNSET
        elif isinstance(self.facets, list):
            facets = self.facets


        else:
            facets = self.facets

        level = self.level


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "confidence": confidence,
            "score": score,
        })
        if facets is not UNSET:
            field_dict["facets"] = facets
        if level is not UNSET:
            field_dict["level"] = level

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        confidence = d.pop("confidence")

        score = d.pop("score")

        def _parse_facets(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                facets_type_0 = cast(list[str], data)

                return facets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        facets = _parse_facets(d.pop("facets", UNSET))


        level = d.pop("level", UNSET)

        big_5_trait = cls(
            confidence=confidence,
            score=score,
            facets=facets,
            level=level,
        )

        return big_5_trait

