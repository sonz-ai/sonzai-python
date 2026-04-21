from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_trend_aggregation import KBTrendAggregation





T = TypeVar("T", bound="KbGetTrendsOutputBody")



@_attrs_define
class KbGetTrendsOutputBody:
    """ 
        Attributes:
            total (int): Total count
            trends (list[KBTrendAggregation] | None): Trend aggregations
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    total: int
    trends: list[KBTrendAggregation] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_trend_aggregation import KBTrendAggregation
        total = self.total

        trends: list[dict[str, Any]] | None
        if isinstance(self.trends, list):
            trends = []
            for trends_type_0_item_data in self.trends:
                trends_type_0_item = trends_type_0_item_data.to_dict()
                trends.append(trends_type_0_item)


        else:
            trends = self.trends

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "total": total,
            "trends": trends,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_trend_aggregation import KBTrendAggregation
        d = dict(src_dict)
        total = d.pop("total")

        def _parse_trends(data: object) -> list[KBTrendAggregation] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                trends_type_0 = []
                _trends_type_0 = data
                for trends_type_0_item_data in (_trends_type_0):
                    trends_type_0_item = KBTrendAggregation.from_dict(trends_type_0_item_data)



                    trends_type_0.append(trends_type_0_item)

                return trends_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBTrendAggregation] | None, data)

        trends = _parse_trends(d.pop("trends"))


        schema = d.pop("$schema", UNSET)

        kb_get_trends_output_body = cls(
            total=total,
            trends=trends,
            schema=schema,
        )

        return kb_get_trends_output_body

