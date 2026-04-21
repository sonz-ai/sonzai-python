from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.support_ticket import SupportTicket
  from ..models.support_ticket_history import SupportTicketHistory





T = TypeVar("T", bound="TicketDetailResponse")



@_attrs_define
class TicketDetailResponse:
    """ 
        Attributes:
            ticket (SupportTicket):
            schema (str | Unset): A URL to the JSON Schema for this object.
            history (list[SupportTicketHistory] | None | Unset):
     """

    ticket: SupportTicket
    schema: str | Unset = UNSET
    history: list[SupportTicketHistory] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.support_ticket import SupportTicket
        from ..models.support_ticket_history import SupportTicketHistory
        ticket = self.ticket.to_dict()

        schema = self.schema

        history: list[dict[str, Any]] | None | Unset
        if isinstance(self.history, Unset):
            history = UNSET
        elif isinstance(self.history, list):
            history = []
            for history_type_0_item_data in self.history:
                history_type_0_item = history_type_0_item_data.to_dict()
                history.append(history_type_0_item)


        else:
            history = self.history


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "ticket": ticket,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if history is not UNSET:
            field_dict["history"] = history

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.support_ticket import SupportTicket
        from ..models.support_ticket_history import SupportTicketHistory
        d = dict(src_dict)
        ticket = SupportTicket.from_dict(d.pop("ticket"))




        schema = d.pop("$schema", UNSET)

        def _parse_history(data: object) -> list[SupportTicketHistory] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                history_type_0 = []
                _history_type_0 = data
                for history_type_0_item_data in (_history_type_0):
                    history_type_0_item = SupportTicketHistory.from_dict(history_type_0_item_data)



                    history_type_0.append(history_type_0_item)

                return history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SupportTicketHistory] | None | Unset, data)

        history = _parse_history(d.pop("history", UNSET))


        ticket_detail_response = cls(
            ticket=ticket,
            schema=schema,
            history=history,
        )

        return ticket_detail_response

