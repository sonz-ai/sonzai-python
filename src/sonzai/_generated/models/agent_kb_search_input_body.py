from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="AgentKBSearchInputBody")



@_attrs_define
class AgentKBSearchInputBody:
    """ 
        Attributes:
            query (str): Search query
            schema (str | Unset): A URL to the JSON Schema for this object.
            limit (int | Unset): Max results (default 10, max 50)
     """

    query: str
    schema: str | Unset = UNSET
    limit: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        query = self.query

        schema = self.schema

        limit = self.limit


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "query": query,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        query = d.pop("query")

        schema = d.pop("$schema", UNSET)

        limit = d.pop("limit", UNSET)

        agent_kb_search_input_body = cls(
            query=query,
            schema=schema,
            limit=limit,
        )

        return agent_kb_search_input_body

