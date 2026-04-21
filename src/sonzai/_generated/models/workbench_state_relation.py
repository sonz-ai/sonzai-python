from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="WorkbenchStateRelation")



@_attrs_define
class WorkbenchStateRelation:
    """ 
        Attributes:
            agent_to_user (int):
            user_to_agent (int):
     """

    agent_to_user: int
    user_to_agent: int





    def to_dict(self) -> dict[str, Any]:
        agent_to_user = self.agent_to_user

        user_to_agent = self.user_to_agent


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_to_user": agent_to_user,
            "user_to_agent": user_to_agent,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_to_user = d.pop("agent_to_user")

        user_to_agent = d.pop("user_to_agent")

        workbench_state_relation = cls(
            agent_to_user=agent_to_user,
            user_to_agent=user_to_agent,
        )

        return workbench_state_relation

