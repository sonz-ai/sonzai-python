from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="KbUpdateAnalyticsRuleInputBody")



@_attrs_define
class KbUpdateAnalyticsRuleInputBody:
    """ 
        Attributes:
            enabled (bool): Whether the rule is active
            schema (str | Unset): A URL to the JSON Schema for this object.
            config (Any | Unset): Updated rule configuration
            name (str | Unset): Updated rule name
            schedule (str | Unset): Updated schedule
     """

    enabled: bool
    schema: str | Unset = UNSET
    config: Any | Unset = UNSET
    name: str | Unset = UNSET
    schedule: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        schema = self.schema

        config = self.config

        name = self.name

        schedule = self.schedule


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "enabled": enabled,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if config is not UNSET:
            field_dict["config"] = config
        if name is not UNSET:
            field_dict["name"] = name
        if schedule is not UNSET:
            field_dict["schedule"] = schedule

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        schema = d.pop("$schema", UNSET)

        config = d.pop("config", UNSET)

        name = d.pop("name", UNSET)

        schedule = d.pop("schedule", UNSET)

        kb_update_analytics_rule_input_body = cls(
            enabled=enabled,
            schema=schema,
            config=config,
            name=name,
            schedule=schedule,
        )

        return kb_update_analytics_rule_input_body

