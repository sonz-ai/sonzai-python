from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.advance_time_diary_entry import AdvanceTimeDiaryEntry
  from ..models.advance_time_wakeup import AdvanceTimeWakeup





T = TypeVar("T", bound="WorkbenchAdvanceTimeResponse")



@_attrs_define
class WorkbenchAdvanceTimeResponse:
    """ 
        Attributes:
            consolidation_processed (int):
            consolidation_ran (bool):
            days_processed (int):
            diary_entries_created (int):
            wakeups_executed (list[AdvanceTimeWakeup] | None):
            weekly_consolidations (int):
            diary_entries (list[AdvanceTimeDiaryEntry] | None | Unset):
     """

    consolidation_processed: int
    consolidation_ran: bool
    days_processed: int
    diary_entries_created: int
    wakeups_executed: list[AdvanceTimeWakeup] | None
    weekly_consolidations: int
    diary_entries: list[AdvanceTimeDiaryEntry] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.advance_time_diary_entry import AdvanceTimeDiaryEntry
        from ..models.advance_time_wakeup import AdvanceTimeWakeup
        consolidation_processed = self.consolidation_processed

        consolidation_ran = self.consolidation_ran

        days_processed = self.days_processed

        diary_entries_created = self.diary_entries_created

        wakeups_executed: list[dict[str, Any]] | None
        if isinstance(self.wakeups_executed, list):
            wakeups_executed = []
            for wakeups_executed_type_0_item_data in self.wakeups_executed:
                wakeups_executed_type_0_item = wakeups_executed_type_0_item_data.to_dict()
                wakeups_executed.append(wakeups_executed_type_0_item)


        else:
            wakeups_executed = self.wakeups_executed

        weekly_consolidations = self.weekly_consolidations

        diary_entries: list[dict[str, Any]] | None | Unset
        if isinstance(self.diary_entries, Unset):
            diary_entries = UNSET
        elif isinstance(self.diary_entries, list):
            diary_entries = []
            for diary_entries_type_0_item_data in self.diary_entries:
                diary_entries_type_0_item = diary_entries_type_0_item_data.to_dict()
                diary_entries.append(diary_entries_type_0_item)


        else:
            diary_entries = self.diary_entries


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "consolidation_processed": consolidation_processed,
            "consolidation_ran": consolidation_ran,
            "days_processed": days_processed,
            "diary_entries_created": diary_entries_created,
            "wakeups_executed": wakeups_executed,
            "weekly_consolidations": weekly_consolidations,
        })
        if diary_entries is not UNSET:
            field_dict["diary_entries"] = diary_entries

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advance_time_diary_entry import AdvanceTimeDiaryEntry
        from ..models.advance_time_wakeup import AdvanceTimeWakeup
        d = dict(src_dict)
        consolidation_processed = d.pop("consolidation_processed")

        consolidation_ran = d.pop("consolidation_ran")

        days_processed = d.pop("days_processed")

        diary_entries_created = d.pop("diary_entries_created")

        def _parse_wakeups_executed(data: object) -> list[AdvanceTimeWakeup] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                wakeups_executed_type_0 = []
                _wakeups_executed_type_0 = data
                for wakeups_executed_type_0_item_data in (_wakeups_executed_type_0):
                    wakeups_executed_type_0_item = AdvanceTimeWakeup.from_dict(wakeups_executed_type_0_item_data)



                    wakeups_executed_type_0.append(wakeups_executed_type_0_item)

                return wakeups_executed_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AdvanceTimeWakeup] | None, data)

        wakeups_executed = _parse_wakeups_executed(d.pop("wakeups_executed"))


        weekly_consolidations = d.pop("weekly_consolidations")

        def _parse_diary_entries(data: object) -> list[AdvanceTimeDiaryEntry] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                diary_entries_type_0 = []
                _diary_entries_type_0 = data
                for diary_entries_type_0_item_data in (_diary_entries_type_0):
                    diary_entries_type_0_item = AdvanceTimeDiaryEntry.from_dict(diary_entries_type_0_item_data)



                    diary_entries_type_0.append(diary_entries_type_0_item)

                return diary_entries_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AdvanceTimeDiaryEntry] | None | Unset, data)

        diary_entries = _parse_diary_entries(d.pop("diary_entries", UNSET))


        workbench_advance_time_response = cls(
            consolidation_processed=consolidation_processed,
            consolidation_ran=consolidation_ran,
            days_processed=days_processed,
            diary_entries_created=diary_entries_created,
            wakeups_executed=wakeups_executed,
            weekly_consolidations=weekly_consolidations,
            diary_entries=diary_entries,
        )

        return workbench_advance_time_response

