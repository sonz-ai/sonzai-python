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
  from ..models.kb_recommendation_score_reasoning import KBRecommendationScoreReasoning





T = TypeVar("T", bound="KBRecommendationScore")



@_attrs_define
class KBRecommendationScore:
    """ 
        Attributes:
            computed_at (datetime.datetime):
            project_id (str):
            reasoning (KBRecommendationScoreReasoning):
            rule_id (str):
            score (float):
            source_node_id (str):
            target_label (str):
            target_node_id (str):
            target_type (str):
     """

    computed_at: datetime.datetime
    project_id: str
    reasoning: KBRecommendationScoreReasoning
    rule_id: str
    score: float
    source_node_id: str
    target_label: str
    target_node_id: str
    target_type: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_recommendation_score_reasoning import KBRecommendationScoreReasoning
        computed_at = self.computed_at.isoformat()

        project_id = self.project_id

        reasoning = self.reasoning.to_dict()

        rule_id = self.rule_id

        score = self.score

        source_node_id = self.source_node_id

        target_label = self.target_label

        target_node_id = self.target_node_id

        target_type = self.target_type


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "computed_at": computed_at,
            "project_id": project_id,
            "reasoning": reasoning,
            "rule_id": rule_id,
            "score": score,
            "source_node_id": source_node_id,
            "target_label": target_label,
            "target_node_id": target_node_id,
            "target_type": target_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_recommendation_score_reasoning import KBRecommendationScoreReasoning
        d = dict(src_dict)
        computed_at = isoparse(d.pop("computed_at"))




        project_id = d.pop("project_id")

        reasoning = KBRecommendationScoreReasoning.from_dict(d.pop("reasoning"))




        rule_id = d.pop("rule_id")

        score = d.pop("score")

        source_node_id = d.pop("source_node_id")

        target_label = d.pop("target_label")

        target_node_id = d.pop("target_node_id")

        target_type = d.pop("target_type")

        kb_recommendation_score = cls(
            computed_at=computed_at,
            project_id=project_id,
            reasoning=reasoning,
            rule_id=rule_id,
            score=score,
            source_node_id=source_node_id,
            target_label=target_label,
            target_node_id=target_node_id,
            target_type=target_type,
        )

        return kb_recommendation_score

