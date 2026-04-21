from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.trigger_consolidation_input_body_period import TriggerConsolidationInputBodyPeriod
from ..types import UNSET, Unset






T = TypeVar("T", bound="TriggerConsolidationInputBody")



@_attrs_define
class TriggerConsolidationInputBody:
    """ 
        Attributes:
            period (TriggerConsolidationInputBodyPeriod): Consolidation period: 'daily' or 'weekly'
            user_id (str): Optional user ID to scope consolidation to a specific user
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    period: TriggerConsolidationInputBodyPeriod
    user_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        period = self.period.value

        user_id = self.user_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "period": period,
            "user_id": user_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = TriggerConsolidationInputBodyPeriod(d.pop("period"))




        user_id = d.pop("user_id")

        schema = d.pop("$schema", UNSET)

        trigger_consolidation_input_body = cls(
            period=period,
            user_id=user_id,
            schema=schema,
        )

        return trigger_consolidation_input_body

