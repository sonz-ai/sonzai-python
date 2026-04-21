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






T = TypeVar("T", bound="AgentIndex")



@_attrs_define
class AgentIndex:
    """ 
        Attributes:
            agent_id (str):
            created_at (datetime.datetime):
            instance_count (int):
            is_active (bool):
            owner_user_id (str):
            tenant_id (str):
            last_seen_at (datetime.datetime | Unset):
            name (str | Unset):
            owner_display_name (str | Unset):
            owner_email (str | Unset):
            project_id (str | Unset):
     """

    agent_id: str
    created_at: datetime.datetime
    instance_count: int
    is_active: bool
    owner_user_id: str
    tenant_id: str
    last_seen_at: datetime.datetime | Unset = UNSET
    name: str | Unset = UNSET
    owner_display_name: str | Unset = UNSET
    owner_email: str | Unset = UNSET
    project_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        created_at = self.created_at.isoformat()

        instance_count = self.instance_count

        is_active = self.is_active

        owner_user_id = self.owner_user_id

        tenant_id = self.tenant_id

        last_seen_at: str | Unset = UNSET
        if not isinstance(self.last_seen_at, Unset):
            last_seen_at = self.last_seen_at.isoformat()

        name = self.name

        owner_display_name = self.owner_display_name

        owner_email = self.owner_email

        project_id = self.project_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "created_at": created_at,
            "instance_count": instance_count,
            "is_active": is_active,
            "owner_user_id": owner_user_id,
            "tenant_id": tenant_id,
        })
        if last_seen_at is not UNSET:
            field_dict["last_seen_at"] = last_seen_at
        if name is not UNSET:
            field_dict["name"] = name
        if owner_display_name is not UNSET:
            field_dict["owner_display_name"] = owner_display_name
        if owner_email is not UNSET:
            field_dict["owner_email"] = owner_email
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        created_at = isoparse(d.pop("created_at"))




        instance_count = d.pop("instance_count")

        is_active = d.pop("is_active")

        owner_user_id = d.pop("owner_user_id")

        tenant_id = d.pop("tenant_id")

        _last_seen_at = d.pop("last_seen_at", UNSET)
        last_seen_at: datetime.datetime | Unset
        if isinstance(_last_seen_at,  Unset):
            last_seen_at = UNSET
        else:
            last_seen_at = isoparse(_last_seen_at)




        name = d.pop("name", UNSET)

        owner_display_name = d.pop("owner_display_name", UNSET)

        owner_email = d.pop("owner_email", UNSET)

        project_id = d.pop("project_id", UNSET)

        agent_index = cls(
            agent_id=agent_id,
            created_at=created_at,
            instance_count=instance_count,
            is_active=is_active,
            owner_user_id=owner_user_id,
            tenant_id=tenant_id,
            last_seen_at=last_seen_at,
            name=name,
            owner_display_name=owner_display_name,
            owner_email=owner_email,
            project_id=project_id,
        )

        return agent_index

