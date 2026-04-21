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






T = TypeVar("T", bound="DiaryEntry")



@_attrs_define
class DiaryEntry:
    """ 
        Attributes:
            agent_id (str):
            content (str):
            created_at (datetime.datetime):
            date (str):
            entry_id (str):
            body_lines (list[str] | None | Unset):
            mood (str | Unset):
            tags (list[str] | None | Unset):
            title (str | Unset):
            topics (list[str] | None | Unset):
            trigger_type (str | Unset):
            user_id (str | Unset):
     """

    agent_id: str
    content: str
    created_at: datetime.datetime
    date: str
    entry_id: str
    body_lines: list[str] | None | Unset = UNSET
    mood: str | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    title: str | Unset = UNSET
    topics: list[str] | None | Unset = UNSET
    trigger_type: str | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        content = self.content

        created_at = self.created_at.isoformat()

        date = self.date

        entry_id = self.entry_id

        body_lines: list[str] | None | Unset
        if isinstance(self.body_lines, Unset):
            body_lines = UNSET
        elif isinstance(self.body_lines, list):
            body_lines = self.body_lines


        else:
            body_lines = self.body_lines

        mood = self.mood

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags


        else:
            tags = self.tags

        title = self.title

        topics: list[str] | None | Unset
        if isinstance(self.topics, Unset):
            topics = UNSET
        elif isinstance(self.topics, list):
            topics = self.topics


        else:
            topics = self.topics

        trigger_type = self.trigger_type

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "content": content,
            "created_at": created_at,
            "date": date,
            "entry_id": entry_id,
        })
        if body_lines is not UNSET:
            field_dict["body_lines"] = body_lines
        if mood is not UNSET:
            field_dict["mood"] = mood
        if tags is not UNSET:
            field_dict["tags"] = tags
        if title is not UNSET:
            field_dict["title"] = title
        if topics is not UNSET:
            field_dict["topics"] = topics
        if trigger_type is not UNSET:
            field_dict["trigger_type"] = trigger_type
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        content = d.pop("content")

        created_at = isoparse(d.pop("created_at"))




        date = d.pop("date")

        entry_id = d.pop("entry_id")

        def _parse_body_lines(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                body_lines_type_0 = cast(list[str], data)

                return body_lines_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        body_lines = _parse_body_lines(d.pop("body_lines", UNSET))


        mood = d.pop("mood", UNSET)

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))


        title = d.pop("title", UNSET)

        def _parse_topics(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                topics_type_0 = cast(list[str], data)

                return topics_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        topics = _parse_topics(d.pop("topics", UNSET))


        trigger_type = d.pop("trigger_type", UNSET)

        user_id = d.pop("user_id", UNSET)

        diary_entry = cls(
            agent_id=agent_id,
            content=content,
            created_at=created_at,
            date=date,
            entry_id=entry_id,
            body_lines=body_lines,
            mood=mood,
            tags=tags,
            title=title,
            topics=topics,
            trigger_type=trigger_type,
            user_id=user_id,
        )

        return diary_entry

