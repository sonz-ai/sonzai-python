from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostByCharacter")



@_attrs_define
class CostByCharacter:
    """ 
        Attributes:
            agent_id (str):
            agent_name (str):
            project_id (str):
            project_name (str):
     """

    agent_id: str
    agent_name: str
    project_id: str
    project_name: str





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        agent_name = self.agent_name

        project_id = self.project_id

        project_name = self.project_name


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agentId": agent_id,
            "agentName": agent_name,
            "projectId": project_id,
            "projectName": project_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agentId")

        agent_name = d.pop("agentName")

        project_id = d.pop("projectId")

        project_name = d.pop("projectName")

        cost_by_character = cls(
            agent_id=agent_id,
            agent_name=agent_name,
            project_id=project_id,
            project_name=project_name,
        )

        return cost_by_character

