from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.kb_conversion_stats_top_features import KBConversionStatsTopFeatures





T = TypeVar("T", bound="KBConversionStats")



@_attrs_define
class KBConversionStats:
    """ 
        Attributes:
            avg_days_to_convert (float):
            computed_at (datetime.datetime):
            conversion_count (int):
            conversion_rate (float):
            project_id (str):
            rule_id (str):
            segment_key (str):
            shown_count (int):
            target_type (str):
            top_features (KBConversionStatsTopFeatures):
            total_leads (int):
     """

    avg_days_to_convert: float
    computed_at: datetime.datetime
    conversion_count: int
    conversion_rate: float
    project_id: str
    rule_id: str
    segment_key: str
    shown_count: int
    target_type: str
    top_features: KBConversionStatsTopFeatures
    total_leads: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_conversion_stats_top_features import KBConversionStatsTopFeatures
        avg_days_to_convert = self.avg_days_to_convert

        computed_at = self.computed_at.isoformat()

        conversion_count = self.conversion_count

        conversion_rate = self.conversion_rate

        project_id = self.project_id

        rule_id = self.rule_id

        segment_key = self.segment_key

        shown_count = self.shown_count

        target_type = self.target_type

        top_features = self.top_features.to_dict()

        total_leads = self.total_leads


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "avg_days_to_convert": avg_days_to_convert,
            "computed_at": computed_at,
            "conversion_count": conversion_count,
            "conversion_rate": conversion_rate,
            "project_id": project_id,
            "rule_id": rule_id,
            "segment_key": segment_key,
            "shown_count": shown_count,
            "target_type": target_type,
            "top_features": top_features,
            "total_leads": total_leads,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_conversion_stats_top_features import KBConversionStatsTopFeatures
        d = dict(src_dict)
        avg_days_to_convert = d.pop("avg_days_to_convert")

        computed_at = isoparse(d.pop("computed_at"))




        conversion_count = d.pop("conversion_count")

        conversion_rate = d.pop("conversion_rate")

        project_id = d.pop("project_id")

        rule_id = d.pop("rule_id")

        segment_key = d.pop("segment_key")

        shown_count = d.pop("shown_count")

        target_type = d.pop("target_type")

        top_features = KBConversionStatsTopFeatures.from_dict(d.pop("top_features"))




        total_leads = d.pop("total_leads")

        kb_conversion_stats = cls(
            avg_days_to_convert=avg_days_to_convert,
            computed_at=computed_at,
            conversion_count=conversion_count,
            conversion_rate=conversion_rate,
            project_id=project_id,
            rule_id=rule_id,
            segment_key=segment_key,
            shown_count=shown_count,
            target_type=target_type,
            top_features=top_features,
            total_leads=total_leads,
        )

        return kb_conversion_stats

