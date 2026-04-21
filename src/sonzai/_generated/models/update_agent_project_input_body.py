from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpdateAgentProjectInputBody")



@_attrs_define
class UpdateAgentProjectInputBody:
    """ 
        Attributes:
            project_id (None | str): Project UUID to assign; null/omitted to detach
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    project_id: None | str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        project_id: None | str
        project_id = self.project_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "project_id": project_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_project_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        project_id = _parse_project_id(d.pop("project_id"))


        schema = d.pop("$schema", UNSET)

        update_agent_project_input_body = cls(
            project_id=project_id,
            schema=schema,
        )

        return update_agent_project_input_body

