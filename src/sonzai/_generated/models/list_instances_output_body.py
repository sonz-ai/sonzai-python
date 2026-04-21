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





T = TypeVar("T", bound="ListInstancesOutputBody")



@_attrs_define
class ListInstancesOutputBody:
    """ 
        Attributes:
            instances (list[AgentInstance] | None): List of agent instances
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    instances: list[AgentInstance] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_instance import AgentInstance
        instances: list[dict[str, Any]] | None
        if isinstance(self.instances, list):
            instances = []
            for instances_type_0_item_data in self.instances:
                instances_type_0_item = instances_type_0_item_data.to_dict()
                instances.append(instances_type_0_item)


        else:
            instances = self.instances

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "instances": instances,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance import AgentInstance
        d = dict(src_dict)
        def _parse_instances(data: object) -> list[AgentInstance] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                instances_type_0 = []
                _instances_type_0 = data
                for instances_type_0_item_data in (_instances_type_0):
                    instances_type_0_item = AgentInstance.from_dict(instances_type_0_item_data)



                    instances_type_0.append(instances_type_0_item)

                return instances_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AgentInstance] | None, data)

        instances = _parse_instances(d.pop("instances"))


        schema = d.pop("$schema", UNSET)

        list_instances_output_body = cls(
            instances=instances,
            schema=schema,
        )

        return list_instances_output_body

