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






T = TypeVar("T", bound="Webhook")



@_attrs_define
class Webhook:
    """ 
        Attributes:
            created_at (datetime.datetime):
            event_type (str):
            is_active (bool):
            project_id (str):
            updated_at (datetime.datetime):
            webhook_url (str):
            auth_header (str | Unset):
     """

    created_at: datetime.datetime
    event_type: str
    is_active: bool
    project_id: str
    updated_at: datetime.datetime
    webhook_url: str
    auth_header: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        event_type = self.event_type

        is_active = self.is_active

        project_id = self.project_id

        updated_at = self.updated_at.isoformat()

        webhook_url = self.webhook_url

        auth_header = self.auth_header


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "event_type": event_type,
            "is_active": is_active,
            "project_id": project_id,
            "updated_at": updated_at,
            "webhook_url": webhook_url,
        })
        if auth_header is not UNSET:
            field_dict["auth_header"] = auth_header

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))




        event_type = d.pop("event_type")

        is_active = d.pop("is_active")

        project_id = d.pop("project_id")

        updated_at = isoparse(d.pop("updated_at"))




        webhook_url = d.pop("webhook_url")

        auth_header = d.pop("auth_header", UNSET)

        webhook = cls(
            created_at=created_at,
            event_type=event_type,
            is_active=is_active,
            project_id=project_id,
            updated_at=updated_at,
            webhook_url=webhook_url,
            auth_header=auth_header,
        )

        return webhook

