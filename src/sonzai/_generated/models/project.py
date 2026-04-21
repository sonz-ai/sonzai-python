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






T = TypeVar("T", bound="Project")



@_attrs_define
class Project:
    """ 
        Attributes:
            created_at (datetime.datetime):
            environment (str):
            game_name (str):
            is_active (bool):
            name (str):
            project_id (str):
            tenant_id (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    created_at: datetime.datetime
    environment: str
    game_name: str
    is_active: bool
    name: str
    project_id: str
    tenant_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        environment = self.environment

        game_name = self.game_name

        is_active = self.is_active

        name = self.name

        project_id = self.project_id

        tenant_id = self.tenant_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "environment": environment,
            "game_name": game_name,
            "is_active": is_active,
            "name": name,
            "project_id": project_id,
            "tenant_id": tenant_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))




        environment = d.pop("environment")

        game_name = d.pop("game_name")

        is_active = d.pop("is_active")

        name = d.pop("name")

        project_id = d.pop("project_id")

        tenant_id = d.pop("tenant_id")

        schema = d.pop("$schema", UNSET)

        project = cls(
            created_at=created_at,
            environment=environment,
            game_name=game_name,
            is_active=is_active,
            name=name,
            project_id=project_id,
            tenant_id=tenant_id,
            schema=schema,
        )

        return project

