from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.memory_summary import MemorySummary





T = TypeVar("T", bound="SummariesResponse")



@_attrs_define
class SummariesResponse:
    """ 
        Attributes:
            summaries (list[MemorySummary] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    summaries: list[MemorySummary] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.memory_summary import MemorySummary
        summaries: list[dict[str, Any]] | None
        if isinstance(self.summaries, list):
            summaries = []
            for summaries_type_0_item_data in self.summaries:
                summaries_type_0_item = summaries_type_0_item_data.to_dict()
                summaries.append(summaries_type_0_item)


        else:
            summaries = self.summaries

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "summaries": summaries,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.memory_summary import MemorySummary
        d = dict(src_dict)
        def _parse_summaries(data: object) -> list[MemorySummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                summaries_type_0 = []
                _summaries_type_0 = data
                for summaries_type_0_item_data in (_summaries_type_0):
                    summaries_type_0_item = MemorySummary.from_dict(summaries_type_0_item_data)



                    summaries_type_0.append(summaries_type_0_item)

                return summaries_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[MemorySummary] | None, data)

        summaries = _parse_summaries(d.pop("summaries"))


        schema = d.pop("$schema", UNSET)

        summaries_response = cls(
            summaries=summaries,
            schema=schema,
        )

        return summaries_response

