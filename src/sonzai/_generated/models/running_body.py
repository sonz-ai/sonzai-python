from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="RunningBody")



@_attrs_define
class RunningBody:
    """ 
        Attributes:
            run_id (str): Eval run UUID — stream progress via GET /eval-runs/{runId}/events
            status (str): Initial run status (always "running")
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    run_id: str
    status: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        run_id = self.run_id

        status = self.status

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "run_id": run_id,
            "status": status,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_id = d.pop("run_id")

        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        running_body = cls(
            run_id=run_id,
            status=status,
            schema=schema,
        )

        return running_body

