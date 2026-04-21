from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.update_metadata_request_custom import UpdateMetadataRequestCustom





T = TypeVar("T", bound="UpdateMetadataRequest")



@_attrs_define
class UpdateMetadataRequest:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            company (str | Unset):
            custom (UpdateMetadataRequestCustom | Unset):
            display_name (str | Unset):
            email (str | Unset):
            phone (str | Unset):
            title (str | Unset):
     """

    schema: str | Unset = UNSET
    company: str | Unset = UNSET
    custom: UpdateMetadataRequestCustom | Unset = UNSET
    display_name: str | Unset = UNSET
    email: str | Unset = UNSET
    phone: str | Unset = UNSET
    title: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_metadata_request_custom import UpdateMetadataRequestCustom
        schema = self.schema

        company = self.company

        custom: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom, Unset):
            custom = self.custom.to_dict()

        display_name = self.display_name

        email = self.email

        phone = self.phone

        title = self.title


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if company is not UNSET:
            field_dict["company"] = company
        if custom is not UNSET:
            field_dict["custom"] = custom
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if email is not UNSET:
            field_dict["email"] = email
        if phone is not UNSET:
            field_dict["phone"] = phone
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_metadata_request_custom import UpdateMetadataRequestCustom
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        company = d.pop("company", UNSET)

        _custom = d.pop("custom", UNSET)
        custom: UpdateMetadataRequestCustom | Unset
        if isinstance(_custom,  Unset):
            custom = UNSET
        else:
            custom = UpdateMetadataRequestCustom.from_dict(_custom)




        display_name = d.pop("display_name", UNSET)

        email = d.pop("email", UNSET)

        phone = d.pop("phone", UNSET)

        title = d.pop("title", UNSET)

        update_metadata_request = cls(
            schema=schema,
            company=company,
            custom=custom,
            display_name=display_name,
            email=email,
            phone=phone,
            title=title,
        )

        return update_metadata_request

