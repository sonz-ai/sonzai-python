from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="GenerateBioInputBody")



@_attrs_define
class GenerateBioInputBody:
    """ 
        Attributes:
            description (str): Free-text personality description
            gender (str): Agent gender
            name (str): Agent display name
            schema (str | Unset): A URL to the JSON Schema for this object.
            current_bio (str | Unset): Current bio to improve upon
            enriched_context_json (Any | Unset): Pre-built enriched context (from orchestrator)
            instance_id (str | Unset): Agent instance identifier
            style (str | Unset): Bio generation style
            user_id (str | Unset): User ID (from orchestrator)
     """

    description: str
    gender: str
    name: str
    schema: str | Unset = UNSET
    current_bio: str | Unset = UNSET
    enriched_context_json: Any | Unset = UNSET
    instance_id: str | Unset = UNSET
    style: str | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        gender = self.gender

        name = self.name

        schema = self.schema

        current_bio = self.current_bio

        enriched_context_json = self.enriched_context_json

        instance_id = self.instance_id

        style = self.style

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "description": description,
            "gender": gender,
            "name": name,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if current_bio is not UNSET:
            field_dict["current_bio"] = current_bio
        if enriched_context_json is not UNSET:
            field_dict["enriched_context_json"] = enriched_context_json
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id
        if style is not UNSET:
            field_dict["style"] = style
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        gender = d.pop("gender")

        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        current_bio = d.pop("current_bio", UNSET)

        enriched_context_json = d.pop("enriched_context_json", UNSET)

        instance_id = d.pop("instance_id", UNSET)

        style = d.pop("style", UNSET)

        user_id = d.pop("user_id", UNSET)

        generate_bio_input_body = cls(
            description=description,
            gender=gender,
            name=name,
            schema=schema,
            current_bio=current_bio,
            enriched_context_json=enriched_context_json,
            instance_id=instance_id,
            style=style,
            user_id=user_id,
        )

        return generate_bio_input_body

