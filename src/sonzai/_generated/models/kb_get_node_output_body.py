from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_edge import KBEdge
  from ..models.kb_node import KBNode
  from ..models.kb_node_history import KBNodeHistory





T = TypeVar("T", bound="KbGetNodeOutputBody")



@_attrs_define
class KbGetNodeOutputBody:
    """ 
        Attributes:
            history (list[KBNodeHistory] | None): Version history (when requested)
            incoming (list[KBEdge] | None): Incoming edges
            node (KBNode):
            outgoing (list[KBEdge] | None): Outgoing edges
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    history: list[KBNodeHistory] | None
    incoming: list[KBEdge] | None
    node: KBNode
    outgoing: list[KBEdge] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_edge import KBEdge
        from ..models.kb_node import KBNode
        from ..models.kb_node_history import KBNodeHistory
        history: list[dict[str, Any]] | None
        if isinstance(self.history, list):
            history = []
            for history_type_0_item_data in self.history:
                history_type_0_item = history_type_0_item_data.to_dict()
                history.append(history_type_0_item)


        else:
            history = self.history

        incoming: list[dict[str, Any]] | None
        if isinstance(self.incoming, list):
            incoming = []
            for incoming_type_0_item_data in self.incoming:
                incoming_type_0_item = incoming_type_0_item_data.to_dict()
                incoming.append(incoming_type_0_item)


        else:
            incoming = self.incoming

        node = self.node.to_dict()

        outgoing: list[dict[str, Any]] | None
        if isinstance(self.outgoing, list):
            outgoing = []
            for outgoing_type_0_item_data in self.outgoing:
                outgoing_type_0_item = outgoing_type_0_item_data.to_dict()
                outgoing.append(outgoing_type_0_item)


        else:
            outgoing = self.outgoing

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "history": history,
            "incoming": incoming,
            "node": node,
            "outgoing": outgoing,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_edge import KBEdge
        from ..models.kb_node import KBNode
        from ..models.kb_node_history import KBNodeHistory
        d = dict(src_dict)
        def _parse_history(data: object) -> list[KBNodeHistory] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                history_type_0 = []
                _history_type_0 = data
                for history_type_0_item_data in (_history_type_0):
                    history_type_0_item = KBNodeHistory.from_dict(history_type_0_item_data)



                    history_type_0.append(history_type_0_item)

                return history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBNodeHistory] | None, data)

        history = _parse_history(d.pop("history"))


        def _parse_incoming(data: object) -> list[KBEdge] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                incoming_type_0 = []
                _incoming_type_0 = data
                for incoming_type_0_item_data in (_incoming_type_0):
                    incoming_type_0_item = KBEdge.from_dict(incoming_type_0_item_data)



                    incoming_type_0.append(incoming_type_0_item)

                return incoming_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBEdge] | None, data)

        incoming = _parse_incoming(d.pop("incoming"))


        node = KBNode.from_dict(d.pop("node"))




        def _parse_outgoing(data: object) -> list[KBEdge] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                outgoing_type_0 = []
                _outgoing_type_0 = data
                for outgoing_type_0_item_data in (_outgoing_type_0):
                    outgoing_type_0_item = KBEdge.from_dict(outgoing_type_0_item_data)



                    outgoing_type_0.append(outgoing_type_0_item)

                return outgoing_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBEdge] | None, data)

        outgoing = _parse_outgoing(d.pop("outgoing"))


        schema = d.pop("$schema", UNSET)

        kb_get_node_output_body = cls(
            history=history,
            incoming=incoming,
            node=node,
            outgoing=outgoing,
            schema=schema,
        )

        return kb_get_node_output_body

