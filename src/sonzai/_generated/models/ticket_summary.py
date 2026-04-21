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






T = TypeVar("T", bound="TicketSummary")



@_attrs_define
class TicketSummary:
    """ 
        Attributes:
            comment_count (int):
            created_at (datetime.datetime):
            created_by_email (str):
            priority (str):
            status (str):
            ticket_id (str):
            title (str):
            type_ (str):
            updated_at (datetime.datetime):
            assigned_to_email (str | Unset):
     """

    comment_count: int
    created_at: datetime.datetime
    created_by_email: str
    priority: str
    status: str
    ticket_id: str
    title: str
    type_: str
    updated_at: datetime.datetime
    assigned_to_email: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        comment_count = self.comment_count

        created_at = self.created_at.isoformat()

        created_by_email = self.created_by_email

        priority = self.priority

        status = self.status

        ticket_id = self.ticket_id

        title = self.title

        type_ = self.type_

        updated_at = self.updated_at.isoformat()

        assigned_to_email = self.assigned_to_email


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "comment_count": comment_count,
            "created_at": created_at,
            "created_by_email": created_by_email,
            "priority": priority,
            "status": status,
            "ticket_id": ticket_id,
            "title": title,
            "type": type_,
            "updated_at": updated_at,
        })
        if assigned_to_email is not UNSET:
            field_dict["assigned_to_email"] = assigned_to_email

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        comment_count = d.pop("comment_count")

        created_at = isoparse(d.pop("created_at"))




        created_by_email = d.pop("created_by_email")

        priority = d.pop("priority")

        status = d.pop("status")

        ticket_id = d.pop("ticket_id")

        title = d.pop("title")

        type_ = d.pop("type")

        updated_at = isoparse(d.pop("updated_at"))




        assigned_to_email = d.pop("assigned_to_email", UNSET)

        ticket_summary = cls(
            comment_count=comment_count,
            created_at=created_at,
            created_by_email=created_by_email,
            priority=priority,
            status=status,
            ticket_id=ticket_id,
            title=title,
            type_=type_,
            updated_at=updated_at,
            assigned_to_email=assigned_to_email,
        )

        return ticket_summary

