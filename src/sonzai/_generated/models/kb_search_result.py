from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_node_history import KBNodeHistory
  from ..models.kb_related_node import KBRelatedNode
  from ..models.kb_search_result_properties import KBSearchResultProperties





T = TypeVar("T", bound="KBSearchResult")



@_attrs_define
class KBSearchResult:
    """ 
        Attributes:
            label (str):
            node_id (str):
            properties (KBSearchResultProperties):
            type_ (str):
            updated_at (str):
            version (int):
            history (list[KBNodeHistory] | None | Unset):
            related (list[KBRelatedNode] | None | Unset):
            score (float | Unset):
            source (str | Unset):
     """

    label: str
    node_id: str
    properties: KBSearchResultProperties
    type_: str
    updated_at: str
    version: int
    history: list[KBNodeHistory] | None | Unset = UNSET
    related: list[KBRelatedNode] | None | Unset = UNSET
    score: float | Unset = UNSET
    source: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_node_history import KBNodeHistory
        from ..models.kb_related_node import KBRelatedNode
        from ..models.kb_search_result_properties import KBSearchResultProperties
        label = self.label

        node_id = self.node_id

        properties = self.properties.to_dict()

        type_ = self.type_

        updated_at = self.updated_at

        version = self.version

        history: list[dict[str, Any]] | None | Unset
        if isinstance(self.history, Unset):
            history = UNSET
        elif isinstance(self.history, list):
            history = []
            for history_type_0_item_data in self.history:
                history_type_0_item = history_type_0_item_data.to_dict()
                history.append(history_type_0_item)


        else:
            history = self.history

        related: list[dict[str, Any]] | None | Unset
        if isinstance(self.related, Unset):
            related = UNSET
        elif isinstance(self.related, list):
            related = []
            for related_type_0_item_data in self.related:
                related_type_0_item = related_type_0_item_data.to_dict()
                related.append(related_type_0_item)


        else:
            related = self.related

        score = self.score

        source = self.source


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "label": label,
            "node_id": node_id,
            "properties": properties,
            "type": type_,
            "updated_at": updated_at,
            "version": version,
        })
        if history is not UNSET:
            field_dict["history"] = history
        if related is not UNSET:
            field_dict["related"] = related
        if score is not UNSET:
            field_dict["score"] = score
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_node_history import KBNodeHistory
        from ..models.kb_related_node import KBRelatedNode
        from ..models.kb_search_result_properties import KBSearchResultProperties
        d = dict(src_dict)
        label = d.pop("label")

        node_id = d.pop("node_id")

        properties = KBSearchResultProperties.from_dict(d.pop("properties"))




        type_ = d.pop("type")

        updated_at = d.pop("updated_at")

        version = d.pop("version")

        def _parse_history(data: object) -> list[KBNodeHistory] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                history_type_0 = []
                _history_type_0 = data
                for history_type_0_item_data in (_history_type_0):
                    history_type_0_item = KBNodeHistory.from_dict(history_type_0_item_data)



                    history_type_0.append(history_type_0_item)

                return history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBNodeHistory] | None | Unset, data)

        history = _parse_history(d.pop("history", UNSET))


        def _parse_related(data: object) -> list[KBRelatedNode] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                related_type_0 = []
                _related_type_0 = data
                for related_type_0_item_data in (_related_type_0):
                    related_type_0_item = KBRelatedNode.from_dict(related_type_0_item_data)



                    related_type_0.append(related_type_0_item)

                return related_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBRelatedNode] | None | Unset, data)

        related = _parse_related(d.pop("related", UNSET))


        score = d.pop("score", UNSET)

        source = d.pop("source", UNSET)

        kb_search_result = cls(
            label=label,
            node_id=node_id,
            properties=properties,
            type_=type_,
            updated_at=updated_at,
            version=version,
            history=history,
            related=related,
            score=score,
            source=source,
        )

        return kb_search_result

