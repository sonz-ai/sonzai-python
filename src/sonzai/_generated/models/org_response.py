from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="OrgResponse")



@_attrs_define
class OrgResponse:
    """ 
        Attributes:
            created_at (str):
            id (str):
            member_count (int):
            name (str):
            role (str):
            slug (str | Unset):
     """

    created_at: str
    id: str
    member_count: int
    name: str
    role: str
    slug: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        id = self.id

        member_count = self.member_count

        name = self.name

        role = self.role

        slug = self.slug


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "id": id,
            "member_count": member_count,
            "name": name,
            "role": role,
        })
        if slug is not UNSET:
            field_dict["slug"] = slug

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("created_at")

        id = d.pop("id")

        member_count = d.pop("member_count")

        name = d.pop("name")

        role = d.pop("role")

        slug = d.pop("slug", UNSET)

        org_response = cls(
            created_at=created_at,
            id=id,
            member_count=member_count,
            name=name,
            role=role,
            slug=slug,
        )

        return org_response

