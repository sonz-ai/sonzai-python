from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.stored_fact import StoredFact





T = TypeVar("T", bound="ListFactsResponse")



@_attrs_define
class ListFactsResponse:
    """ 
        Attributes:
            facts (list[StoredFact] | None):
            total_count (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    facts: list[StoredFact] | None
    total_count: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.stored_fact import StoredFact
        facts: list[dict[str, Any]] | None
        if isinstance(self.facts, list):
            facts = []
            for facts_type_0_item_data in self.facts:
                facts_type_0_item = facts_type_0_item_data.to_dict()
                facts.append(facts_type_0_item)


        else:
            facts = self.facts

        total_count = self.total_count

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "facts": facts,
            "total_count": total_count,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.stored_fact import StoredFact
        d = dict(src_dict)
        def _parse_facts(data: object) -> list[StoredFact] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                facts_type_0 = []
                _facts_type_0 = data
                for facts_type_0_item_data in (_facts_type_0):
                    facts_type_0_item = StoredFact.from_dict(facts_type_0_item_data)



                    facts_type_0.append(facts_type_0_item)

                return facts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[StoredFact] | None, data)

        facts = _parse_facts(d.pop("facts"))


        total_count = d.pop("total_count")

        schema = d.pop("$schema", UNSET)

        list_facts_response = cls(
            facts=facts,
            total_count=total_count,
            schema=schema,
        )

        return list_facts_response

