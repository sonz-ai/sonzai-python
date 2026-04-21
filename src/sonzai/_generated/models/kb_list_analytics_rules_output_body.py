from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_analytics_rule import KBAnalyticsRule





T = TypeVar("T", bound="KbListAnalyticsRulesOutputBody")



@_attrs_define
class KbListAnalyticsRulesOutputBody:
    """ 
        Attributes:
            rules (list[KBAnalyticsRule] | None): List of analytics rules
            total (int): Total count
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    rules: list[KBAnalyticsRule] | None
    total: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_analytics_rule import KBAnalyticsRule
        rules: list[dict[str, Any]] | None
        if isinstance(self.rules, list):
            rules = []
            for rules_type_0_item_data in self.rules:
                rules_type_0_item = rules_type_0_item_data.to_dict()
                rules.append(rules_type_0_item)


        else:
            rules = self.rules

        total = self.total

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "rules": rules,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_analytics_rule import KBAnalyticsRule
        d = dict(src_dict)
        def _parse_rules(data: object) -> list[KBAnalyticsRule] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                rules_type_0 = []
                _rules_type_0 = data
                for rules_type_0_item_data in (_rules_type_0):
                    rules_type_0_item = KBAnalyticsRule.from_dict(rules_type_0_item_data)



                    rules_type_0.append(rules_type_0_item)

                return rules_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBAnalyticsRule] | None, data)

        rules = _parse_rules(d.pop("rules"))


        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        kb_list_analytics_rules_output_body = cls(
            rules=rules,
            total=total,
            schema=schema,
        )

        return kb_list_analytics_rules_output_body

