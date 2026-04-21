from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.ticket_summary import TicketSummary





T = TypeVar("T", bound="TicketListResponse")



@_attrs_define
class TicketListResponse:
    """ 
        Attributes:
            has_more (bool):
            tickets (list[TicketSummary] | None):
            total (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    has_more: bool
    tickets: list[TicketSummary] | None
    total: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.ticket_summary import TicketSummary
        has_more = self.has_more

        tickets: list[dict[str, Any]] | None
        if isinstance(self.tickets, list):
            tickets = []
            for tickets_type_0_item_data in self.tickets:
                tickets_type_0_item = tickets_type_0_item_data.to_dict()
                tickets.append(tickets_type_0_item)


        else:
            tickets = self.tickets

        total = self.total

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "has_more": has_more,
            "tickets": tickets,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ticket_summary import TicketSummary
        d = dict(src_dict)
        has_more = d.pop("has_more")

        def _parse_tickets(data: object) -> list[TicketSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tickets_type_0 = []
                _tickets_type_0 = data
                for tickets_type_0_item_data in (_tickets_type_0):
                    tickets_type_0_item = TicketSummary.from_dict(tickets_type_0_item_data)



                    tickets_type_0.append(tickets_type_0_item)

                return tickets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[TicketSummary] | None, data)

        tickets = _parse_tickets(d.pop("tickets"))


        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        ticket_list_response = cls(
            has_more=has_more,
            tickets=tickets,
            total=total,
            schema=schema,
        )

        return ticket_list_response

