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






T = TypeVar("T", bound="SupportTicketHistory")



@_attrs_define
class SupportTicketHistory:
    """ 
        Attributes:
            changed_by (str):
            changed_by_email (str):
            created_at (datetime.datetime):
            field_changed (str):
            history_id (str):
            ticket_id (str):
            new_value (str | Unset):
            old_value (str | Unset):
     """

    changed_by: str
    changed_by_email: str
    created_at: datetime.datetime
    field_changed: str
    history_id: str
    ticket_id: str
    new_value: str | Unset = UNSET
    old_value: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        changed_by = self.changed_by

        changed_by_email = self.changed_by_email

        created_at = self.created_at.isoformat()

        field_changed = self.field_changed

        history_id = self.history_id

        ticket_id = self.ticket_id

        new_value = self.new_value

        old_value = self.old_value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "changed_by": changed_by,
            "changed_by_email": changed_by_email,
            "created_at": created_at,
            "field_changed": field_changed,
            "history_id": history_id,
            "ticket_id": ticket_id,
        })
        if new_value is not UNSET:
            field_dict["new_value"] = new_value
        if old_value is not UNSET:
            field_dict["old_value"] = old_value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        changed_by = d.pop("changed_by")

        changed_by_email = d.pop("changed_by_email")

        created_at = isoparse(d.pop("created_at"))




        field_changed = d.pop("field_changed")

        history_id = d.pop("history_id")

        ticket_id = d.pop("ticket_id")

        new_value = d.pop("new_value", UNSET)

        old_value = d.pop("old_value", UNSET)

        support_ticket_history = cls(
            changed_by=changed_by,
            changed_by_email=changed_by_email,
            created_at=created_at,
            field_changed=field_changed,
            history_id=history_id,
            ticket_id=ticket_id,
            new_value=new_value,
            old_value=old_value,
        )

        return support_ticket_history

