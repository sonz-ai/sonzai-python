from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateProjectInputBody")



@_attrs_define
class CreateProjectInputBody:
    """ 
        Attributes:
            name (str): Project name
            schema (str | Unset): A URL to the JSON Schema for this object.
            environment (str | Unset): Environment (production / development / staging); defaults to production
     """

    name: str
    schema: str | Unset = UNSET
    environment: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        schema = self.schema

        environment = self.environment


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if environment is not UNSET:
            field_dict["environment"] = environment

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        environment = d.pop("environment", UNSET)

        create_project_input_body = cls(
            name=name,
            schema=schema,
            environment=environment,
        )

        return create_project_input_body

