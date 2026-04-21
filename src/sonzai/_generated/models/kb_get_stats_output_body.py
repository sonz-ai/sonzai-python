from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_get_stats_output_body_documents import KbGetStatsOutputBodyDocuments
  from ..models.kb_get_stats_output_body_nodes import KbGetStatsOutputBodyNodes





T = TypeVar("T", bound="KbGetStatsOutputBody")



@_attrs_define
class KbGetStatsOutputBody:
    """ 
        Attributes:
            documents (KbGetStatsOutputBodyDocuments): Document counts by status
            edges (int): Total edge count
            extraction_tokens (int): Total extraction tokens used
            nodes (KbGetStatsOutputBodyNodes): Node counts (total, active)
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    documents: KbGetStatsOutputBodyDocuments
    edges: int
    extraction_tokens: int
    nodes: KbGetStatsOutputBodyNodes
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_get_stats_output_body_documents import KbGetStatsOutputBodyDocuments
        from ..models.kb_get_stats_output_body_nodes import KbGetStatsOutputBodyNodes
        documents = self.documents.to_dict()

        edges = self.edges

        extraction_tokens = self.extraction_tokens

        nodes = self.nodes.to_dict()

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "documents": documents,
            "edges": edges,
            "extraction_tokens": extraction_tokens,
            "nodes": nodes,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_get_stats_output_body_documents import KbGetStatsOutputBodyDocuments
        from ..models.kb_get_stats_output_body_nodes import KbGetStatsOutputBodyNodes
        d = dict(src_dict)
        documents = KbGetStatsOutputBodyDocuments.from_dict(d.pop("documents"))




        edges = d.pop("edges")

        extraction_tokens = d.pop("extraction_tokens")

        nodes = KbGetStatsOutputBodyNodes.from_dict(d.pop("nodes"))




        schema = d.pop("$schema", UNSET)

        kb_get_stats_output_body = cls(
            documents=documents,
            edges=edges,
            extraction_tokens=extraction_tokens,
            nodes=nodes,
            schema=schema,
        )

        return kb_get_stats_output_body

