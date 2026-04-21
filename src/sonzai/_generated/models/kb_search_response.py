from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_search_result import KBSearchResult





T = TypeVar("T", bound="KBSearchResponse")



@_attrs_define
class KBSearchResponse:
    """ 
        Attributes:
            query (str):
            results (list[KBSearchResult] | None):
            total (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    query: str
    results: list[KBSearchResult] | None
    total: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_search_result import KBSearchResult
        query = self.query

        results: list[dict[str, Any]] | None
        if isinstance(self.results, list):
            results = []
            for results_type_0_item_data in self.results:
                results_type_0_item = results_type_0_item_data.to_dict()
                results.append(results_type_0_item)


        else:
            results = self.results

        total = self.total

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "query": query,
            "results": results,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_search_result import KBSearchResult
        d = dict(src_dict)
        query = d.pop("query")

        def _parse_results(data: object) -> list[KBSearchResult] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                results_type_0 = []
                _results_type_0 = data
                for results_type_0_item_data in (_results_type_0):
                    results_type_0_item = KBSearchResult.from_dict(results_type_0_item_data)



                    results_type_0.append(results_type_0_item)

                return results_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBSearchResult] | None, data)

        results = _parse_results(d.pop("results"))


        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        kb_search_response = cls(
            query=query,
            results=results,
            total=total,
            schema=schema,
        )

        return kb_search_response

