from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="EvalOnlyRequest")



@_attrs_define
class EvalOnlyRequest:
    """ 
        Attributes:
            source_run_id (str): UUID of the existing run whose transcript is being re-evaluated
            template_id (str): Quality-eval template UUID to apply
            schema (str | Unset): A URL to the JSON Schema for this object.
            adaptation_template_id (str | Unset): Optional adaptation-eval template UUID
            quality_only (bool | Unset): Skip adaptation evaluation
     """

    source_run_id: str
    template_id: str
    schema: str | Unset = UNSET
    adaptation_template_id: str | Unset = UNSET
    quality_only: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        source_run_id = self.source_run_id

        template_id = self.template_id

        schema = self.schema

        adaptation_template_id = self.adaptation_template_id

        quality_only = self.quality_only


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "source_run_id": source_run_id,
            "template_id": template_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if adaptation_template_id is not UNSET:
            field_dict["adaptation_template_id"] = adaptation_template_id
        if quality_only is not UNSET:
            field_dict["quality_only"] = quality_only

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_run_id = d.pop("source_run_id")

        template_id = d.pop("template_id")

        schema = d.pop("$schema", UNSET)

        adaptation_template_id = d.pop("adaptation_template_id", UNSET)

        quality_only = d.pop("quality_only", UNSET)

        eval_only_request = cls(
            source_run_id=source_run_id,
            template_id=template_id,
            schema=schema,
            adaptation_template_id=adaptation_template_id,
            quality_only=quality_only,
        )

        return eval_only_request

