from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.cost_by_character import CostByCharacter
  from ..models.cost_by_project import CostByProject
  from ..models.cost_by_service import CostByService
  from ..models.cost_by_traffic_source import CostByTrafficSource
  from ..models.cost_daily_entry import CostDailyEntry
  from ..models.cost_response_period_struct import CostResponsePeriodStruct
  from ..models.cost_summary import CostSummary





T = TypeVar("T", bound="CostResponse")



@_attrs_define
class CostResponse:
    """ 
        Attributes:
            daily (list[CostDailyEntry] | None):
            period (CostResponsePeriodStruct):
            summary (CostSummary):
            schema (str | Unset): A URL to the JSON Schema for this object.
            by_character (list[CostByCharacter] | None | Unset):
            by_project (list[CostByProject] | None | Unset):
            by_service (list[CostByService] | None | Unset):
            by_traffic_source (list[CostByTrafficSource] | None | Unset):
     """

    daily: list[CostDailyEntry] | None
    period: CostResponsePeriodStruct
    summary: CostSummary
    schema: str | Unset = UNSET
    by_character: list[CostByCharacter] | None | Unset = UNSET
    by_project: list[CostByProject] | None | Unset = UNSET
    by_service: list[CostByService] | None | Unset = UNSET
    by_traffic_source: list[CostByTrafficSource] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.cost_by_character import CostByCharacter
        from ..models.cost_by_project import CostByProject
        from ..models.cost_by_service import CostByService
        from ..models.cost_by_traffic_source import CostByTrafficSource
        from ..models.cost_daily_entry import CostDailyEntry
        from ..models.cost_response_period_struct import CostResponsePeriodStruct
        from ..models.cost_summary import CostSummary
        daily: list[dict[str, Any]] | None
        if isinstance(self.daily, list):
            daily = []
            for daily_type_0_item_data in self.daily:
                daily_type_0_item = daily_type_0_item_data.to_dict()
                daily.append(daily_type_0_item)


        else:
            daily = self.daily

        period = self.period.to_dict()

        summary = self.summary.to_dict()

        schema = self.schema

        by_character: list[dict[str, Any]] | None | Unset
        if isinstance(self.by_character, Unset):
            by_character = UNSET
        elif isinstance(self.by_character, list):
            by_character = []
            for by_character_type_0_item_data in self.by_character:
                by_character_type_0_item = by_character_type_0_item_data.to_dict()
                by_character.append(by_character_type_0_item)


        else:
            by_character = self.by_character

        by_project: list[dict[str, Any]] | None | Unset
        if isinstance(self.by_project, Unset):
            by_project = UNSET
        elif isinstance(self.by_project, list):
            by_project = []
            for by_project_type_0_item_data in self.by_project:
                by_project_type_0_item = by_project_type_0_item_data.to_dict()
                by_project.append(by_project_type_0_item)


        else:
            by_project = self.by_project

        by_service: list[dict[str, Any]] | None | Unset
        if isinstance(self.by_service, Unset):
            by_service = UNSET
        elif isinstance(self.by_service, list):
            by_service = []
            for by_service_type_0_item_data in self.by_service:
                by_service_type_0_item = by_service_type_0_item_data.to_dict()
                by_service.append(by_service_type_0_item)


        else:
            by_service = self.by_service

        by_traffic_source: list[dict[str, Any]] | None | Unset
        if isinstance(self.by_traffic_source, Unset):
            by_traffic_source = UNSET
        elif isinstance(self.by_traffic_source, list):
            by_traffic_source = []
            for by_traffic_source_type_0_item_data in self.by_traffic_source:
                by_traffic_source_type_0_item = by_traffic_source_type_0_item_data.to_dict()
                by_traffic_source.append(by_traffic_source_type_0_item)


        else:
            by_traffic_source = self.by_traffic_source


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "daily": daily,
            "period": period,
            "summary": summary,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if by_character is not UNSET:
            field_dict["byCharacter"] = by_character
        if by_project is not UNSET:
            field_dict["byProject"] = by_project
        if by_service is not UNSET:
            field_dict["byService"] = by_service
        if by_traffic_source is not UNSET:
            field_dict["byTrafficSource"] = by_traffic_source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cost_by_character import CostByCharacter
        from ..models.cost_by_project import CostByProject
        from ..models.cost_by_service import CostByService
        from ..models.cost_by_traffic_source import CostByTrafficSource
        from ..models.cost_daily_entry import CostDailyEntry
        from ..models.cost_response_period_struct import CostResponsePeriodStruct
        from ..models.cost_summary import CostSummary
        d = dict(src_dict)
        def _parse_daily(data: object) -> list[CostDailyEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                daily_type_0 = []
                _daily_type_0 = data
                for daily_type_0_item_data in (_daily_type_0):
                    daily_type_0_item = CostDailyEntry.from_dict(daily_type_0_item_data)



                    daily_type_0.append(daily_type_0_item)

                return daily_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CostDailyEntry] | None, data)

        daily = _parse_daily(d.pop("daily"))


        period = CostResponsePeriodStruct.from_dict(d.pop("period"))




        summary = CostSummary.from_dict(d.pop("summary"))




        schema = d.pop("$schema", UNSET)

        def _parse_by_character(data: object) -> list[CostByCharacter] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_character_type_0 = []
                _by_character_type_0 = data
                for by_character_type_0_item_data in (_by_character_type_0):
                    by_character_type_0_item = CostByCharacter.from_dict(by_character_type_0_item_data)



                    by_character_type_0.append(by_character_type_0_item)

                return by_character_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CostByCharacter] | None | Unset, data)

        by_character = _parse_by_character(d.pop("byCharacter", UNSET))


        def _parse_by_project(data: object) -> list[CostByProject] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_project_type_0 = []
                _by_project_type_0 = data
                for by_project_type_0_item_data in (_by_project_type_0):
                    by_project_type_0_item = CostByProject.from_dict(by_project_type_0_item_data)



                    by_project_type_0.append(by_project_type_0_item)

                return by_project_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CostByProject] | None | Unset, data)

        by_project = _parse_by_project(d.pop("byProject", UNSET))


        def _parse_by_service(data: object) -> list[CostByService] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_service_type_0 = []
                _by_service_type_0 = data
                for by_service_type_0_item_data in (_by_service_type_0):
                    by_service_type_0_item = CostByService.from_dict(by_service_type_0_item_data)



                    by_service_type_0.append(by_service_type_0_item)

                return by_service_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CostByService] | None | Unset, data)

        by_service = _parse_by_service(d.pop("byService", UNSET))


        def _parse_by_traffic_source(data: object) -> list[CostByTrafficSource] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_traffic_source_type_0 = []
                _by_traffic_source_type_0 = data
                for by_traffic_source_type_0_item_data in (_by_traffic_source_type_0):
                    by_traffic_source_type_0_item = CostByTrafficSource.from_dict(by_traffic_source_type_0_item_data)



                    by_traffic_source_type_0.append(by_traffic_source_type_0_item)

                return by_traffic_source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CostByTrafficSource] | None | Unset, data)

        by_traffic_source = _parse_by_traffic_source(d.pop("byTrafficSource", UNSET))


        cost_response = cls(
            daily=daily,
            period=period,
            summary=summary,
            schema=schema,
            by_character=by_character,
            by_project=by_project,
            by_service=by_service,
            by_traffic_source=by_traffic_source,
        )

        return cost_response

