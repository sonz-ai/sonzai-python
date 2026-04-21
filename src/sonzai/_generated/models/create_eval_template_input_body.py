from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.eval_category import EvalCategory





T = TypeVar("T", bound="CreateEvalTemplateInputBody")



@_attrs_define
class CreateEvalTemplateInputBody:
    """ 
        Attributes:
            name (str): Template name
            schema (str | Unset): A URL to the JSON Schema for this object.
            categories (list[EvalCategory] | None | Unset): Evaluation categories
            description (str | Unset): Template description
            judge_model (str | Unset): Judge LLM model (default: gemini-3.1-pro-preview)
            max_tokens (int | Unset): Max tokens (default: 8192)
            scoring_rubric (str | Unset): Scoring rubric prompt
            temperature (float | Unset): Sampling temperature (default: 0.3)
            template_type (str | Unset): Template type (quality or adaptation)
     """

    name: str
    schema: str | Unset = UNSET
    categories: list[EvalCategory] | None | Unset = UNSET
    description: str | Unset = UNSET
    judge_model: str | Unset = UNSET
    max_tokens: int | Unset = UNSET
    scoring_rubric: str | Unset = UNSET
    temperature: float | Unset = UNSET
    template_type: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_category import EvalCategory
        name = self.name

        schema = self.schema

        categories: list[dict[str, Any]] | None | Unset
        if isinstance(self.categories, Unset):
            categories = UNSET
        elif isinstance(self.categories, list):
            categories = []
            for categories_type_0_item_data in self.categories:
                categories_type_0_item = categories_type_0_item_data.to_dict()
                categories.append(categories_type_0_item)


        else:
            categories = self.categories

        description = self.description

        judge_model = self.judge_model

        max_tokens = self.max_tokens

        scoring_rubric = self.scoring_rubric

        temperature = self.temperature

        template_type = self.template_type


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if categories is not UNSET:
            field_dict["categories"] = categories
        if description is not UNSET:
            field_dict["description"] = description
        if judge_model is not UNSET:
            field_dict["judge_model"] = judge_model
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if scoring_rubric is not UNSET:
            field_dict["scoring_rubric"] = scoring_rubric
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if template_type is not UNSET:
            field_dict["template_type"] = template_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_category import EvalCategory
        d = dict(src_dict)
        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        def _parse_categories(data: object) -> list[EvalCategory] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
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
            return cast(list[EvalCategory] | None | Unset, data)

        categories = _parse_categories(d.pop("categories", UNSET))


        description = d.pop("description", UNSET)

        judge_model = d.pop("judge_model", UNSET)

        max_tokens = d.pop("max_tokens", UNSET)

        scoring_rubric = d.pop("scoring_rubric", UNSET)

        temperature = d.pop("temperature", UNSET)

        template_type = d.pop("template_type", UNSET)

        create_eval_template_input_body = cls(
            name=name,
            schema=schema,
            categories=categories,
            description=description,
            judge_model=judge_model,
            max_tokens=max_tokens,
            scoring_rubric=scoring_rubric,
            temperature=temperature,
            template_type=template_type,
        )

        return create_eval_template_input_body

