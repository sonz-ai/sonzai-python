from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="UserPersona")



@_attrs_define
class UserPersona:
    """ 
        Attributes:
            description (str):
            name (str):
            style (str):
     """

    description: str
    name: str
    style: str





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        style = self.style


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "description": description,
            "name": name,
            "style": style,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        name = d.pop("name")

        style = d.pop("style")

        user_persona = cls(
            description=description,
            name=name,
            style=style,
        )

        return user_persona

