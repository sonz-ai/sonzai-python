from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="AgentDialogueOutputBody")



@_attrs_define
class AgentDialogueOutputBody:
    """ 
        Attributes:
            response (str): Agent dialogue response
            schema (str | Unset): A URL to the JSON Schema for this object.
            side_effects (Any | Unset): Side effects produced by the agent
     """

    response: str
    schema: str | Unset = UNSET
    side_effects: Any | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        response = self.response

        schema = self.schema

        side_effects = self.side_effects


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "response": response,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if side_effects is not UNSET:
            field_dict["side_effects"] = side_effects

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        response = d.pop("response")

        schema = d.pop("$schema", UNSET)

        side_effects = d.pop("side_effects", UNSET)

        agent_dialogue_output_body = cls(
            response=response,
            schema=schema,
            side_effects=side_effects,
        )

        return agent_dialogue_output_body

