from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.org_response import OrgResponse





T = TypeVar("T", bound="MeResponse")



@_attrs_define
class MeResponse:
    """ 
        Attributes:
            email (str):
            orgs (list[OrgResponse] | None):
            user_id (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    email: str
    orgs: list[OrgResponse] | None
    user_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.org_response import OrgResponse
        email = self.email

        orgs: list[dict[str, Any]] | None
        if isinstance(self.orgs, list):
            orgs = []
            for orgs_type_0_item_data in self.orgs:
                orgs_type_0_item = orgs_type_0_item_data.to_dict()
                orgs.append(orgs_type_0_item)


        else:
            orgs = self.orgs

        user_id = self.user_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "email": email,
            "orgs": orgs,
            "user_id": user_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.org_response import OrgResponse
        d = dict(src_dict)
        email = d.pop("email")

        def _parse_orgs(data: object) -> list[OrgResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                orgs_type_0 = []
                _orgs_type_0 = data
                for orgs_type_0_item_data in (_orgs_type_0):
                    orgs_type_0_item = OrgResponse.from_dict(orgs_type_0_item_data)



                    orgs_type_0.append(orgs_type_0_item)

                return orgs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[OrgResponse] | None, data)

        orgs = _parse_orgs(d.pop("orgs"))


        user_id = d.pop("user_id")

        schema = d.pop("$schema", UNSET)

        me_response = cls(
            email=email,
            orgs=orgs,
            user_id=user_id,
            schema=schema,
        )

        return me_response

