from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.user_entry import UserEntry





T = TypeVar("T", bound="UsersResponse")



@_attrs_define
class UsersResponse:
    """ 
        Attributes:
            total (int):
            users (list[UserEntry] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    total: int
    users: list[UserEntry] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.user_entry import UserEntry
        total = self.total

        users: list[dict[str, Any]] | None
        if isinstance(self.users, list):
            users = []
            for users_type_0_item_data in self.users:
                users_type_0_item = users_type_0_item_data.to_dict()
                users.append(users_type_0_item)


        else:
            users = self.users

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "total": total,
            "users": users,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_entry import UserEntry
        d = dict(src_dict)
        total = d.pop("total")

        def _parse_users(data: object) -> list[UserEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                users_type_0 = []
                _users_type_0 = data
                for users_type_0_item_data in (_users_type_0):
                    users_type_0_item = UserEntry.from_dict(users_type_0_item_data)



                    users_type_0.append(users_type_0_item)

                return users_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UserEntry] | None, data)

        users = _parse_users(d.pop("users"))


        schema = d.pop("$schema", UNSET)

        users_response = cls(
            total=total,
            users=users,
            schema=schema,
        )

        return users_response

