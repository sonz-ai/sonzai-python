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
  from ..models.tenant_billing_profile_event_prices import TenantBillingProfileEventPrices
  from ..models.tenant_billing_profile_service_prices import TenantBillingProfileServicePrices





T = TypeVar("T", bound="TenantBillingProfile")



@_attrs_define
class TenantBillingProfile:
    """ 
        Attributes:
            billing_mode (str):
            char_price_per_month_usd (float):
            credit_balance (float):
            currency (str):
            event_prices (TenantBillingProfileEventPrices):
            free_credit_granted (bool):
            input_token_price_per_1k_usd (float):
            output_token_price_per_1k_usd (float):
            outstanding_usd (float):
            postpaid_limit_usd (float):
            service_prices (TenantBillingProfileServicePrices):
            tenant_id (str):
            token_price_per_1k_usd (float):
            updated_at (datetime.datetime):
            schema (str | Unset): A URL to the JSON Schema for this object.
            stripe_customer_id (str | Unset):
     """

    billing_mode: str
    char_price_per_month_usd: float
    credit_balance: float
    currency: str
    event_prices: TenantBillingProfileEventPrices
    free_credit_granted: bool
    input_token_price_per_1k_usd: float
    output_token_price_per_1k_usd: float
    outstanding_usd: float
    postpaid_limit_usd: float
    service_prices: TenantBillingProfileServicePrices
    tenant_id: str
    token_price_per_1k_usd: float
    updated_at: datetime.datetime
    schema: str | Unset = UNSET
    stripe_customer_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.tenant_billing_profile_event_prices import TenantBillingProfileEventPrices
        from ..models.tenant_billing_profile_service_prices import TenantBillingProfileServicePrices
        billing_mode = self.billing_mode

        char_price_per_month_usd = self.char_price_per_month_usd

        credit_balance = self.credit_balance

        currency = self.currency

        event_prices = self.event_prices.to_dict()

        free_credit_granted = self.free_credit_granted

        input_token_price_per_1k_usd = self.input_token_price_per_1k_usd

        output_token_price_per_1k_usd = self.output_token_price_per_1k_usd

        outstanding_usd = self.outstanding_usd

        postpaid_limit_usd = self.postpaid_limit_usd

        service_prices = self.service_prices.to_dict()

        tenant_id = self.tenant_id

        token_price_per_1k_usd = self.token_price_per_1k_usd

        updated_at = self.updated_at.isoformat()

        schema = self.schema

        stripe_customer_id = self.stripe_customer_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "billingMode": billing_mode,
            "charPricePerMonthUsd": char_price_per_month_usd,
            "creditBalance": credit_balance,
            "currency": currency,
            "eventPrices": event_prices,
            "freeCreditGranted": free_credit_granted,
            "inputTokenPricePer1KUsd": input_token_price_per_1k_usd,
            "outputTokenPricePer1KUsd": output_token_price_per_1k_usd,
            "outstandingUsd": outstanding_usd,
            "postpaidLimitUsd": postpaid_limit_usd,
            "servicePrices": service_prices,
            "tenantId": tenant_id,
            "tokenPricePer1KUsd": token_price_per_1k_usd,
            "updatedAt": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if stripe_customer_id is not UNSET:
            field_dict["stripeCustomerId"] = stripe_customer_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tenant_billing_profile_event_prices import TenantBillingProfileEventPrices
        from ..models.tenant_billing_profile_service_prices import TenantBillingProfileServicePrices
        d = dict(src_dict)
        billing_mode = d.pop("billingMode")

        char_price_per_month_usd = d.pop("charPricePerMonthUsd")

        credit_balance = d.pop("creditBalance")

        currency = d.pop("currency")

        event_prices = TenantBillingProfileEventPrices.from_dict(d.pop("eventPrices"))




        free_credit_granted = d.pop("freeCreditGranted")

        input_token_price_per_1k_usd = d.pop("inputTokenPricePer1KUsd")

        output_token_price_per_1k_usd = d.pop("outputTokenPricePer1KUsd")

        outstanding_usd = d.pop("outstandingUsd")

        postpaid_limit_usd = d.pop("postpaidLimitUsd")

        service_prices = TenantBillingProfileServicePrices.from_dict(d.pop("servicePrices"))




        tenant_id = d.pop("tenantId")

        token_price_per_1k_usd = d.pop("tokenPricePer1KUsd")

        updated_at = isoparse(d.pop("updatedAt"))




        schema = d.pop("$schema", UNSET)

        stripe_customer_id = d.pop("stripeCustomerId", UNSET)

        tenant_billing_profile = cls(
            billing_mode=billing_mode,
            char_price_per_month_usd=char_price_per_month_usd,
            credit_balance=credit_balance,
            currency=currency,
            event_prices=event_prices,
            free_credit_granted=free_credit_granted,
            input_token_price_per_1k_usd=input_token_price_per_1k_usd,
            output_token_price_per_1k_usd=output_token_price_per_1k_usd,
            outstanding_usd=outstanding_usd,
            postpaid_limit_usd=postpaid_limit_usd,
            service_prices=service_prices,
            tenant_id=tenant_id,
            token_price_per_1k_usd=token_price_per_1k_usd,
            updated_at=updated_at,
            schema=schema,
            stripe_customer_id=stripe_customer_id,
        )

        return tenant_billing_profile

