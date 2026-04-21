from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.agent_index import AgentIndex





T = TypeVar("T", bound="PaginatedAgentsResponse")



@_attrs_define
class PaginatedAgentsResponse:
    """ 
        Attributes:
            has_more (bool):
            items (list[AgentIndex] | None):
            total_count (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
            next_cursor (str | Unset):
     """

    has_more: bool
    items: list[AgentIndex] | None
    total_count: int
    schema: str | Unset = UNSET
    next_cursor: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_index import AgentIndex
        has_more = self.has_more

        items: list[dict[str, Any]] | None
        if isinstance(self.items, list):
            items = []
            for items_type_0_item_data in self.items:
                items_type_0_item = items_type_0_item_data.to_dict()
                items.append(items_type_0_item)


        else:
            items = self.items

        total_count = self.total_count

        schema = self.schema

        next_cursor = self.next_cursor


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "has_more": has_more,
            "items": items,
            "total_count": total_count,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_index import AgentIndex
        d = dict(src_dict)
        has_more = d.pop("has_more")

        def _parse_items(data: object) -> list[AgentIndex] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                items_type_0 = []
                _items_type_0 = data
                for items_type_0_item_data in (_items_type_0):
                    items_type_0_item = AgentIndex.from_dict(items_type_0_item_data)



                    items_type_0.append(items_type_0_item)

                return items_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AgentIndex] | None, data)

        items = _parse_items(d.pop("items"))


        total_count = d.pop("total_count")

        schema = d.pop("$schema", UNSET)

        next_cursor = d.pop("next_cursor", UNSET)

        paginated_agents_response = cls(
            has_more=has_more,
            items=items,
            total_count=total_count,
            schema=schema,
            next_cursor=next_cursor,
        )

        return paginated_agents_response

