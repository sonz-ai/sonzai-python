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
  from ..models.behavioral_traits import BehavioralTraits
  from ..models.big_5_assessment import Big5Assessment
  from ..models.interaction_preferences import InteractionPreferences
  from ..models.personality_dimensions import PersonalityDimensions





T = TypeVar("T", bound="AgentDetailResponse")



@_attrs_define
class AgentDetailResponse:
    """ 
        Attributes:
            agent_id (str):
            created_at (datetime.datetime):
            instance_count (int):
            is_active (bool):
            owner_user_id (str):
            tenant_id (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            avatar_url (str | Unset):
            behaviors (BehavioralTraits | Unset):
            big5 (Big5Assessment | Unset):
            bio (str | Unset):
            dimensions (PersonalityDimensions | Unset):
            gender (str | Unset):
            last_seen_at (datetime.datetime | Unset):
            name (str | Unset):
            owner_display_name (str | Unset):
            owner_email (str | Unset):
            personality_prompt (str | Unset):
            preferences (InteractionPreferences | Unset):
            primary_traits (list[str] | None | Unset):
            project_id (str | Unset):
            speech_patterns (list[str] | None | Unset):
            true_dislikes (list[str] | None | Unset):
            true_interests (list[str] | None | Unset):
     """

    agent_id: str
    created_at: datetime.datetime
    instance_count: int
    is_active: bool
    owner_user_id: str
    tenant_id: str
    schema: str | Unset = UNSET
    avatar_url: str | Unset = UNSET
    behaviors: BehavioralTraits | Unset = UNSET
    big5: Big5Assessment | Unset = UNSET
    bio: str | Unset = UNSET
    dimensions: PersonalityDimensions | Unset = UNSET
    gender: str | Unset = UNSET
    last_seen_at: datetime.datetime | Unset = UNSET
    name: str | Unset = UNSET
    owner_display_name: str | Unset = UNSET
    owner_email: str | Unset = UNSET
    personality_prompt: str | Unset = UNSET
    preferences: InteractionPreferences | Unset = UNSET
    primary_traits: list[str] | None | Unset = UNSET
    project_id: str | Unset = UNSET
    speech_patterns: list[str] | None | Unset = UNSET
    true_dislikes: list[str] | None | Unset = UNSET
    true_interests: list[str] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.behavioral_traits import BehavioralTraits
        from ..models.big_5_assessment import Big5Assessment
        from ..models.interaction_preferences import InteractionPreferences
        from ..models.personality_dimensions import PersonalityDimensions
        agent_id = self.agent_id

        created_at = self.created_at.isoformat()

        instance_count = self.instance_count

        is_active = self.is_active

        owner_user_id = self.owner_user_id

        tenant_id = self.tenant_id

        schema = self.schema

        avatar_url = self.avatar_url

        behaviors: dict[str, Any] | Unset = UNSET
        if not isinstance(self.behaviors, Unset):
            behaviors = self.behaviors.to_dict()

        big5: dict[str, Any] | Unset = UNSET
        if not isinstance(self.big5, Unset):
            big5 = self.big5.to_dict()

        bio = self.bio

        dimensions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dimensions, Unset):
            dimensions = self.dimensions.to_dict()

        gender = self.gender

        last_seen_at: str | Unset = UNSET
        if not isinstance(self.last_seen_at, Unset):
            last_seen_at = self.last_seen_at.isoformat()

        name = self.name

        owner_display_name = self.owner_display_name

        owner_email = self.owner_email

        personality_prompt = self.personality_prompt

        preferences: dict[str, Any] | Unset = UNSET
        if not isinstance(self.preferences, Unset):
            preferences = self.preferences.to_dict()

        primary_traits: list[str] | None | Unset
        if isinstance(self.primary_traits, Unset):
            primary_traits = UNSET
        elif isinstance(self.primary_traits, list):
            primary_traits = self.primary_traits


        else:
            primary_traits = self.primary_traits

        project_id = self.project_id

        speech_patterns: list[str] | None | Unset
        if isinstance(self.speech_patterns, Unset):
            speech_patterns = UNSET
        elif isinstance(self.speech_patterns, list):
            speech_patterns = self.speech_patterns


        else:
            speech_patterns = self.speech_patterns

        true_dislikes: list[str] | None | Unset
        if isinstance(self.true_dislikes, Unset):
            true_dislikes = UNSET
        elif isinstance(self.true_dislikes, list):
            true_dislikes = self.true_dislikes


        else:
            true_dislikes = self.true_dislikes

        true_interests: list[str] | None | Unset
        if isinstance(self.true_interests, Unset):
            true_interests = UNSET
        elif isinstance(self.true_interests, list):
            true_interests = self.true_interests


        else:
            true_interests = self.true_interests


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "created_at": created_at,
            "instance_count": instance_count,
            "is_active": is_active,
            "owner_user_id": owner_user_id,
            "tenant_id": tenant_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if avatar_url is not UNSET:
            field_dict["avatar_url"] = avatar_url
        if behaviors is not UNSET:
            field_dict["behaviors"] = behaviors
        if big5 is not UNSET:
            field_dict["big5"] = big5
        if bio is not UNSET:
            field_dict["bio"] = bio
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions
        if gender is not UNSET:
            field_dict["gender"] = gender
        if last_seen_at is not UNSET:
            field_dict["last_seen_at"] = last_seen_at
        if name is not UNSET:
            field_dict["name"] = name
        if owner_display_name is not UNSET:
            field_dict["owner_display_name"] = owner_display_name
        if owner_email is not UNSET:
            field_dict["owner_email"] = owner_email
        if personality_prompt is not UNSET:
            field_dict["personality_prompt"] = personality_prompt
        if preferences is not UNSET:
            field_dict["preferences"] = preferences
        if primary_traits is not UNSET:
            field_dict["primary_traits"] = primary_traits
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if speech_patterns is not UNSET:
            field_dict["speech_patterns"] = speech_patterns
        if true_dislikes is not UNSET:
            field_dict["true_dislikes"] = true_dislikes
        if true_interests is not UNSET:
            field_dict["true_interests"] = true_interests

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.behavioral_traits import BehavioralTraits
        from ..models.big_5_assessment import Big5Assessment
        from ..models.interaction_preferences import InteractionPreferences
        from ..models.personality_dimensions import PersonalityDimensions
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        created_at = isoparse(d.pop("created_at"))




        instance_count = d.pop("instance_count")

        is_active = d.pop("is_active")

        owner_user_id = d.pop("owner_user_id")

        tenant_id = d.pop("tenant_id")

        schema = d.pop("$schema", UNSET)

        avatar_url = d.pop("avatar_url", UNSET)

        _behaviors = d.pop("behaviors", UNSET)
        behaviors: BehavioralTraits | Unset
        if isinstance(_behaviors,  Unset):
            behaviors = UNSET
        else:
            behaviors = BehavioralTraits.from_dict(_behaviors)




        _big5 = d.pop("big5", UNSET)
        big5: Big5Assessment | Unset
        if isinstance(_big5,  Unset):
            big5 = UNSET
        else:
            big5 = Big5Assessment.from_dict(_big5)




        bio = d.pop("bio", UNSET)

        _dimensions = d.pop("dimensions", UNSET)
        dimensions: PersonalityDimensions | Unset
        if isinstance(_dimensions,  Unset):
            dimensions = UNSET
        else:
            dimensions = PersonalityDimensions.from_dict(_dimensions)




        gender = d.pop("gender", UNSET)

        _last_seen_at = d.pop("last_seen_at", UNSET)
        last_seen_at: datetime.datetime | Unset
        if isinstance(_last_seen_at,  Unset):
            last_seen_at = UNSET
        else:
            last_seen_at = isoparse(_last_seen_at)




        name = d.pop("name", UNSET)

        owner_display_name = d.pop("owner_display_name", UNSET)

        owner_email = d.pop("owner_email", UNSET)

        personality_prompt = d.pop("personality_prompt", UNSET)

        _preferences = d.pop("preferences", UNSET)
        preferences: InteractionPreferences | Unset
        if isinstance(_preferences,  Unset):
            preferences = UNSET
        else:
            preferences = InteractionPreferences.from_dict(_preferences)




        def _parse_primary_traits(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                primary_traits_type_0 = cast(list[str], data)

                return primary_traits_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        primary_traits = _parse_primary_traits(d.pop("primary_traits", UNSET))


        project_id = d.pop("project_id", UNSET)

        def _parse_speech_patterns(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                speech_patterns_type_0 = cast(list[str], data)

                return speech_patterns_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        speech_patterns = _parse_speech_patterns(d.pop("speech_patterns", UNSET))


        def _parse_true_dislikes(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                true_dislikes_type_0 = cast(list[str], data)

                return true_dislikes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        true_dislikes = _parse_true_dislikes(d.pop("true_dislikes", UNSET))


        def _parse_true_interests(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                true_interests_type_0 = cast(list[str], data)

                return true_interests_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        true_interests = _parse_true_interests(d.pop("true_interests", UNSET))


        agent_detail_response = cls(
            agent_id=agent_id,
            created_at=created_at,
            instance_count=instance_count,
            is_active=is_active,
            owner_user_id=owner_user_id,
            tenant_id=tenant_id,
            schema=schema,
            avatar_url=avatar_url,
            behaviors=behaviors,
            big5=big5,
            bio=bio,
            dimensions=dimensions,
            gender=gender,
            last_seen_at=last_seen_at,
            name=name,
            owner_display_name=owner_display_name,
            owner_email=owner_email,
            personality_prompt=personality_prompt,
            preferences=preferences,
            primary_traits=primary_traits,
            project_id=project_id,
            speech_patterns=speech_patterns,
            true_dislikes=true_dislikes,
            true_interests=true_interests,
        )

        return agent_detail_response

