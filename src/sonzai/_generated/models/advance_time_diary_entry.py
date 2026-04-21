from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="AdvanceTimeDiaryEntry")



@_attrs_define
class AdvanceTimeDiaryEntry:
    """ 
        Attributes:
            content (str):
            date (str):
            mood (str | Unset):
            topics (list[str] | None | Unset):
     """

    content: str
    date: str
    mood: str | Unset = UNSET
    topics: list[str] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        date = self.date

        mood = self.mood

        topics: list[str] | None | Unset
        if isinstance(self.topics, Unset):
            topics = UNSET
        elif isinstance(self.topics, list):
            topics = self.topics


        else:
            topics = self.topics


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
            "date": date,
        })
        if mood is not UNSET:
            field_dict["mood"] = mood
        if topics is not UNSET:
            field_dict["topics"] = topics

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        date = d.pop("date")

        mood = d.pop("mood", UNSET)

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


        advance_time_diary_entry = cls(
            content=content,
            date=date,
            mood=mood,
            topics=topics,
        )

        return advance_time_diary_entry

