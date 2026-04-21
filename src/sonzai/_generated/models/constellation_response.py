from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.edge import Edge
  from ..models.insight import Insight
  from ..models.node import Node





T = TypeVar("T", bound="ConstellationResponse")



@_attrs_define
class ConstellationResponse:
    """ 
        Attributes:
            edges (list[Edge] | None):
            insights (list[Insight] | None):
            nodes (list[Node] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    edges: list[Edge] | None
    insights: list[Insight] | None
    nodes: list[Node] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.edge import Edge
        from ..models.insight import Insight
        from ..models.node import Node
        edges: list[dict[str, Any]] | None
        if isinstance(self.edges, list):
            edges = []
            for edges_type_0_item_data in self.edges:
                edges_type_0_item = edges_type_0_item_data.to_dict()
                edges.append(edges_type_0_item)


        else:
            edges = self.edges

        insights: list[dict[str, Any]] | None
        if isinstance(self.insights, list):
            insights = []
            for insights_type_0_item_data in self.insights:
                insights_type_0_item = insights_type_0_item_data.to_dict()
                insights.append(insights_type_0_item)


        else:
            insights = self.insights

        nodes: list[dict[str, Any]] | None
        if isinstance(self.nodes, list):
            nodes = []
            for nodes_type_0_item_data in self.nodes:
                nodes_type_0_item = nodes_type_0_item_data.to_dict()
                nodes.append(nodes_type_0_item)


        else:
            nodes = self.nodes

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "edges": edges,
            "insights": insights,
            "nodes": nodes,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.edge import Edge
        from ..models.insight import Insight
        from ..models.node import Node
        d = dict(src_dict)
        def _parse_edges(data: object) -> list[Edge] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                edges_type_0 = []
                _edges_type_0 = data
                for edges_type_0_item_data in (_edges_type_0):
                    edges_type_0_item = Edge.from_dict(edges_type_0_item_data)



                    edges_type_0.append(edges_type_0_item)

                return edges_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Edge] | None, data)

        edges = _parse_edges(d.pop("edges"))


        def _parse_insights(data: object) -> list[Insight] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                insights_type_0 = []
                _insights_type_0 = data
                for insights_type_0_item_data in (_insights_type_0):
                    insights_type_0_item = Insight.from_dict(insights_type_0_item_data)



                    insights_type_0.append(insights_type_0_item)

                return insights_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Insight] | None, data)

        insights = _parse_insights(d.pop("insights"))


        def _parse_nodes(data: object) -> list[Node] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                nodes_type_0 = []
                _nodes_type_0 = data
                for nodes_type_0_item_data in (_nodes_type_0):
                    nodes_type_0_item = Node.from_dict(nodes_type_0_item_data)



                    nodes_type_0.append(nodes_type_0_item)

                return nodes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Node] | None, data)

        nodes = _parse_nodes(d.pop("nodes"))


        schema = d.pop("$schema", UNSET)

        constellation_response = cls(
            edges=edges,
            insights=insights,
            nodes=nodes,
            schema=schema,
        )

        return constellation_response

