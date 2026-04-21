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






T = TypeVar("T", bound="SupportTicketComment")



@_attrs_define
class SupportTicketComment:
    """ 
        Attributes:
            author_email (str):
            author_id (str):
            author_type (str):
            comment_id (str):
            content (str):
            created_at (datetime.datetime):
            is_internal (bool):
            ticket_id (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    author_email: str
    author_id: str
    author_type: str
    comment_id: str
    content: str
    created_at: datetime.datetime
    is_internal: bool
    ticket_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        author_email = self.author_email

        author_id = self.author_id

        author_type = self.author_type

        comment_id = self.comment_id

        content = self.content

        created_at = self.created_at.isoformat()

        is_internal = self.is_internal

        ticket_id = self.ticket_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "author_email": author_email,
            "author_id": author_id,
            "author_type": author_type,
            "comment_id": comment_id,
            "content": content,
            "created_at": created_at,
            "is_internal": is_internal,
            "ticket_id": ticket_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        author_email = d.pop("author_email")

        author_id = d.pop("author_id")

        author_type = d.pop("author_type")

        comment_id = d.pop("comment_id")

        content = d.pop("content")

        created_at = isoparse(d.pop("created_at"))




        is_internal = d.pop("is_internal")

        ticket_id = d.pop("ticket_id")

        schema = d.pop("$schema", UNSET)

        support_ticket_comment = cls(
            author_email=author_email,
            author_id=author_id,
            author_type=author_type,
            comment_id=comment_id,
            content=content,
            created_at=created_at,
            is_internal=is_internal,
            ticket_id=ticket_id,
            schema=schema,
        )

        return support_ticket_comment

