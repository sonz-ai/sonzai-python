from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="BatchGetPersonalitiesInputBody")



@_attrs_define
class BatchGetPersonalitiesInputBody:
    """ 
        Attributes:
            agent_ids (list[str] | None): List of agent IDs (max 50)
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    agent_ids: list[str] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_ids: list[str] | None
        if isinstance(self.agent_ids, list):
            agent_ids = self.agent_ids


        else:
            agent_ids = self.agent_ids

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_ids": agent_ids,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_agent_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                agent_ids_type_0 = cast(list[str], data)

                return agent_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        agent_ids = _parse_agent_ids(d.pop("agent_ids"))


        schema = d.pop("$schema", UNSET)

        batch_get_personalities_input_body = cls(
            agent_ids=agent_ids,
            schema=schema,
        )

        return batch_get_personalities_input_body

