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
  from ..models.eval_category import EvalCategory





T = TypeVar("T", bound="EvalTemplate")



@_attrs_define
class EvalTemplate:
    """ 
        Attributes:
            categories (list[EvalCategory] | None):
            created_at (datetime.datetime):
            description (str):
            is_system (bool):
            judge_model (str):
            max_tokens (int):
            name (str):
            scoring_rubric (str):
            temperature (float):
            template_id (str):
            template_type (str):
            updated_at (datetime.datetime):
            schema (str | Unset): A URL to the JSON Schema for this object.
            tenant_id (str | Unset):
     """

    categories: list[EvalCategory] | None
    created_at: datetime.datetime
    description: str
    is_system: bool
    judge_model: str
    max_tokens: int
    name: str
    scoring_rubric: str
    temperature: float
    template_id: str
    template_type: str
    updated_at: datetime.datetime
    schema: str | Unset = UNSET
    tenant_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_category import EvalCategory
        categories: list[dict[str, Any]] | None
        if isinstance(self.categories, list):
            categories = []
            for categories_type_0_item_data in self.categories:
                categories_type_0_item = categories_type_0_item_data.to_dict()
                categories.append(categories_type_0_item)


        else:
            categories = self.categories

        created_at = self.created_at.isoformat()

        description = self.description

        is_system = self.is_system

        judge_model = self.judge_model

        max_tokens = self.max_tokens

        name = self.name

        scoring_rubric = self.scoring_rubric

        temperature = self.temperature

        template_id = self.template_id

        template_type = self.template_type

        updated_at = self.updated_at.isoformat()

        schema = self.schema

        tenant_id = self.tenant_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "categories": categories,
            "created_at": created_at,
            "description": description,
            "is_system": is_system,
            "judge_model": judge_model,
            "max_tokens": max_tokens,
            "name": name,
            "scoring_rubric": scoring_rubric,
            "temperature": temperature,
            "template_id": template_id,
            "template_type": template_type,
            "updated_at": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_category import EvalCategory
        d = dict(src_dict)
        def _parse_categories(data: object) -> list[EvalCategory] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                categories_type_0 = []
                _categories_type_0 = data
                for categories_type_0_item_data in (_categories_type_0):
                    categories_type_0_item = EvalCategory.from_dict(categories_type_0_item_data)



                    categories_type_0.append(categories_type_0_item)

                return categories_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[EvalCategory] | None, data)

        categories = _parse_categories(d.pop("categories"))


        created_at = isoparse(d.pop("created_at"))




        description = d.pop("description")

        is_system = d.pop("is_system")

        judge_model = d.pop("judge_model")

        max_tokens = d.pop("max_tokens")

        name = d.pop("name")

        scoring_rubric = d.pop("scoring_rubric")

        temperature = d.pop("temperature")

        template_id = d.pop("template_id")

        template_type = d.pop("template_type")

        updated_at = isoparse(d.pop("updated_at"))




        schema = d.pop("$schema", UNSET)

        tenant_id = d.pop("tenant_id", UNSET)

        eval_template = cls(
            categories=categories,
            created_at=created_at,
            description=description,
            is_system=is_system,
            judge_model=judge_model,
            max_tokens=max_tokens,
            name=name,
            scoring_rubric=scoring_rubric,
            temperature=temperature,
            template_id=template_id,
            template_type=template_type,
            updated_at=updated_at,
            schema=schema,
            tenant_id=tenant_id,
        )

        return eval_template

