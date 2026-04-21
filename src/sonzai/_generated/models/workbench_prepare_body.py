from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="WorkbenchPrepareBody")



@_attrs_define
class WorkbenchPrepareBody:
    """ 
        Attributes:
            agent_id (str):
            ready (bool):
            warm (bool):
            schema (str | Unset): A URL to the JSON Schema for this object.
            run_id (str | Unset):
     """

    agent_id: str
    ready: bool
    warm: bool
    schema: str | Unset = UNSET
    run_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        ready = self.ready

        warm = self.warm

        schema = self.schema

        run_id = self.run_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "ready": ready,
            "warm": warm,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if run_id is not UNSET:
            field_dict["run_id"] = run_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        ready = d.pop("ready")

        warm = d.pop("warm")

        schema = d.pop("$schema", UNSET)

        run_id = d.pop("run_id", UNSET)

        workbench_prepare_body = cls(
            agent_id=agent_id,
            ready=ready,
            warm=warm,
            schema=schema,
            run_id=run_id,
        )

        return workbench_prepare_body

