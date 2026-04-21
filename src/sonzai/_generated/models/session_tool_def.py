from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.session_tool_def_parameters import SessionToolDefParameters





T = TypeVar("T", bound="SessionToolDef")



@_attrs_define
class SessionToolDef:
    """ 
        Attributes:
            name (str): Tool name (must not start with 'sonzai_')
            description (str | Unset): Human-readable tool description
            parameters (SessionToolDefParameters | Unset): OpenAI-compatible JSON Schema for tool parameters
     """

    name: str
    description: str | Unset = UNSET
    parameters: SessionToolDefParameters | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.session_tool_def_parameters import SessionToolDefParameters
        name = self.name

        description = self.description

        parameters: dict[str, Any] | Unset = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.session_tool_def_parameters import SessionToolDefParameters
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: SessionToolDefParameters | Unset
        if isinstance(_parameters,  Unset):
            parameters = UNSET
        else:
            parameters = SessionToolDefParameters.from_dict(_parameters)




        session_tool_def = cls(
            name=name,
            description=description,
            parameters=parameters,
        )

        return session_tool_def

