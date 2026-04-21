from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.group_result_values import GroupResultValues





T = TypeVar("T", bound="GroupResult")



@_attrs_define
class GroupResult:
    """ 
        Attributes:
            group (str):
            values (GroupResultValues):
     """

    group: str
    values: GroupResultValues





    def to_dict(self) -> dict[str, Any]:
        from ..models.group_result_values import GroupResultValues
        group = self.group

        values = self.values.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "group": group,
            "values": values,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.group_result_values import GroupResultValues
        d = dict(src_dict)
        group = d.pop("group")

        values = GroupResultValues.from_dict(d.pop("values"))




        group_result = cls(
            group=group,
            values=values,
        )

        return group_result

