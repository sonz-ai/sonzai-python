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






T = TypeVar("T", bound="ContractPayment")



@_attrs_define
class ContractPayment:
    """ 
        Attributes:
            amount_usd (float):
            credit_usd (float):
            due_date (datetime.datetime):
            paid (bool):
            period (str):
            service_usd (float):
            is_one_time (bool | Unset):
     """

    amount_usd: float
    credit_usd: float
    due_date: datetime.datetime
    paid: bool
    period: str
    service_usd: float
    is_one_time: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        amount_usd = self.amount_usd

        credit_usd = self.credit_usd

        due_date = self.due_date.isoformat()

        paid = self.paid

        period = self.period

        service_usd = self.service_usd

        is_one_time = self.is_one_time


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "amountUsd": amount_usd,
            "creditUsd": credit_usd,
            "dueDate": due_date,
            "paid": paid,
            "period": period,
            "serviceUsd": service_usd,
        })
        if is_one_time is not UNSET:
            field_dict["isOneTime"] = is_one_time

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_usd = d.pop("amountUsd")

        credit_usd = d.pop("creditUsd")

        due_date = isoparse(d.pop("dueDate"))




        paid = d.pop("paid")

        period = d.pop("period")

        service_usd = d.pop("serviceUsd")

        is_one_time = d.pop("isOneTime", UNSET)

        contract_payment = cls(
            amount_usd=amount_usd,
            credit_usd=credit_usd,
            due_date=due_date,
            paid=paid,
            period=period,
            service_usd=service_usd,
            is_one_time=is_one_time,
        )

        return contract_payment

