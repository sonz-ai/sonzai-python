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

if TYPE_CHECKING:
  from ..models.support_ticket_comment import SupportTicketComment





T = TypeVar("T", bound="SupportTicket")



@_attrs_define
class SupportTicket:
    """ 
        Attributes:
            created_at (datetime.datetime):
            created_by (str):
            created_by_email (str):
            description (str):
            priority (str):
            status (str):
            tenant_id (str):
            ticket_id (str):
            title (str):
            type_ (str):
            updated_at (datetime.datetime):
            schema (str | Unset): A URL to the JSON Schema for this object.
            assigned_to (str | Unset):
            assigned_to_email (str | Unset):
            comment_count (int | Unset):
            comments (list[SupportTicketComment] | None | Unset):
            resolved_at (datetime.datetime | Unset):
     """

    created_at: datetime.datetime
    created_by: str
    created_by_email: str
    description: str
    priority: str
    status: str
    tenant_id: str
    ticket_id: str
    title: str
    type_: str
    updated_at: datetime.datetime
    schema: str | Unset = UNSET
    assigned_to: str | Unset = UNSET
    assigned_to_email: str | Unset = UNSET
    comment_count: int | Unset = UNSET
    comments: list[SupportTicketComment] | None | Unset = UNSET
    resolved_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.support_ticket_comment import SupportTicketComment
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        created_by_email = self.created_by_email

        description = self.description

        priority = self.priority

        status = self.status

        tenant_id = self.tenant_id

        ticket_id = self.ticket_id

        title = self.title

        type_ = self.type_

        updated_at = self.updated_at.isoformat()

        schema = self.schema

        assigned_to = self.assigned_to

        assigned_to_email = self.assigned_to_email

        comment_count = self.comment_count

        comments: list[dict[str, Any]] | None | Unset
        if isinstance(self.comments, Unset):
            comments = UNSET
        elif isinstance(self.comments, list):
            comments = []
            for comments_type_0_item_data in self.comments:
                comments_type_0_item = comments_type_0_item_data.to_dict()
                comments.append(comments_type_0_item)


        else:
            comments = self.comments

        resolved_at: str | Unset = UNSET
        if not isinstance(self.resolved_at, Unset):
            resolved_at = self.resolved_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "created_by": created_by,
            "created_by_email": created_by_email,
            "description": description,
            "priority": priority,
            "status": status,
            "tenant_id": tenant_id,
            "ticket_id": ticket_id,
            "title": title,
            "type": type_,
            "updated_at": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if assigned_to is not UNSET:
            field_dict["assigned_to"] = assigned_to
        if assigned_to_email is not UNSET:
            field_dict["assigned_to_email"] = assigned_to_email
        if comment_count is not UNSET:
            field_dict["comment_count"] = comment_count
        if comments is not UNSET:
            field_dict["comments"] = comments
        if resolved_at is not UNSET:
            field_dict["resolved_at"] = resolved_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.support_ticket_comment import SupportTicketComment
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))




        created_by = d.pop("created_by")

        created_by_email = d.pop("created_by_email")

        description = d.pop("description")

        priority = d.pop("priority")

        status = d.pop("status")

        tenant_id = d.pop("tenant_id")

        ticket_id = d.pop("ticket_id")

        title = d.pop("title")

        type_ = d.pop("type")

        updated_at = isoparse(d.pop("updated_at"))




        schema = d.pop("$schema", UNSET)

        assigned_to = d.pop("assigned_to", UNSET)

        assigned_to_email = d.pop("assigned_to_email", UNSET)

        comment_count = d.pop("comment_count", UNSET)

        def _parse_comments(data: object) -> list[SupportTicketComment] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                comments_type_0 = []
                _comments_type_0 = data
                for comments_type_0_item_data in (_comments_type_0):
                    comments_type_0_item = SupportTicketComment.from_dict(comments_type_0_item_data)



                    comments_type_0.append(comments_type_0_item)

                return comments_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SupportTicketComment] | None | Unset, data)

        comments = _parse_comments(d.pop("comments", UNSET))


        _resolved_at = d.pop("resolved_at", UNSET)
        resolved_at: datetime.datetime | Unset
        if isinstance(_resolved_at,  Unset):
            resolved_at = UNSET
        else:
            resolved_at = isoparse(_resolved_at)




        support_ticket = cls(
            created_at=created_at,
            created_by=created_by,
            created_by_email=created_by_email,
            description=description,
            priority=priority,
            status=status,
            tenant_id=tenant_id,
            ticket_id=ticket_id,
            title=title,
            type_=type_,
            updated_at=updated_at,
            schema=schema,
            assigned_to=assigned_to,
            assigned_to_email=assigned_to_email,
            comment_count=comment_count,
            comments=comments,
            resolved_at=resolved_at,
        )

        return support_ticket

