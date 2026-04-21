from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.insert_edge_detail import InsertEdgeDetail
  from ..models.insert_fact_detail import InsertFactDetail





T = TypeVar("T", bound="KbInsertFactsOutputBody")



@_attrs_define
class KbInsertFactsOutputBody:
    """ 
        Attributes:
            created (int): Number of new nodes created
            details (list[InsertFactDetail] | None): Per-fact results
            edges (list[InsertEdgeDetail] | None): Created edges
            processed (int): Number of facts processed
            updated (int): Number of existing nodes updated
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    created: int
    details: list[InsertFactDetail] | None
    edges: list[InsertEdgeDetail] | None
    processed: int
    updated: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.insert_edge_detail import InsertEdgeDetail
        from ..models.insert_fact_detail import InsertFactDetail
        created = self.created

        details: list[dict[str, Any]] | None
        if isinstance(self.details, list):
            details = []
            for details_type_0_item_data in self.details:
                details_type_0_item = details_type_0_item_data.to_dict()
                details.append(details_type_0_item)


        else:
            details = self.details

        edges: list[dict[str, Any]] | None
        if isinstance(self.edges, list):
            edges = []
            for edges_type_0_item_data in self.edges:
                edges_type_0_item = edges_type_0_item_data.to_dict()
                edges.append(edges_type_0_item)


        else:
            edges = self.edges

        processed = self.processed

        updated = self.updated

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created": created,
            "details": details,
            "edges": edges,
            "processed": processed,
            "updated": updated,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.insert_edge_detail import InsertEdgeDetail
        from ..models.insert_fact_detail import InsertFactDetail
        d = dict(src_dict)
        created = d.pop("created")

        def _parse_details(data: object) -> list[InsertFactDetail] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                details_type_0 = []
                _details_type_0 = data
                for details_type_0_item_data in (_details_type_0):
                    details_type_0_item = InsertFactDetail.from_dict(details_type_0_item_data)



                    details_type_0.append(details_type_0_item)

                return details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[InsertFactDetail] | None, data)

        details = _parse_details(d.pop("details"))


        def _parse_edges(data: object) -> list[InsertEdgeDetail] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                edges_type_0 = []
                _edges_type_0 = data
                for edges_type_0_item_data in (_edges_type_0):
                    edges_type_0_item = InsertEdgeDetail.from_dict(edges_type_0_item_data)



                    edges_type_0.append(edges_type_0_item)

                return edges_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[InsertEdgeDetail] | None, data)

        edges = _parse_edges(d.pop("edges"))


        processed = d.pop("processed")

        updated = d.pop("updated")

        schema = d.pop("$schema", UNSET)

        kb_insert_facts_output_body = cls(
            created=created,
            details=details,
            edges=edges,
            processed=processed,
            updated=updated,
            schema=schema,
        )

        return kb_insert_facts_output_body

