from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_trend_ranking import KBTrendRanking





T = TypeVar("T", bound="KbGetTrendRankingsOutputBody")



@_attrs_define
class KbGetTrendRankingsOutputBody:
    """ 
        Attributes:
            rankings (list[KBTrendRanking] | None): Ranked trends
            total (int): Total count
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    rankings: list[KBTrendRanking] | None
    total: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_trend_ranking import KBTrendRanking
        rankings: list[dict[str, Any]] | None
        if isinstance(self.rankings, list):
            rankings = []
            for rankings_type_0_item_data in self.rankings:
                rankings_type_0_item = rankings_type_0_item_data.to_dict()
                rankings.append(rankings_type_0_item)


        else:
            rankings = self.rankings

        total = self.total

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "rankings": rankings,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_trend_ranking import KBTrendRanking
        d = dict(src_dict)
        def _parse_rankings(data: object) -> list[KBTrendRanking] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                rankings_type_0 = []
                _rankings_type_0 = data
                for rankings_type_0_item_data in (_rankings_type_0):
                    rankings_type_0_item = KBTrendRanking.from_dict(rankings_type_0_item_data)



                    rankings_type_0.append(rankings_type_0_item)

                return rankings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBTrendRanking] | None, data)

        rankings = _parse_rankings(d.pop("rankings"))


        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        kb_get_trend_rankings_output_body = cls(
            rankings=rankings,
            total=total,
            schema=schema,
        )

        return kb_get_trend_rankings_output_body

