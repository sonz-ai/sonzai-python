from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateProjectInputBody")



@_attrs_define
class UpdateProjectInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            environment (str | Unset): Environment
            game_name (str | Unset): Display name shown in the game
            name (str | Unset): New project name
     """

    schema: str | Unset = UNSET
    environment: str | Unset = UNSET
    game_name: str | Unset = UNSET
    name: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        environment = self.environment

        game_name = self.game_name

        name = self.name


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if environment is not UNSET:
            field_dict["environment"] = environment
        if game_name is not UNSET:
            field_dict["game_name"] = game_name
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        environment = d.pop("environment", UNSET)

        game_name = d.pop("game_name", UNSET)

        name = d.pop("name", UNSET)

        update_project_input_body = cls(
            schema=schema,
            environment=environment,
            game_name=game_name,
            name=name,
        )

        return update_project_input_body

