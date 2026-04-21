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

if TYPE_CHECKING:
  from ..models.atomic_fact_metadata import AtomicFactMetadata





T = TypeVar("T", bound="AtomicFact")



@_attrs_define
class AtomicFact:
    """ 
        Attributes:
            agent_id (str):
            atomic_text (str):
            confidence (float):
            created_at (datetime.datetime):
            fact_id (str):
            fact_type (str):
            last_confirmed (datetime.datetime):
            last_retrieved_at (datetime.datetime):
            mention_count (int):
            node_id (str):
            retention_strength (float):
            updated_at (datetime.datetime):
            schema (str | Unset): A URL to the JSON Schema for this object.
            agent_framing (str | Unset):
            character_salience (float | Unset):
            cluster_id (str | Unset):
            emotional_intensity (float | Unset):
            entities (list[str] | None | Unset):
            episode_id (str | Unset):
            event_time (datetime.datetime | Unset):
            evidence_message_ids (list[str] | None | Unset):
            hit_count (int | Unset):
            importance (float | Unset):
            inferred_entities (list[str] | None | Unset):
            metadata (AtomicFactMetadata | Unset):
            miss_count (int | Unset):
            polarity_group_id (str | Unset):
            relationship_relevance (float | Unset):
            sentiment (str | Unset):
            session_id (str | Unset):
            source_id (str | Unset):
            source_type (str | Unset):
            supersedes_id (str | Unset):
            temporal_relevance (str | Unset):
            time_sensitive_at (datetime.datetime | Unset):
            topic_tags (list[str] | None | Unset):
            user_id (str | Unset):
     """

    agent_id: str
    atomic_text: str
    confidence: float
    created_at: datetime.datetime
    fact_id: str
    fact_type: str
    last_confirmed: datetime.datetime
    last_retrieved_at: datetime.datetime
    mention_count: int
    node_id: str
    retention_strength: float
    updated_at: datetime.datetime
    schema: str | Unset = UNSET
    agent_framing: str | Unset = UNSET
    character_salience: float | Unset = UNSET
    cluster_id: str | Unset = UNSET
    emotional_intensity: float | Unset = UNSET
    entities: list[str] | None | Unset = UNSET
    episode_id: str | Unset = UNSET
    event_time: datetime.datetime | Unset = UNSET
    evidence_message_ids: list[str] | None | Unset = UNSET
    hit_count: int | Unset = UNSET
    importance: float | Unset = UNSET
    inferred_entities: list[str] | None | Unset = UNSET
    metadata: AtomicFactMetadata | Unset = UNSET
    miss_count: int | Unset = UNSET
    polarity_group_id: str | Unset = UNSET
    relationship_relevance: float | Unset = UNSET
    sentiment: str | Unset = UNSET
    session_id: str | Unset = UNSET
    source_id: str | Unset = UNSET
    source_type: str | Unset = UNSET
    supersedes_id: str | Unset = UNSET
    temporal_relevance: str | Unset = UNSET
    time_sensitive_at: datetime.datetime | Unset = UNSET
    topic_tags: list[str] | None | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.atomic_fact_metadata import AtomicFactMetadata
        agent_id = self.agent_id

        atomic_text = self.atomic_text

        confidence = self.confidence

        created_at = self.created_at.isoformat()

        fact_id = self.fact_id

        fact_type = self.fact_type

        last_confirmed = self.last_confirmed.isoformat()

        last_retrieved_at = self.last_retrieved_at.isoformat()

        mention_count = self.mention_count

        node_id = self.node_id

        retention_strength = self.retention_strength

        updated_at = self.updated_at.isoformat()

        schema = self.schema

        agent_framing = self.agent_framing

        character_salience = self.character_salience

        cluster_id = self.cluster_id

        emotional_intensity = self.emotional_intensity

        entities: list[str] | None | Unset
        if isinstance(self.entities, Unset):
            entities = UNSET
        elif isinstance(self.entities, list):
            entities = self.entities


        else:
            entities = self.entities

        episode_id = self.episode_id

        event_time: str | Unset = UNSET
        if not isinstance(self.event_time, Unset):
            event_time = self.event_time.isoformat()

        evidence_message_ids: list[str] | None | Unset
        if isinstance(self.evidence_message_ids, Unset):
            evidence_message_ids = UNSET
        elif isinstance(self.evidence_message_ids, list):
            evidence_message_ids = self.evidence_message_ids


        else:
            evidence_message_ids = self.evidence_message_ids

        hit_count = self.hit_count

        importance = self.importance

        inferred_entities: list[str] | None | Unset
        if isinstance(self.inferred_entities, Unset):
            inferred_entities = UNSET
        elif isinstance(self.inferred_entities, list):
            inferred_entities = self.inferred_entities


        else:
            inferred_entities = self.inferred_entities

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        miss_count = self.miss_count

        polarity_group_id = self.polarity_group_id

        relationship_relevance = self.relationship_relevance

        sentiment = self.sentiment

        session_id = self.session_id

        source_id = self.source_id

        source_type = self.source_type

        supersedes_id = self.supersedes_id

        temporal_relevance = self.temporal_relevance

        time_sensitive_at: str | Unset = UNSET
        if not isinstance(self.time_sensitive_at, Unset):
            time_sensitive_at = self.time_sensitive_at.isoformat()

        topic_tags: list[str] | None | Unset
        if isinstance(self.topic_tags, Unset):
            topic_tags = UNSET
        elif isinstance(self.topic_tags, list):
            topic_tags = self.topic_tags


        else:
            topic_tags = self.topic_tags

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "atomic_text": atomic_text,
            "confidence": confidence,
            "created_at": created_at,
            "fact_id": fact_id,
            "fact_type": fact_type,
            "last_confirmed": last_confirmed,
            "last_retrieved_at": last_retrieved_at,
            "mention_count": mention_count,
            "node_id": node_id,
            "retention_strength": retention_strength,
            "updated_at": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if agent_framing is not UNSET:
            field_dict["agent_framing"] = agent_framing
        if character_salience is not UNSET:
            field_dict["character_salience"] = character_salience
        if cluster_id is not UNSET:
            field_dict["cluster_id"] = cluster_id
        if emotional_intensity is not UNSET:
            field_dict["emotional_intensity"] = emotional_intensity
        if entities is not UNSET:
            field_dict["entities"] = entities
        if episode_id is not UNSET:
            field_dict["episode_id"] = episode_id
        if event_time is not UNSET:
            field_dict["event_time"] = event_time
        if evidence_message_ids is not UNSET:
            field_dict["evidence_message_ids"] = evidence_message_ids
        if hit_count is not UNSET:
            field_dict["hit_count"] = hit_count
        if importance is not UNSET:
            field_dict["importance"] = importance
        if inferred_entities is not UNSET:
            field_dict["inferred_entities"] = inferred_entities
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if miss_count is not UNSET:
            field_dict["miss_count"] = miss_count
        if polarity_group_id is not UNSET:
            field_dict["polarity_group_id"] = polarity_group_id
        if relationship_relevance is not UNSET:
            field_dict["relationship_relevance"] = relationship_relevance
        if sentiment is not UNSET:
            field_dict["sentiment"] = sentiment
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if source_id is not UNSET:
            field_dict["source_id"] = source_id
        if source_type is not UNSET:
            field_dict["source_type"] = source_type
        if supersedes_id is not UNSET:
            field_dict["supersedes_id"] = supersedes_id
        if temporal_relevance is not UNSET:
            field_dict["temporal_relevance"] = temporal_relevance
        if time_sensitive_at is not UNSET:
            field_dict["time_sensitive_at"] = time_sensitive_at
        if topic_tags is not UNSET:
            field_dict["topic_tags"] = topic_tags
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.atomic_fact_metadata import AtomicFactMetadata
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        atomic_text = d.pop("atomic_text")

        confidence = d.pop("confidence")

        created_at = isoparse(d.pop("created_at"))




        fact_id = d.pop("fact_id")

        fact_type = d.pop("fact_type")

        last_confirmed = isoparse(d.pop("last_confirmed"))




        last_retrieved_at = isoparse(d.pop("last_retrieved_at"))




        mention_count = d.pop("mention_count")

        node_id = d.pop("node_id")

        retention_strength = d.pop("retention_strength")

        updated_at = isoparse(d.pop("updated_at"))




        schema = d.pop("$schema", UNSET)

        agent_framing = d.pop("agent_framing", UNSET)

        character_salience = d.pop("character_salience", UNSET)

        cluster_id = d.pop("cluster_id", UNSET)

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


        episode_id = d.pop("episode_id", UNSET)

        _event_time = d.pop("event_time", UNSET)
        event_time: datetime.datetime | Unset
        if isinstance(_event_time,  Unset):
            event_time = UNSET
        else:
            event_time = isoparse(_event_time)




        def _parse_evidence_message_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                evidence_message_ids_type_0 = cast(list[str], data)

                return evidence_message_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        evidence_message_ids = _parse_evidence_message_ids(d.pop("evidence_message_ids", UNSET))


        hit_count = d.pop("hit_count", UNSET)

        importance = d.pop("importance", UNSET)

        def _parse_inferred_entities(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                inferred_entities_type_0 = cast(list[str], data)

                return inferred_entities_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        inferred_entities = _parse_inferred_entities(d.pop("inferred_entities", UNSET))


        _metadata = d.pop("metadata", UNSET)
        metadata: AtomicFactMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = AtomicFactMetadata.from_dict(_metadata)




        miss_count = d.pop("miss_count", UNSET)

        polarity_group_id = d.pop("polarity_group_id", UNSET)

        relationship_relevance = d.pop("relationship_relevance", UNSET)

        sentiment = d.pop("sentiment", UNSET)

        session_id = d.pop("session_id", UNSET)

        source_id = d.pop("source_id", UNSET)

        source_type = d.pop("source_type", UNSET)

        supersedes_id = d.pop("supersedes_id", UNSET)

        temporal_relevance = d.pop("temporal_relevance", UNSET)

        _time_sensitive_at = d.pop("time_sensitive_at", UNSET)
        time_sensitive_at: datetime.datetime | Unset
        if isinstance(_time_sensitive_at,  Unset):
            time_sensitive_at = UNSET
        else:
            time_sensitive_at = isoparse(_time_sensitive_at)




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


        user_id = d.pop("user_id", UNSET)

        atomic_fact = cls(
            agent_id=agent_id,
            atomic_text=atomic_text,
            confidence=confidence,
            created_at=created_at,
            fact_id=fact_id,
            fact_type=fact_type,
            last_confirmed=last_confirmed,
            last_retrieved_at=last_retrieved_at,
            mention_count=mention_count,
            node_id=node_id,
            retention_strength=retention_strength,
            updated_at=updated_at,
            schema=schema,
            agent_framing=agent_framing,
            character_salience=character_salience,
            cluster_id=cluster_id,
            emotional_intensity=emotional_intensity,
            entities=entities,
            episode_id=episode_id,
            event_time=event_time,
            evidence_message_ids=evidence_message_ids,
            hit_count=hit_count,
            importance=importance,
            inferred_entities=inferred_entities,
            metadata=metadata,
            miss_count=miss_count,
            polarity_group_id=polarity_group_id,
            relationship_relevance=relationship_relevance,
            sentiment=sentiment,
            session_id=session_id,
            source_id=source_id,
            source_type=source_type,
            supersedes_id=supersedes_id,
            temporal_relevance=temporal_relevance,
            time_sensitive_at=time_sensitive_at,
            topic_tags=topic_tags,
            user_id=user_id,
        )

        return atomic_fact

