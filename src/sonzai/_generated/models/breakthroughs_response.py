from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.breakthrough import Breakthrough





T = TypeVar("T", bound="BreakthroughsResponse")



@_attrs_define
class BreakthroughsResponse:
    """ 
        Attributes:
            breakthroughs (list[Breakthrough] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    breakthroughs: list[Breakthrough] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.breakthrough import Breakthrough
        breakthroughs: list[dict[str, Any]] | None
        if isinstance(self.breakthroughs, list):
            breakthroughs = []
            for breakthroughs_type_0_item_data in self.breakthroughs:
                breakthroughs_type_0_item = breakthroughs_type_0_item_data.to_dict()
                breakthroughs.append(breakthroughs_type_0_item)


        else:
            breakthroughs = self.breakthroughs

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "breakthroughs": breakthroughs,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.breakthrough import Breakthrough
        d = dict(src_dict)
        def _parse_breakthroughs(data: object) -> list[Breakthrough] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                breakthroughs_type_0 = []
                _breakthroughs_type_0 = data
                for breakthroughs_type_0_item_data in (_breakthroughs_type_0):
                    breakthroughs_type_0_item = Breakthrough.from_dict(breakthroughs_type_0_item_data)



                    breakthroughs_type_0.append(breakthroughs_type_0_item)

                return breakthroughs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Breakthrough] | None, data)

        breakthroughs = _parse_breakthroughs(d.pop("breakthroughs"))


        schema = d.pop("$schema", UNSET)

        breakthroughs_response = cls(
            breakthroughs=breakthroughs,
            schema=schema,
        )

        return breakthroughs_response

