from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CreateAgentBodyCapabilitiesStruct")



@_attrs_define
class CreateAgentBodyCapabilitiesStruct:
    """ 
        Attributes:
            image_generation (bool):
            inventory (bool):
     """

    image_generation: bool
    inventory: bool





    def to_dict(self) -> dict[str, Any]:
        image_generation = self.image_generation

        inventory = self.inventory


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "image_generation": image_generation,
            "inventory": inventory,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image_generation = d.pop("image_generation")

        inventory = d.pop("inventory")

        create_agent_body_capabilities_struct = cls(
            image_generation=image_generation,
            inventory=inventory,
        )

        return create_agent_body_capabilities_struct

