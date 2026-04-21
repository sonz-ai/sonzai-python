from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="WorkbenchStateFact")



@_attrs_define
class WorkbenchStateFact:
    """ 
        Attributes:
            fact_type (str):
            importance (float):
            text (str):
            entities (list[str] | None | Unset):
            sentiment (str | Unset):
            topic_tags (list[str] | None | Unset):
     """

    fact_type: str
    importance: float
    text: str
    entities: list[str] | None | Unset = UNSET
    sentiment: str | Unset = UNSET
    topic_tags: list[str] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        fact_type = self.fact_type

        importance = self.importance

        text = self.text

        entities: list[str] | None | Unset
        if isinstance(self.entities, Unset):
            entities = UNSET
        elif isinstance(self.entities, list):
            entities = self.entities


        else:
            entities = self.entities

        sentiment = self.sentiment

        topic_tags: list[str] | None | Unset
        if isinstance(self.topic_tags, Unset):
            topic_tags = UNSET
        elif isinstance(self.topic_tags, list):
            topic_tags = self.topic_tags


        else:
            topic_tags = self.topic_tags


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "fact_type": fact_type,
            "importance": importance,
            "text": text,
        })
        if entities is not UNSET:
            field_dict["entities"] = entities
        if sentiment is not UNSET:
            field_dict["sentiment"] = sentiment
        if topic_tags is not UNSET:
            field_dict["topic_tags"] = topic_tags

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fact_type = d.pop("fact_type")

        importance = d.pop("importance")

        text = d.pop("text")

        def _parse_entities(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                entities_type_0 = cast(list[str], data)

                return entities_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        entities = _parse_entities(d.pop("entities", UNSET))


        sentiment = d.pop("sentiment", UNSET)

        def _parse_topic_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                topic_tags_type_0 = cast(list[str], data)

                return topic_tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        topic_tags = _parse_topic_tags(d.pop("topic_tags", UNSET))


        workbench_state_fact = cls(
            fact_type=fact_type,
            importance=importance,
            text=text,
            entities=entities,
            sentiment=sentiment,
            topic_tags=topic_tags,
        )

        return workbench_state_fact

