from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="KBTrendAggregation")



@_attrs_define
class KBTrendAggregation:
    """ 
        Attributes:
            computed_at (datetime.datetime):
            max_value (float):
            metric_name (str):
            min_value (float):
            node_id (str):
            project_id (str):
            sample_count (int):
            value (float):
            window (str):
     """

    computed_at: datetime.datetime
    max_value: float
    metric_name: str
    min_value: float
    node_id: str
    project_id: str
    sample_count: int
    value: float
    window: str





    def to_dict(self) -> dict[str, Any]:
        computed_at = self.computed_at.isoformat()

        max_value = self.max_value

        metric_name = self.metric_name

        min_value = self.min_value

        node_id = self.node_id

        project_id = self.project_id

        sample_count = self.sample_count

        value = self.value

        window = self.window


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "computed_at": computed_at,
            "max_value": max_value,
            "metric_name": metric_name,
            "min_value": min_value,
            "node_id": node_id,
            "project_id": project_id,
            "sample_count": sample_count,
            "value": value,
            "window": window,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        computed_at = isoparse(d.pop("computed_at"))




        max_value = d.pop("max_value")

        metric_name = d.pop("metric_name")

        min_value = d.pop("min_value")

        node_id = d.pop("node_id")

        project_id = d.pop("project_id")

        sample_count = d.pop("sample_count")

        value = d.pop("value")

        window = d.pop("window")

        kb_trend_aggregation = cls(
            computed_at=computed_at,
            max_value=max_value,
            metric_name=metric_name,
            min_value=min_value,
            node_id=node_id,
            project_id=project_id,
            sample_count=sample_count,
            value=value,
            window=window,
        )

        return kb_trend_aggregation

