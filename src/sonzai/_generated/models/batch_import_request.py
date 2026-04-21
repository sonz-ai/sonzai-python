from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.batch_import_user import BatchImportUser





T = TypeVar("T", bound="BatchImportRequest")



@_attrs_define
class BatchImportRequest:
    """ 
        Attributes:
            users (list[BatchImportUser] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
            source (str | Unset):
     """

    users: list[BatchImportUser] | None
    schema: str | Unset = UNSET
    source: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_import_user import BatchImportUser
        users: list[dict[str, Any]] | None
        if isinstance(self.users, list):
            users = []
            for users_type_0_item_data in self.users:
                users_type_0_item = users_type_0_item_data.to_dict()
                users.append(users_type_0_item)


        else:
            users = self.users

        schema = self.schema

        source = self.source


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "users": users,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_import_user import BatchImportUser
        d = dict(src_dict)
        def _parse_users(data: object) -> list[BatchImportUser] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                users_type_0 = []
                _users_type_0 = data
                for users_type_0_item_data in (_users_type_0):
                    users_type_0_item = BatchImportUser.from_dict(users_type_0_item_data)



                    users_type_0.append(users_type_0_item)

                return users_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[BatchImportUser] | None, data)

        users = _parse_users(d.pop("users"))


        schema = d.pop("$schema", UNSET)

        source = d.pop("source", UNSET)

        batch_import_request = cls(
            users=users,
            schema=schema,
            source=source,
        )

        return batch_import_request

