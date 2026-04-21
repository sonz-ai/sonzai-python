from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.storefront_agent import StorefrontAgent





T = TypeVar("T", bound="StorefrontListAgentsOutputBody")



@_attrs_define
class StorefrontListAgentsOutputBody:
    """ 
        Attributes:
            agents (list[StorefrontAgent] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    agents: list[StorefrontAgent] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.storefront_agent import StorefrontAgent
        agents: list[dict[str, Any]] | None
        if isinstance(self.agents, list):
            agents = []
            for agents_type_0_item_data in self.agents:
                agents_type_0_item = agents_type_0_item_data.to_dict()
                agents.append(agents_type_0_item)


        else:
            agents = self.agents

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agents": agents,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storefront_agent import StorefrontAgent
        d = dict(src_dict)
        def _parse_agents(data: object) -> list[StorefrontAgent] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                agents_type_0 = []
                _agents_type_0 = data
                for agents_type_0_item_data in (_agents_type_0):
                    agents_type_0_item = StorefrontAgent.from_dict(agents_type_0_item_data)



                    agents_type_0.append(agents_type_0_item)

                return agents_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[StorefrontAgent] | None, data)

        agents = _parse_agents(d.pop("agents"))


        schema = d.pop("$schema", UNSET)

        storefront_list_agents_output_body = cls(
            agents=agents,
            schema=schema,
        )

        return storefront_list_agents_output_body

