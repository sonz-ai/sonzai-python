from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.mood_state import MoodState
  from ..models.user_metadata import UserMetadata





T = TypeVar("T", bound="UserEntry")



@_attrs_define
class UserEntry:
    """ 
        Attributes:
            role (str):
            user_id (str):
            created_at (str | Unset):
            display_name (str | Unset):
            last_interaction_at (str | Unset):
            metadata (UserMetadata | Unset):
            mood (MoodState | Unset):
     """

    role: str
    user_id: str
    created_at: str | Unset = UNSET
    display_name: str | Unset = UNSET
    last_interaction_at: str | Unset = UNSET
    metadata: UserMetadata | Unset = UNSET
    mood: MoodState | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.mood_state import MoodState
        from ..models.user_metadata import UserMetadata
        role = self.role

        user_id = self.user_id

        created_at = self.created_at

        display_name = self.display_name

        last_interaction_at = self.last_interaction_at

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        mood: dict[str, Any] | Unset = UNSET
        if not isinstance(self.mood, Unset):
            mood = self.mood.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "role": role,
            "user_id": user_id,
        })
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if last_interaction_at is not UNSET:
            field_dict["last_interaction_at"] = last_interaction_at
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if mood is not UNSET:
            field_dict["mood"] = mood

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mood_state import MoodState
        from ..models.user_metadata import UserMetadata
        d = dict(src_dict)
        role = d.pop("role")

        user_id = d.pop("user_id")

        created_at = d.pop("created_at", UNSET)

        display_name = d.pop("display_name", UNSET)

        last_interaction_at = d.pop("last_interaction_at", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: UserMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = UserMetadata.from_dict(_metadata)




        _mood = d.pop("mood", UNSET)
        mood: MoodState | Unset
        if isinstance(_mood,  Unset):
            mood = UNSET
        else:
            mood = MoodState.from_dict(_mood)




        user_entry = cls(
            role=role,
            user_id=user_id,
            created_at=created_at,
            display_name=display_name,
            last_interaction_at=last_interaction_at,
            metadata=metadata,
            mood=mood,
        )

        return user_entry

