from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="KBAnalyticsRule")



@_attrs_define
class KBAnalyticsRule:
    """ 
        Attributes:
            config (Any):
            created_at (datetime.datetime):
            enabled (bool):
            last_run_at (datetime.datetime):
            last_run_duration_ms (int):
            last_run_status (str):
            name (str):
            project_id (str):
            rule_id (str):
            rule_type (str):
            schedule (str):
            updated_at (datetime.datetime):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    config: Any
    created_at: datetime.datetime
    enabled: bool
    last_run_at: datetime.datetime
    last_run_duration_ms: int
    last_run_status: str
    name: str
    project_id: str
    rule_id: str
    rule_type: str
    schedule: str
    updated_at: datetime.datetime
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        config = self.config

        created_at = self.created_at.isoformat()

        enabled = self.enabled

        last_run_at = self.last_run_at.isoformat()

        last_run_duration_ms = self.last_run_duration_ms

        last_run_status = self.last_run_status

        name = self.name

        project_id = self.project_id

        rule_id = self.rule_id

        rule_type = self.rule_type

        schedule = self.schedule

        updated_at = self.updated_at.isoformat()

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "config": config,
            "created_at": created_at,
            "enabled": enabled,
            "last_run_at": last_run_at,
            "last_run_duration_ms": last_run_duration_ms,
            "last_run_status": last_run_status,
            "name": name,
            "project_id": project_id,
            "rule_id": rule_id,
            "rule_type": rule_type,
            "schedule": schedule,
            "updated_at": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        config = d.pop("config")

        created_at = isoparse(d.pop("created_at"))




        enabled = d.pop("enabled")

        last_run_at = isoparse(d.pop("last_run_at"))




        last_run_duration_ms = d.pop("last_run_duration_ms")

        last_run_status = d.pop("last_run_status")

        name = d.pop("name")

        project_id = d.pop("project_id")

        rule_id = d.pop("rule_id")

        rule_type = d.pop("rule_type")

        schedule = d.pop("schedule")

        updated_at = isoparse(d.pop("updated_at"))




        schema = d.pop("$schema", UNSET)

        kb_analytics_rule = cls(
            config=config,
            created_at=created_at,
            enabled=enabled,
            last_run_at=last_run_at,
            last_run_duration_ms=last_run_duration_ms,
            last_run_status=last_run_status,
            name=name,
            project_id=project_id,
            rule_id=rule_id,
            rule_type=rule_type,
            schedule=schedule,
            updated_at=updated_at,
            schema=schema,
        )

        return kb_analytics_rule

