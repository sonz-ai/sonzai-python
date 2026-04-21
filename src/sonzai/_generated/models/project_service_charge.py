from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="ProjectServiceCharge")



@_attrs_define
class ProjectServiceCharge:
    """ 
        Attributes:
            active (bool):
            amount_usd (float):
            charge_id (str):
            charge_type (str):
            created_at (datetime.datetime):
            description (str):
            tenant_id (str):
            updated_at (datetime.datetime):
            billed_at (datetime.datetime | Unset):
            created_by (str | Unset):
            project_id (str | Unset):
            project_name (str | Unset):
     """

    active: bool
    amount_usd: float
    charge_id: str
    charge_type: str
    created_at: datetime.datetime
    description: str
    tenant_id: str
    updated_at: datetime.datetime
    billed_at: datetime.datetime | Unset = UNSET
    created_by: str | Unset = UNSET
    project_id: str | Unset = UNSET
    project_name: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        active = self.active

        amount_usd = self.amount_usd

        charge_id = self.charge_id

        charge_type = self.charge_type

        created_at = self.created_at.isoformat()

        description = self.description

        tenant_id = self.tenant_id

        updated_at = self.updated_at.isoformat()

        billed_at: str | Unset = UNSET
        if not isinstance(self.billed_at, Unset):
            billed_at = self.billed_at.isoformat()

        created_by = self.created_by

        project_id = self.project_id

        project_name = self.project_name


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "active": active,
            "amountUsd": amount_usd,
            "chargeId": charge_id,
            "chargeType": charge_type,
            "createdAt": created_at,
            "description": description,
            "tenantId": tenant_id,
            "updatedAt": updated_at,
        })
        if billed_at is not UNSET:
            field_dict["billedAt"] = billed_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if project_name is not UNSET:
            field_dict["projectName"] = project_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active = d.pop("active")

        amount_usd = d.pop("amountUsd")

        charge_id = d.pop("chargeId")

        charge_type = d.pop("chargeType")

        created_at = isoparse(d.pop("createdAt"))




        description = d.pop("description")

        tenant_id = d.pop("tenantId")

        updated_at = isoparse(d.pop("updatedAt"))




        _billed_at = d.pop("billedAt", UNSET)
        billed_at: datetime.datetime | Unset
        if isinstance(_billed_at,  Unset):
            billed_at = UNSET
        else:
            billed_at = isoparse(_billed_at)




        created_by = d.pop("createdBy", UNSET)

        project_id = d.pop("projectId", UNSET)

        project_name = d.pop("projectName", UNSET)

        project_service_charge = cls(
            active=active,
            amount_usd=amount_usd,
            charge_id=charge_id,
            charge_type=charge_type,
            created_at=created_at,
            description=description,
            tenant_id=tenant_id,
            updated_at=updated_at,
            billed_at=billed_at,
            created_by=created_by,
            project_id=project_id,
            project_name=project_name,
        )

        return project_service_charge

