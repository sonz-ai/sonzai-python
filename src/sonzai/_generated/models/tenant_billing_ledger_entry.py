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






T = TypeVar("T", bound="TenantBillingLedgerEntry")



@_attrs_define
class TenantBillingLedgerEntry:
    """ 
        Attributes:
            amount_credits (float):
            amount_usd (float):
            created_at (datetime.datetime):
            description (str):
            entry_id (str):
            entry_type (str):
            tenant_id (str):
            tokens (int):
            created_by (str | Unset):
            traffic_source (str | Unset):
     """

    amount_credits: float
    amount_usd: float
    created_at: datetime.datetime
    description: str
    entry_id: str
    entry_type: str
    tenant_id: str
    tokens: int
    created_by: str | Unset = UNSET
    traffic_source: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        amount_credits = self.amount_credits

        amount_usd = self.amount_usd

        created_at = self.created_at.isoformat()

        description = self.description

        entry_id = self.entry_id

        entry_type = self.entry_type

        tenant_id = self.tenant_id

        tokens = self.tokens

        created_by = self.created_by

        traffic_source = self.traffic_source


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "amountCredits": amount_credits,
            "amountUsd": amount_usd,
            "createdAt": created_at,
            "description": description,
            "entryId": entry_id,
            "entryType": entry_type,
            "tenantId": tenant_id,
            "tokens": tokens,
        })
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if traffic_source is not UNSET:
            field_dict["trafficSource"] = traffic_source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_credits = d.pop("amountCredits")

        amount_usd = d.pop("amountUsd")

        created_at = isoparse(d.pop("createdAt"))




        description = d.pop("description")

        entry_id = d.pop("entryId")

        entry_type = d.pop("entryType")

        tenant_id = d.pop("tenantId")

        tokens = d.pop("tokens")

        created_by = d.pop("createdBy", UNSET)

        traffic_source = d.pop("trafficSource", UNSET)

        tenant_billing_ledger_entry = cls(
            amount_credits=amount_credits,
            amount_usd=amount_usd,
            created_at=created_at,
            description=description,
            entry_id=entry_id,
            entry_type=entry_type,
            tenant_id=tenant_id,
            tokens=tokens,
            created_by=created_by,
            traffic_source=traffic_source,
        )

        return tenant_billing_ledger_entry

