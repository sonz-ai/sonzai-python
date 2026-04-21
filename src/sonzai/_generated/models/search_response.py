from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.search_result import SearchResult





T = TypeVar("T", bound="SearchResponse")



@_attrs_define
class SearchResponse:
    """ 
        Attributes:
            results (list[SearchResult] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    results: list[SearchResult] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.search_result import SearchResult
        results: list[dict[str, Any]] | None
        if isinstance(self.results, list):
            results = []
            for results_type_0_item_data in self.results:
                results_type_0_item = results_type_0_item_data.to_dict()
                results.append(results_type_0_item)


        else:
            results = self.results

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "results": results,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_result import SearchResult
        d = dict(src_dict)
        def _parse_results(data: object) -> list[SearchResult] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                results_type_0 = []
                _results_type_0 = data
                for results_type_0_item_data in (_results_type_0):
                    results_type_0_item = SearchResult.from_dict(results_type_0_item_data)



                    results_type_0.append(results_type_0_item)

                return results_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SearchResult] | None, data)

        results = _parse_results(d.pop("results"))


        schema = d.pop("$schema", UNSET)

        search_response = cls(
            results=results,
            schema=schema,
        )

        return search_response

