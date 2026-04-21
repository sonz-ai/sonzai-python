from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="WorkbenchStateInterest")



@_attrs_define
class WorkbenchStateInterest:
    """ 
        Attributes:
            category (str):
            confidence (float):
            topic (str):
     """

    category: str
    confidence: float
    topic: str





    def to_dict(self) -> dict[str, Any]:
        category = self.category

        confidence = self.confidence

        topic = self.topic


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "category": category,
            "confidence": confidence,
            "topic": topic,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        category = d.pop("category")

        confidence = d.pop("confidence")

        topic = d.pop("topic")

        workbench_state_interest = cls(
            category=category,
            confidence=confidence,
            topic=topic,
        )

        return workbench_state_interest

