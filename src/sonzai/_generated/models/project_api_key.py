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






T = TypeVar("T", bound="ProjectAPIKey")



@_attrs_define
class ProjectAPIKey:
    """ 
        Attributes:
            created_at (datetime.datetime):
            created_by (str):
            is_active (bool):
            is_admin_managed (bool):
            key_id (str):
            key_prefix (str):
            name (str):
            project_id (str):
            scopes (list[str] | None):
            tenant_id (str):
            expires_at (datetime.datetime | Unset):
            last_used_at (datetime.datetime | Unset):
     """

    created_at: datetime.datetime
    created_by: str
    is_active: bool
    is_admin_managed: bool
    key_id: str
    key_prefix: str
    name: str
    project_id: str
    scopes: list[str] | None
    tenant_id: str
    expires_at: datetime.datetime | Unset = UNSET
    last_used_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        is_active = self.is_active

        is_admin_managed = self.is_admin_managed

        key_id = self.key_id

        key_prefix = self.key_prefix

        name = self.name

        project_id = self.project_id

        scopes: list[str] | None
        if isinstance(self.scopes, list):
            scopes = self.scopes


        else:
            scopes = self.scopes

        tenant_id = self.tenant_id

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        last_used_at: str | Unset = UNSET
        if not isinstance(self.last_used_at, Unset):
            last_used_at = self.last_used_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "created_by": created_by,
            "is_active": is_active,
            "is_admin_managed": is_admin_managed,
            "key_id": key_id,
            "key_prefix": key_prefix,
            "name": name,
            "project_id": project_id,
            "scopes": scopes,
            "tenant_id": tenant_id,
        })
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))




        created_by = d.pop("created_by")

        is_active = d.pop("is_active")

        is_admin_managed = d.pop("is_admin_managed")

        key_id = d.pop("key_id")

        key_prefix = d.pop("key_prefix")

        name = d.pop("name")

        project_id = d.pop("project_id")

        def _parse_scopes(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scopes_type_0 = cast(list[str], data)

                return scopes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        scopes = _parse_scopes(d.pop("scopes"))


        tenant_id = d.pop("tenant_id")

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at,  Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)




        _last_used_at = d.pop("last_used_at", UNSET)
        last_used_at: datetime.datetime | Unset
        if isinstance(_last_used_at,  Unset):
            last_used_at = UNSET
        else:
            last_used_at = isoparse(_last_used_at)




        project_api_key = cls(
            created_at=created_at,
            created_by=created_by,
            is_active=is_active,
            is_admin_managed=is_admin_managed,
            key_id=key_id,
            key_prefix=key_prefix,
            name=name,
            project_id=project_id,
            scopes=scopes,
            tenant_id=tenant_id,
            expires_at=expires_at,
            last_used_at=last_used_at,
        )

        return project_api_key

