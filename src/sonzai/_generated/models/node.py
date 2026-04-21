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






T = TypeVar("T", bound="Node")



@_attrs_define
class Node:
    """ 
        Attributes:
            agent_id (str):
            brightness (float):
            created_at (datetime.datetime):
            description (str):
            first_mentioned_at (datetime.datetime):
            label (str):
            last_mentioned_at (datetime.datetime):
            mention_count (int):
            node_id (str):
            node_type (str):
            significance (float):
            updated_at (datetime.datetime):
            user_id (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    agent_id: str
    brightness: float
    created_at: datetime.datetime
    description: str
    first_mentioned_at: datetime.datetime
    label: str
    last_mentioned_at: datetime.datetime
    mention_count: int
    node_id: str
    node_type: str
    significance: float
    updated_at: datetime.datetime
    user_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        brightness = self.brightness

        created_at = self.created_at.isoformat()

        description = self.description

        first_mentioned_at = self.first_mentioned_at.isoformat()

        label = self.label

        last_mentioned_at = self.last_mentioned_at.isoformat()

        mention_count = self.mention_count

        node_id = self.node_id

        node_type = self.node_type

        significance = self.significance

        updated_at = self.updated_at.isoformat()

        user_id = self.user_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "AgentID": agent_id,
            "Brightness": brightness,
            "CreatedAt": created_at,
            "Description": description,
            "FirstMentionedAt": first_mentioned_at,
            "Label": label,
            "LastMentionedAt": last_mentioned_at,
            "MentionCount": mention_count,
            "NodeID": node_id,
            "NodeType": node_type,
            "Significance": significance,
            "UpdatedAt": updated_at,
            "UserID": user_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("AgentID")

        brightness = d.pop("Brightness")

        created_at = isoparse(d.pop("CreatedAt"))




        description = d.pop("Description")

        first_mentioned_at = isoparse(d.pop("FirstMentionedAt"))




        label = d.pop("Label")

        last_mentioned_at = isoparse(d.pop("LastMentionedAt"))




        mention_count = d.pop("MentionCount")

        node_id = d.pop("NodeID")

        node_type = d.pop("NodeType")

        significance = d.pop("Significance")

        updated_at = isoparse(d.pop("UpdatedAt"))




        user_id = d.pop("UserID")

        schema = d.pop("$schema", UNSET)

        node = cls(
            agent_id=agent_id,
            brightness=brightness,
            created_at=created_at,
            description=description,
            first_mentioned_at=first_mentioned_at,
            label=label,
            last_mentioned_at=last_mentioned_at,
            mention_count=mention_count,
            node_id=node_id,
            node_type=node_type,
            significance=significance,
            updated_at=updated_at,
            user_id=user_id,
            schema=schema,
        )

        return node

