from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.prime_user_metadata_custom import PrimeUserMetadataCustom





T = TypeVar("T", bound="PrimeUserMetadata")



@_attrs_define
class PrimeUserMetadata:
    """ 
        Attributes:
            company (str | Unset):
            custom (PrimeUserMetadataCustom | Unset):
            email (str | Unset):
            phone (str | Unset):
            title (str | Unset):
     """

    company: str | Unset = UNSET
    custom: PrimeUserMetadataCustom | Unset = UNSET
    email: str | Unset = UNSET
    phone: str | Unset = UNSET
    title: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.prime_user_metadata_custom import PrimeUserMetadataCustom
        company = self.company

        custom: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom, Unset):
            custom = self.custom.to_dict()

        email = self.email

        phone = self.phone

        title = self.title


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if company is not UNSET:
            field_dict["company"] = company
        if custom is not UNSET:
            field_dict["custom"] = custom
        if email is not UNSET:
            field_dict["email"] = email
        if phone is not UNSET:
            field_dict["phone"] = phone
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.prime_user_metadata_custom import PrimeUserMetadataCustom
        d = dict(src_dict)
        company = d.pop("company", UNSET)

        _custom = d.pop("custom", UNSET)
        custom: PrimeUserMetadataCustom | Unset
        if isinstance(_custom,  Unset):
            custom = UNSET
        else:
            custom = PrimeUserMetadataCustom.from_dict(_custom)




        email = d.pop("email", UNSET)

        phone = d.pop("phone", UNSET)

        title = d.pop("title", UNSET)

        prime_user_metadata = cls(
            company=company,
            custom=custom,
            email=email,
            phone=phone,
            title=title,
        )

        return prime_user_metadata

