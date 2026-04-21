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






T = TypeVar("T", bound="UserPersonaRecord")



@_attrs_define
class UserPersonaRecord:
    """ 
        Attributes:
            created_at (datetime.datetime):
            description (str):
            is_default (bool):
            name (str):
            persona_id (str):
            style (str):
            updated_at (datetime.datetime):
            schema (str | Unset): A URL to the JSON Schema for this object.
            tenant_id (str | Unset):
     """

    created_at: datetime.datetime
    description: str
    is_default: bool
    name: str
    persona_id: str
    style: str
    updated_at: datetime.datetime
    schema: str | Unset = UNSET
    tenant_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        description = self.description

        is_default = self.is_default

        name = self.name

        persona_id = self.persona_id

        style = self.style

        updated_at = self.updated_at.isoformat()

        schema = self.schema

        tenant_id = self.tenant_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "description": description,
            "is_default": is_default,
            "name": name,
            "persona_id": persona_id,
            "style": style,
            "updated_at": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))




        description = d.pop("description")

        is_default = d.pop("is_default")

        name = d.pop("name")

        persona_id = d.pop("persona_id")

        style = d.pop("style")

        updated_at = isoparse(d.pop("updated_at"))




        schema = d.pop("$schema", UNSET)

        tenant_id = d.pop("tenant_id", UNSET)

        user_persona_record = cls(
            created_at=created_at,
            description=description,
            is_default=is_default,
            name=name,
            persona_id=persona_id,
            style=style,
            updated_at=updated_at,
            schema=schema,
            tenant_id=tenant_id,
        )

        return user_persona_record

