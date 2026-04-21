from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_conversion_stats import KBConversionStats





T = TypeVar("T", bound="KbGetConversionStatsOutputBody")



@_attrs_define
class KbGetConversionStatsOutputBody:
    """ 
        Attributes:
            conversions (list[KBConversionStats] | None): Conversion statistics
            total (int): Total count
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    conversions: list[KBConversionStats] | None
    total: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_conversion_stats import KBConversionStats
        conversions: list[dict[str, Any]] | None
        if isinstance(self.conversions, list):
            conversions = []
            for conversions_type_0_item_data in self.conversions:
                conversions_type_0_item = conversions_type_0_item_data.to_dict()
                conversions.append(conversions_type_0_item)


        else:
            conversions = self.conversions

        total = self.total

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "conversions": conversions,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_conversion_stats import KBConversionStats
        d = dict(src_dict)
        def _parse_conversions(data: object) -> list[KBConversionStats] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                conversions_type_0 = []
                _conversions_type_0 = data
                for conversions_type_0_item_data in (_conversions_type_0):
                    conversions_type_0_item = KBConversionStats.from_dict(conversions_type_0_item_data)



                    conversions_type_0.append(conversions_type_0_item)

                return conversions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBConversionStats] | None, data)

        conversions = _parse_conversions(d.pop("conversions"))


        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        kb_get_conversion_stats_output_body = cls(
            conversions=conversions,
            total=total,
            schema=schema,
        )

        return kb_get_conversion_stats_output_body

