from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.eval_run import EvalRun





T = TypeVar("T", bound="ListEvalRunsOutputBody")



@_attrs_define
class ListEvalRunsOutputBody:
    """ 
        Attributes:
            runs (list[EvalRun] | None): List of eval runs
            total_count (int): Total number of matching runs
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    runs: list[EvalRun] | None
    total_count: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_run import EvalRun
        runs: list[dict[str, Any]] | None
        if isinstance(self.runs, list):
            runs = []
            for runs_type_0_item_data in self.runs:
                runs_type_0_item = runs_type_0_item_data.to_dict()
                runs.append(runs_type_0_item)


        else:
            runs = self.runs

        total_count = self.total_count

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runs": runs,
            "total_count": total_count,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_run import EvalRun
        d = dict(src_dict)
        def _parse_runs(data: object) -> list[EvalRun] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                runs_type_0 = []
                _runs_type_0 = data
                for runs_type_0_item_data in (_runs_type_0):
                    runs_type_0_item = EvalRun.from_dict(runs_type_0_item_data)



                    runs_type_0.append(runs_type_0_item)

                return runs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[EvalRun] | None, data)

        runs = _parse_runs(d.pop("runs"))


        total_count = d.pop("total_count")

        schema = d.pop("$schema", UNSET)

        list_eval_runs_output_body = cls(
            runs=runs,
            total_count=total_count,
            schema=schema,
        )

        return list_eval_runs_output_body

