from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.kb_similarity_config_field_weights import KBSimilarityConfigFieldWeights





T = TypeVar("T", bound="KBSimilarityConfig")



@_attrs_define
class KBSimilarityConfig:
    """ 
        Attributes:
            enabled (bool):
            field_weights (KBSimilarityConfigFieldWeights):
            max_edges_per_node (int):
            threshold (float):
     """

    enabled: bool
    field_weights: KBSimilarityConfigFieldWeights
    max_edges_per_node: int
    threshold: float





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_similarity_config_field_weights import KBSimilarityConfigFieldWeights
        enabled = self.enabled

        field_weights = self.field_weights.to_dict()

        max_edges_per_node = self.max_edges_per_node

        threshold = self.threshold


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "enabled": enabled,
            "field_weights": field_weights,
            "max_edges_per_node": max_edges_per_node,
            "threshold": threshold,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_similarity_config_field_weights import KBSimilarityConfigFieldWeights
        d = dict(src_dict)
        enabled = d.pop("enabled")

        field_weights = KBSimilarityConfigFieldWeights.from_dict(d.pop("field_weights"))




        max_edges_per_node = d.pop("max_edges_per_node")

        threshold = d.pop("threshold")

        kb_similarity_config = cls(
            enabled=enabled,
            field_weights=field_weights,
            max_edges_per_node=max_edges_per_node,
            threshold=threshold,
        )

        return kb_similarity_config

