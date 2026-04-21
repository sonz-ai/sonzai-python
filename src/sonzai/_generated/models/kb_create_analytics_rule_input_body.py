from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="KbCreateAnalyticsRuleInputBody")



@_attrs_define
class KbCreateAnalyticsRuleInputBody:
    """ 
        Attributes:
            config (Any): Rule configuration object
            enabled (bool): Whether the rule is active
            name (str): Rule name
            rule_type (str): Rule type: 'recommendation' or 'trend'
            schema (str | Unset): A URL to the JSON Schema for this object.
            schedule (str | Unset): Optional cron schedule
     """

    config: Any
    enabled: bool
    name: str
    rule_type: str
    schema: str | Unset = UNSET
    schedule: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        config = self.config

        enabled = self.enabled

        name = self.name

        rule_type = self.rule_type

        schema = self.schema

        schedule = self.schedule


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "config": config,
            "enabled": enabled,
            "name": name,
            "rule_type": rule_type,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if schedule is not UNSET:
            field_dict["schedule"] = schedule

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        config = d.pop("config")

        enabled = d.pop("enabled")

        name = d.pop("name")

        rule_type = d.pop("rule_type")

        schema = d.pop("$schema", UNSET)

        schedule = d.pop("schedule", UNSET)

        kb_create_analytics_rule_input_body = cls(
            config=config,
            enabled=enabled,
            name=name,
            rule_type=rule_type,
            schema=schema,
            schedule=schedule,
        )

        return kb_create_analytics_rule_input_body

