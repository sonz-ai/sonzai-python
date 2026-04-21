from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.job_user import JobUser





T = TypeVar("T", bound="ListImportJobUsersOutputBody")



@_attrs_define
class ListImportJobUsersOutputBody:
    """ 
        Attributes:
            count (int): Number of rows returned
            users (list[JobUser] | None): Per-user progress rows for this job
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    count: int
    users: list[JobUser] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.job_user import JobUser
        count = self.count

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
            "count": count,
            "users": users,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_user import JobUser
        d = dict(src_dict)
        count = d.pop("count")

        def _parse_users(data: object) -> list[JobUser] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                users_type_0 = []
                _users_type_0 = data
                for users_type_0_item_data in (_users_type_0):
                    users_type_0_item = JobUser.from_dict(users_type_0_item_data)



                    users_type_0.append(users_type_0_item)

                return users_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[JobUser] | None, data)

        users = _parse_users(d.pop("users"))


        schema = d.pop("$schema", UNSET)

        list_import_job_users_output_body = cls(
            count=count,
            users=users,
            schema=schema,
        )

        return list_import_job_users_output_body

