from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.user_metadata_custom import UserMetadataCustom





T = TypeVar("T", bound="UserMetadata")



@_attrs_define
class UserMetadata:
    """ 
        Attributes:
            custom (UserMetadataCustom | Unset):
            email (str | Unset):
            phone (str | Unset):
     """

    custom: UserMetadataCustom | Unset = UNSET
    email: str | Unset = UNSET
    phone: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.user_metadata_custom import UserMetadataCustom
        custom: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom, Unset):
            custom = self.custom.to_dict()

        email = self.email

        phone = self.phone


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if custom is not UNSET:
            field_dict["custom"] = custom
        if email is not UNSET:
            field_dict["email"] = email
        if phone is not UNSET:
            field_dict["phone"] = phone

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_metadata_custom import UserMetadataCustom
        d = dict(src_dict)
        _custom = d.pop("custom", UNSET)
        custom: UserMetadataCustom | Unset
        if isinstance(_custom,  Unset):
            custom = UNSET
        else:
            custom = UserMetadataCustom.from_dict(_custom)




        email = d.pop("email", UNSET)

        phone = d.pop("phone", UNSET)

        user_metadata = cls(
            custom=custom,
            email=email,
            phone=phone,
        )

        return user_metadata

