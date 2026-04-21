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

if TYPE_CHECKING:
  from ..models.contract_payment import ContractPayment





T = TypeVar("T", bound="EnterpriseContract")



@_attrs_define
class EnterpriseContract:
    """ 
        Attributes:
            auto_renew (bool):
            bonus_credits_paid (bool):
            bonus_credits_usd (float):
            contract_id (str):
            created_at (datetime.datetime):
            credit_portion_usd (float):
            end_date (datetime.datetime):
            onetime_amount_usd (float):
            onetime_credit_usd (float):
            onetime_service_usd (float):
            payment_amount_usd (float):
            payment_credit_usd (float):
            payment_frequency (str):
            payment_schedule (list[ContractPayment] | None):
            payment_service_usd (float):
            service_portion_usd (float):
            start_date (datetime.datetime):
            status (str):
            tenant_id (str):
            total_value_usd (float):
            updated_at (datetime.datetime):
            schema (str | Unset): A URL to the JSON Schema for this object.
            created_by (str | Unset):
            credit_period_limit (int | Unset):
            notes (str | Unset):
            payment_link_url (str | Unset):
            service_period_limit (int | Unset):
            stripe_price_id (str | Unset):
            stripe_subscription_id (str | Unset):
     """

    auto_renew: bool
    bonus_credits_paid: bool
    bonus_credits_usd: float
    contract_id: str
    created_at: datetime.datetime
    credit_portion_usd: float
    end_date: datetime.datetime
    onetime_amount_usd: float
    onetime_credit_usd: float
    onetime_service_usd: float
    payment_amount_usd: float
    payment_credit_usd: float
    payment_frequency: str
    payment_schedule: list[ContractPayment] | None
    payment_service_usd: float
    service_portion_usd: float
    start_date: datetime.datetime
    status: str
    tenant_id: str
    total_value_usd: float
    updated_at: datetime.datetime
    schema: str | Unset = UNSET
    created_by: str | Unset = UNSET
    credit_period_limit: int | Unset = UNSET
    notes: str | Unset = UNSET
    payment_link_url: str | Unset = UNSET
    service_period_limit: int | Unset = UNSET
    stripe_price_id: str | Unset = UNSET
    stripe_subscription_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.contract_payment import ContractPayment
        auto_renew = self.auto_renew

        bonus_credits_paid = self.bonus_credits_paid

        bonus_credits_usd = self.bonus_credits_usd

        contract_id = self.contract_id

        created_at = self.created_at.isoformat()

        credit_portion_usd = self.credit_portion_usd

        end_date = self.end_date.isoformat()

        onetime_amount_usd = self.onetime_amount_usd

        onetime_credit_usd = self.onetime_credit_usd

        onetime_service_usd = self.onetime_service_usd

        payment_amount_usd = self.payment_amount_usd

        payment_credit_usd = self.payment_credit_usd

        payment_frequency = self.payment_frequency

        payment_schedule: list[dict[str, Any]] | None
        if isinstance(self.payment_schedule, list):
            payment_schedule = []
            for payment_schedule_type_0_item_data in self.payment_schedule:
                payment_schedule_type_0_item = payment_schedule_type_0_item_data.to_dict()
                payment_schedule.append(payment_schedule_type_0_item)


        else:
            payment_schedule = self.payment_schedule

        payment_service_usd = self.payment_service_usd

        service_portion_usd = self.service_portion_usd

        start_date = self.start_date.isoformat()

        status = self.status

        tenant_id = self.tenant_id

        total_value_usd = self.total_value_usd

        updated_at = self.updated_at.isoformat()

        schema = self.schema

        created_by = self.created_by

        credit_period_limit = self.credit_period_limit

        notes = self.notes

        payment_link_url = self.payment_link_url

        service_period_limit = self.service_period_limit

        stripe_price_id = self.stripe_price_id

        stripe_subscription_id = self.stripe_subscription_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "autoRenew": auto_renew,
            "bonusCreditsPaid": bonus_credits_paid,
            "bonusCreditsUsd": bonus_credits_usd,
            "contractId": contract_id,
            "createdAt": created_at,
            "creditPortionUsd": credit_portion_usd,
            "endDate": end_date,
            "onetimeAmountUsd": onetime_amount_usd,
            "onetimeCreditUsd": onetime_credit_usd,
            "onetimeServiceUsd": onetime_service_usd,
            "paymentAmountUsd": payment_amount_usd,
            "paymentCreditUsd": payment_credit_usd,
            "paymentFrequency": payment_frequency,
            "paymentSchedule": payment_schedule,
            "paymentServiceUsd": payment_service_usd,
            "servicePortionUsd": service_portion_usd,
            "startDate": start_date,
            "status": status,
            "tenantId": tenant_id,
            "totalValueUsd": total_value_usd,
            "updatedAt": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if credit_period_limit is not UNSET:
            field_dict["creditPeriodLimit"] = credit_period_limit
        if notes is not UNSET:
            field_dict["notes"] = notes
        if payment_link_url is not UNSET:
            field_dict["paymentLinkUrl"] = payment_link_url
        if service_period_limit is not UNSET:
            field_dict["servicePeriodLimit"] = service_period_limit
        if stripe_price_id is not UNSET:
            field_dict["stripePriceId"] = stripe_price_id
        if stripe_subscription_id is not UNSET:
            field_dict["stripeSubscriptionId"] = stripe_subscription_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.contract_payment import ContractPayment
        d = dict(src_dict)
        auto_renew = d.pop("autoRenew")

        bonus_credits_paid = d.pop("bonusCreditsPaid")

        bonus_credits_usd = d.pop("bonusCreditsUsd")

        contract_id = d.pop("contractId")

        created_at = isoparse(d.pop("createdAt"))




        credit_portion_usd = d.pop("creditPortionUsd")

        end_date = isoparse(d.pop("endDate"))




        onetime_amount_usd = d.pop("onetimeAmountUsd")

        onetime_credit_usd = d.pop("onetimeCreditUsd")

        onetime_service_usd = d.pop("onetimeServiceUsd")

        payment_amount_usd = d.pop("paymentAmountUsd")

        payment_credit_usd = d.pop("paymentCreditUsd")

        payment_frequency = d.pop("paymentFrequency")

        def _parse_payment_schedule(data: object) -> list[ContractPayment] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                payment_schedule_type_0 = []
                _payment_schedule_type_0 = data
                for payment_schedule_type_0_item_data in (_payment_schedule_type_0):
                    payment_schedule_type_0_item = ContractPayment.from_dict(payment_schedule_type_0_item_data)



                    payment_schedule_type_0.append(payment_schedule_type_0_item)

                return payment_schedule_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ContractPayment] | None, data)

        payment_schedule = _parse_payment_schedule(d.pop("paymentSchedule"))


        payment_service_usd = d.pop("paymentServiceUsd")

        service_portion_usd = d.pop("servicePortionUsd")

        start_date = isoparse(d.pop("startDate"))




        status = d.pop("status")

        tenant_id = d.pop("tenantId")

        total_value_usd = d.pop("totalValueUsd")

        updated_at = isoparse(d.pop("updatedAt"))




        schema = d.pop("$schema", UNSET)

        created_by = d.pop("createdBy", UNSET)

        credit_period_limit = d.pop("creditPeriodLimit", UNSET)

        notes = d.pop("notes", UNSET)

        payment_link_url = d.pop("paymentLinkUrl", UNSET)

        service_period_limit = d.pop("servicePeriodLimit", UNSET)

        stripe_price_id = d.pop("stripePriceId", UNSET)

        stripe_subscription_id = d.pop("stripeSubscriptionId", UNSET)

        enterprise_contract = cls(
            auto_renew=auto_renew,
            bonus_credits_paid=bonus_credits_paid,
            bonus_credits_usd=bonus_credits_usd,
            contract_id=contract_id,
            created_at=created_at,
            credit_portion_usd=credit_portion_usd,
            end_date=end_date,
            onetime_amount_usd=onetime_amount_usd,
            onetime_credit_usd=onetime_credit_usd,
            onetime_service_usd=onetime_service_usd,
            payment_amount_usd=payment_amount_usd,
            payment_credit_usd=payment_credit_usd,
            payment_frequency=payment_frequency,
            payment_schedule=payment_schedule,
            payment_service_usd=payment_service_usd,
            service_portion_usd=service_portion_usd,
            start_date=start_date,
            status=status,
            tenant_id=tenant_id,
            total_value_usd=total_value_usd,
            updated_at=updated_at,
            schema=schema,
            created_by=created_by,
            credit_period_limit=credit_period_limit,
            notes=notes,
            payment_link_url=payment_link_url,
            service_period_limit=service_period_limit,
            stripe_price_id=stripe_price_id,
            stripe_subscription_id=stripe_subscription_id,
        )

        return enterprise_contract

