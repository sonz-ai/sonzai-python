from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.agent_instance import AgentInstance





T = TypeVar("T", bound="ResetInstanceOutputBody")



@_attrs_define
class ResetInstanceOutputBody:
    """ 
        Attributes:
            facts_deleted (int): Number of facts deleted
            instance (AgentInstance):
            nodes_deleted (int): Number of nodes deleted
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    facts_deleted: int
    instance: AgentInstance
    nodes_deleted: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_instance import AgentInstance
        facts_deleted = self.facts_deleted

        instance = self.instance.to_dict()

        nodes_deleted = self.nodes_deleted

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "facts_deleted": facts_deleted,
            "instance": instance,
            "nodes_deleted": nodes_deleted,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance import AgentInstance
        d = dict(src_dict)
        facts_deleted = d.pop("facts_deleted")

        instance = AgentInstance.from_dict(d.pop("instance"))




        nodes_deleted = d.pop("nodes_deleted")

        schema = d.pop("$schema", UNSET)

        reset_instance_output_body = cls(
            facts_deleted=facts_deleted,
            instance=instance,
            nodes_deleted=nodes_deleted,
            schema=schema,
        )

        return reset_instance_output_body

