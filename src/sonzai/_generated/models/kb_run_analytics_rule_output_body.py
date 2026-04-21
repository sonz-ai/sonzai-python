from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="KbRunAnalyticsRuleOutputBody")



@_attrs_define
class KbRunAnalyticsRuleOutputBody:
    """ 
        Attributes:
            message (str): Human-readable message
            rule_id (str): Rule that was triggered
            status (str): Accepted status
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    message: str
    rule_id: str
    status: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        message = self.message

        rule_id = self.rule_id

        status = self.status

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "message": message,
            "rule_id": rule_id,
            "status": status,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        rule_id = d.pop("rule_id")

        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        kb_run_analytics_rule_output_body = cls(
            message=message,
            rule_id=rule_id,
            status=status,
            schema=schema,
        )

        return kb_run_analytics_rule_output_body

