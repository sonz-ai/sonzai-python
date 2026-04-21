from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="WorkbenchSimulateUserBody")



@_attrs_define
class WorkbenchSimulateUserBody:
    """ 
        Attributes:
            end_session (bool):
            message (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    end_session: bool
    message: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        end_session = self.end_session

        message = self.message

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "end_session": end_session,
            "message": message,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        end_session = d.pop("end_session")

        message = d.pop("message")

        schema = d.pop("$schema", UNSET)

        workbench_simulate_user_body = cls(
            end_session=end_session,
            message=message,
            schema=schema,
        )

        return workbench_simulate_user_body

