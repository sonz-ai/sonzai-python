from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="KBTrendRanking")



@_attrs_define
class KBTrendRanking:
    """ 
        Attributes:
            computed_at (datetime.datetime):
            node_id (str):
            node_label (str):
            project_id (str):
            rank (int):
            ranking_type (str):
            rule_id (str):
            value (float):
            window (str):
     """

    computed_at: datetime.datetime
    node_id: str
    node_label: str
    project_id: str
    rank: int
    ranking_type: str
    rule_id: str
    value: float
    window: str





    def to_dict(self) -> dict[str, Any]:
        computed_at = self.computed_at.isoformat()

        node_id = self.node_id

        node_label = self.node_label

        project_id = self.project_id

        rank = self.rank

        ranking_type = self.ranking_type

        rule_id = self.rule_id

        value = self.value

        window = self.window


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "computed_at": computed_at,
            "node_id": node_id,
            "node_label": node_label,
            "project_id": project_id,
            "rank": rank,
            "ranking_type": ranking_type,
            "rule_id": rule_id,
            "value": value,
            "window": window,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        computed_at = isoparse(d.pop("computed_at"))




        node_id = d.pop("node_id")

        node_label = d.pop("node_label")

        project_id = d.pop("project_id")

        rank = d.pop("rank")

        ranking_type = d.pop("ranking_type")

        rule_id = d.pop("rule_id")

        value = d.pop("value")

        window = d.pop("window")

        kb_trend_ranking = cls(
            computed_at=computed_at,
            node_id=node_id,
            node_label=node_label,
            project_id=project_id,
            rank=rank,
            ranking_type=ranking_type,
            rule_id=rule_id,
            value=value,
            window=window,
        )

        return kb_trend_ranking

