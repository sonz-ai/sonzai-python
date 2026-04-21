from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="EvalRunEvent")



@_attrs_define
class EvalRunEvent:
    """ 
        Attributes:
            type_ (str): Event kind — final_status | turn_started | turn_completed | score | error | ...
            schema (str | Unset): A URL to the JSON Schema for this object.
            adaptation_result (Any | Unset): Adaptation-evaluation result payload (final_status only)
            error_reason (str | Unset): Error detail (final_status / error events)
            evaluation_result (Any | Unset): Quality-evaluation result payload (final_status only)
            status (str | Unset): Terminal status (completed | failed) on final_status events
     """

    type_: str
    schema: str | Unset = UNSET
    adaptation_result: Any | Unset = UNSET
    error_reason: str | Unset = UNSET
    evaluation_result: Any | Unset = UNSET
    status: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        schema = self.schema

        adaptation_result = self.adaptation_result

        error_reason = self.error_reason

        evaluation_result = self.evaluation_result

        status = self.status


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if adaptation_result is not UNSET:
            field_dict["adaptation_result"] = adaptation_result
        if error_reason is not UNSET:
            field_dict["error_reason"] = error_reason
        if evaluation_result is not UNSET:
            field_dict["evaluation_result"] = evaluation_result
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        schema = d.pop("$schema", UNSET)

        adaptation_result = d.pop("adaptation_result", UNSET)

        error_reason = d.pop("error_reason", UNSET)

        evaluation_result = d.pop("evaluation_result", UNSET)

        status = d.pop("status", UNSET)

        eval_run_event = cls(
            type_=type_,
            schema=schema,
            adaptation_result=adaptation_result,
            error_reason=error_reason,
            evaluation_result=evaluation_result,
            status=status,
        )

        return eval_run_event

