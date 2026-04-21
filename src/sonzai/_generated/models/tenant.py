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






T = TypeVar("T", bound="Tenant")



@_attrs_define
class Tenant:
    """ 
        Attributes:
            created_at (datetime.datetime):
            is_active (bool):
            name (str):
            tenant_id (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            clerk_org_id (str | Unset):
            license_key_id (str | Unset):
            slug (str | Unset):
     """

    created_at: datetime.datetime
    is_active: bool
    name: str
    tenant_id: str
    schema: str | Unset = UNSET
    clerk_org_id: str | Unset = UNSET
    license_key_id: str | Unset = UNSET
    slug: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        is_active = self.is_active

        name = self.name

        tenant_id = self.tenant_id

        schema = self.schema

        clerk_org_id = self.clerk_org_id

        license_key_id = self.license_key_id

        slug = self.slug


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "is_active": is_active,
            "name": name,
            "tenant_id": tenant_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if clerk_org_id is not UNSET:
            field_dict["clerk_org_id"] = clerk_org_id
        if license_key_id is not UNSET:
            field_dict["license_key_id"] = license_key_id
        if slug is not UNSET:
            field_dict["slug"] = slug

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))




        is_active = d.pop("is_active")

        name = d.pop("name")

        tenant_id = d.pop("tenant_id")

        schema = d.pop("$schema", UNSET)

        clerk_org_id = d.pop("clerk_org_id", UNSET)

        license_key_id = d.pop("license_key_id", UNSET)

        slug = d.pop("slug", UNSET)

        tenant = cls(
            created_at=created_at,
            is_active=is_active,
            name=name,
            tenant_id=tenant_id,
            schema=schema,
            clerk_org_id=clerk_org_id,
            license_key_id=license_key_id,
            slug=slug,
        )

        return tenant

