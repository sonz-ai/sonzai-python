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






T = TypeVar("T", bound="Notification")



@_attrs_define
class Notification:
    """ 
        Attributes:
            created_at (datetime.datetime):
            event_type (str):
            notification_id (str):
            payload (Any):
            project_id (str):
            status (str):
            acknowledged_at (datetime.datetime | Unset):
            agent_id (str | Unset):
            expires_at (datetime.datetime | Unset):
            user_id (str | Unset):
     """

    created_at: datetime.datetime
    event_type: str
    notification_id: str
    payload: Any
    project_id: str
    status: str
    acknowledged_at: datetime.datetime | Unset = UNSET
    agent_id: str | Unset = UNSET
    expires_at: datetime.datetime | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        event_type = self.event_type

        notification_id = self.notification_id

        payload = self.payload

        project_id = self.project_id

        status = self.status

        acknowledged_at: str | Unset = UNSET
        if not isinstance(self.acknowledged_at, Unset):
            acknowledged_at = self.acknowledged_at.isoformat()

        agent_id = self.agent_id

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "event_type": event_type,
            "notification_id": notification_id,
            "payload": payload,
            "project_id": project_id,
            "status": status,
        })
        if acknowledged_at is not UNSET:
            field_dict["acknowledged_at"] = acknowledged_at
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))




        event_type = d.pop("event_type")

        notification_id = d.pop("notification_id")

        payload = d.pop("payload")

        project_id = d.pop("project_id")

        status = d.pop("status")

        _acknowledged_at = d.pop("acknowledged_at", UNSET)
        acknowledged_at: datetime.datetime | Unset
        if isinstance(_acknowledged_at,  Unset):
            acknowledged_at = UNSET
        else:
            acknowledged_at = isoparse(_acknowledged_at)




        agent_id = d.pop("agent_id", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at,  Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)




        user_id = d.pop("user_id", UNSET)

        notification = cls(
            created_at=created_at,
            event_type=event_type,
            notification_id=notification_id,
            payload=payload,
            project_id=project_id,
            status=status,
            acknowledged_at=acknowledged_at,
            agent_id=agent_id,
            expires_at=expires_at,
            user_id=user_id,
        )

        return notification

