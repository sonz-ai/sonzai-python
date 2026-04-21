from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.atomic_fact import AtomicFact





T = TypeVar("T", bound="TimelineSession")



@_attrs_define
class TimelineSession:
    """ 
        Attributes:
            fact_count (int):
            facts (list[AtomicFact] | None):
            first_fact_at (str):
            last_fact_at (str):
            session_id (str):
     """

    fact_count: int
    facts: list[AtomicFact] | None
    first_fact_at: str
    last_fact_at: str
    session_id: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.atomic_fact import AtomicFact
        fact_count = self.fact_count

        facts: list[dict[str, Any]] | None
        if isinstance(self.facts, list):
            facts = []
            for facts_type_0_item_data in self.facts:
                facts_type_0_item = facts_type_0_item_data.to_dict()
                facts.append(facts_type_0_item)


        else:
            facts = self.facts

        first_fact_at = self.first_fact_at

        last_fact_at = self.last_fact_at

        session_id = self.session_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "fact_count": fact_count,
            "facts": facts,
            "first_fact_at": first_fact_at,
            "last_fact_at": last_fact_at,
            "session_id": session_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.atomic_fact import AtomicFact
        d = dict(src_dict)
        fact_count = d.pop("fact_count")

        def _parse_facts(data: object) -> list[AtomicFact] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                facts_type_0 = []
                _facts_type_0 = data
                for facts_type_0_item_data in (_facts_type_0):
                    facts_type_0_item = AtomicFact.from_dict(facts_type_0_item_data)



                    facts_type_0.append(facts_type_0_item)

                return facts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AtomicFact] | None, data)

        facts = _parse_facts(d.pop("facts"))


        first_fact_at = d.pop("first_fact_at")

        last_fact_at = d.pop("last_fact_at")

        session_id = d.pop("session_id")

        timeline_session = cls(
            fact_count=fact_count,
            facts=facts,
            first_fact_at=first_fact_at,
            last_fact_at=last_fact_at,
            session_id=session_id,
        )

        return timeline_session

