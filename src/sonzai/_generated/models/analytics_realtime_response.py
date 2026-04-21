from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.analytics_overview import AnalyticsOverview
  from ..models.daily_stats_entry import DailyStatsEntry





T = TypeVar("T", bound="AnalyticsRealtimeResponse")



@_attrs_define
class AnalyticsRealtimeResponse:
    """ 
        Attributes:
            daily (list[DailyStatsEntry] | None):
            overview (AnalyticsOverview):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    daily: list[DailyStatsEntry] | None
    overview: AnalyticsOverview
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.analytics_overview import AnalyticsOverview
        from ..models.daily_stats_entry import DailyStatsEntry
        daily: list[dict[str, Any]] | None
        if isinstance(self.daily, list):
            daily = []
            for daily_type_0_item_data in self.daily:
                daily_type_0_item = daily_type_0_item_data.to_dict()
                daily.append(daily_type_0_item)


        else:
            daily = self.daily

        overview = self.overview.to_dict()

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "daily": daily,
            "overview": overview,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.analytics_overview import AnalyticsOverview
        from ..models.daily_stats_entry import DailyStatsEntry
        d = dict(src_dict)
        def _parse_daily(data: object) -> list[DailyStatsEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                daily_type_0 = []
                _daily_type_0 = data
                for daily_type_0_item_data in (_daily_type_0):
                    daily_type_0_item = DailyStatsEntry.from_dict(daily_type_0_item_data)



                    daily_type_0.append(daily_type_0_item)

                return daily_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DailyStatsEntry] | None, data)

        daily = _parse_daily(d.pop("daily"))


        overview = AnalyticsOverview.from_dict(d.pop("overview"))




        schema = d.pop("$schema", UNSET)

        analytics_realtime_response = cls(
            daily=daily,
            overview=overview,
            schema=schema,
        )

        return analytics_realtime_response

