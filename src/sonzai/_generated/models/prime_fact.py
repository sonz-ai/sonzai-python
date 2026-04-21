from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="PrimeFact")



@_attrs_define
class PrimeFact:
    """ 
        Attributes:
            atomic_text (str): The fact, e.g. 'User is vegetarian'
            confidence (float): 0..1
            fact_type (str): One of: preference, commitment, fact, experience, correction, milestone, habit, identity,
                emotion
            importance (float): 0..1
            created_at (datetime.datetime | Unset): When the source system first learned this fact. Defaults to import time
                when omitted.
            emotional_intensity (float | Unset): 0..1
            entities (list[str] | None | Unset):
            event_time (datetime.datetime | Unset): When the event the fact describes actually happened.
            relationship_relevance (float | Unset): 0..1
            sentiment (str | Unset): positive | negative | neutral | mixed
            source_id (str | Unset): External id for traceability (e.g. 'legacy:fact-42').
            temporal_relevance (str | Unset): ongoing | past | future | recurring | one_time
            topic_tags (list[str] | None | Unset):
     """

    atomic_text: str
    confidence: float
    fact_type: str
    importance: float
    created_at: datetime.datetime | Unset = UNSET
    emotional_intensity: float | Unset = UNSET
    entities: list[str] | None | Unset = UNSET
    event_time: datetime.datetime | Unset = UNSET
    relationship_relevance: float | Unset = UNSET
    sentiment: str | Unset = UNSET
    source_id: str | Unset = UNSET
    temporal_relevance: str | Unset = UNSET
    topic_tags: list[str] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        atomic_text = self.atomic_text

        confidence = self.confidence

        fact_type = self.fact_type

        importance = self.importance

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        emotional_intensity = self.emotional_intensity

        entities: list[str] | None | Unset
        if isinstance(self.entities, Unset):
            entities = UNSET
        elif isinstance(self.entities, list):
            entities = self.entities


        else:
            entities = self.entities

        event_time: str | Unset = UNSET
        if not isinstance(self.event_time, Unset):
            event_time = self.event_time.isoformat()

        relationship_relevance = self.relationship_relevance

        sentiment = self.sentiment

        source_id = self.source_id

        temporal_relevance = self.temporal_relevance

        topic_tags: list[str] | None | Unset
        if isinstance(self.topic_tags, Unset):
            topic_tags = UNSET
        elif isinstance(self.topic_tags, list):
            topic_tags = self.topic_tags


        else:
            topic_tags = self.topic_tags


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "atomic_text": atomic_text,
            "confidence": confidence,
            "fact_type": fact_type,
            "importance": importance,
        })
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if emotional_intensity is not UNSET:
            field_dict["emotional_intensity"] = emotional_intensity
        if entities is not UNSET:
            field_dict["entities"] = entities
        if event_time is not UNSET:
            field_dict["event_time"] = event_time
        if relationship_relevance is not UNSET:
            field_dict["relationship_relevance"] = relationship_relevance
        if sentiment is not UNSET:
            field_dict["sentiment"] = sentiment
        if source_id is not UNSET:
            field_dict["source_id"] = source_id
        if temporal_relevance is not UNSET:
            field_dict["temporal_relevance"] = temporal_relevance
        if topic_tags is not UNSET:
            field_dict["topic_tags"] = topic_tags

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        atomic_text = d.pop("atomic_text")

        confidence = d.pop("confidence")

        fact_type = d.pop("fact_type")

        importance = d.pop("importance")

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)




        emotional_intensity = d.pop("emotional_intensity", UNSET)

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


        _event_time = d.pop("event_time", UNSET)
        event_time: datetime.datetime | Unset
        if isinstance(_event_time,  Unset):
            event_time = UNSET
        else:
            event_time = isoparse(_event_time)




        relationship_relevance = d.pop("relationship_relevance", UNSET)

        sentiment = d.pop("sentiment", UNSET)

        source_id = d.pop("source_id", UNSET)

        temporal_relevance = d.pop("temporal_relevance", UNSET)

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


        prime_fact = cls(
            atomic_text=atomic_text,
            confidence=confidence,
            fact_type=fact_type,
            importance=importance,
            created_at=created_at,
            emotional_intensity=emotional_intensity,
            entities=entities,
            event_time=event_time,
            relationship_relevance=relationship_relevance,
            sentiment=sentiment,
            source_id=source_id,
            temporal_relevance=temporal_relevance,
            topic_tags=topic_tags,
        )

        return prime_fact

