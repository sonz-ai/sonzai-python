from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="KbRecordFeedbackInputBody")



@_attrs_define
class KbRecordFeedbackInputBody:
    """ 
        Attributes:
            converted (bool): Whether the recommendation converted
            rule_id (str): Rule ID
            score_at_time (float): Score at time of recommendation
            source_node_id (str): Source node ID
            target_node_id (str): Target node ID
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    converted: bool
    rule_id: str
    score_at_time: float
    source_node_id: str
    target_node_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        converted = self.converted

        rule_id = self.rule_id

        score_at_time = self.score_at_time

        source_node_id = self.source_node_id

        target_node_id = self.target_node_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "converted": converted,
            "rule_id": rule_id,
            "score_at_time": score_at_time,
            "source_node_id": source_node_id,
            "target_node_id": target_node_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        converted = d.pop("converted")

        rule_id = d.pop("rule_id")

        score_at_time = d.pop("score_at_time")

        source_node_id = d.pop("source_node_id")

        target_node_id = d.pop("target_node_id")

        schema = d.pop("$schema", UNSET)

        kb_record_feedback_input_body = cls(
            converted=converted,
            rule_id=rule_id,
            score_at_time=score_at_time,
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            schema=schema,
        )

        return kb_record_feedback_input_body

