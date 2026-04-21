from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.process_side_effects_summary import ProcessSideEffectsSummary





T = TypeVar("T", bound="ProcessResponse")



@_attrs_define
class ProcessResponse:
    """ 
        Attributes:
            facts_extracted (int):
            side_effects (ProcessSideEffectsSummary):
            success (bool):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    facts_extracted: int
    side_effects: ProcessSideEffectsSummary
    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.process_side_effects_summary import ProcessSideEffectsSummary
        facts_extracted = self.facts_extracted

        side_effects = self.side_effects.to_dict()

        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "facts_extracted": facts_extracted,
            "side_effects": side_effects,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_side_effects_summary import ProcessSideEffectsSummary
        d = dict(src_dict)
        facts_extracted = d.pop("facts_extracted")

        side_effects = ProcessSideEffectsSummary.from_dict(d.pop("side_effects"))




        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        process_response = cls(
            facts_extracted=facts_extracted,
            side_effects=side_effects,
            success=success,
            schema=schema,
        )

        return process_response

