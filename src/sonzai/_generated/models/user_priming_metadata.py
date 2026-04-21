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
  from ..models.user_priming_metadata_custom_fields import UserPrimingMetadataCustomFields





T = TypeVar("T", bound="UserPrimingMetadata")



@_attrs_define
class UserPrimingMetadata:
    """ 
        Attributes:
            agent_id (str):
            company (str):
            created_at (datetime.datetime):
            custom_fields (UserPrimingMetadataCustomFields):
            display_name (str):
            email (str):
            facts_count (int):
            first_met_at (datetime.datetime | None):
            linkedin_url (str):
            phone (str):
            primed_at (datetime.datetime):
            source_id (str):
            source_type (str):
            timezone (str):
            title (str):
            updated_at (datetime.datetime):
            user_id (str):
            warmth_score (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    agent_id: str
    company: str
    created_at: datetime.datetime
    custom_fields: UserPrimingMetadataCustomFields
    display_name: str
    email: str
    facts_count: int
    first_met_at: datetime.datetime | None
    linkedin_url: str
    phone: str
    primed_at: datetime.datetime
    source_id: str
    source_type: str
    timezone: str
    title: str
    updated_at: datetime.datetime
    user_id: str
    warmth_score: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.user_priming_metadata_custom_fields import UserPrimingMetadataCustomFields
        agent_id = self.agent_id

        company = self.company

        created_at = self.created_at.isoformat()

        custom_fields = self.custom_fields.to_dict()

        display_name = self.display_name

        email = self.email

        facts_count = self.facts_count

        first_met_at: None | str
        if isinstance(self.first_met_at, datetime.datetime):
            first_met_at = self.first_met_at.isoformat()
        else:
            first_met_at = self.first_met_at

        linkedin_url = self.linkedin_url

        phone = self.phone

        primed_at = self.primed_at.isoformat()

        source_id = self.source_id

        source_type = self.source_type

        timezone = self.timezone

        title = self.title

        updated_at = self.updated_at.isoformat()

        user_id = self.user_id

        warmth_score = self.warmth_score

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "AgentID": agent_id,
            "Company": company,
            "CreatedAt": created_at,
            "CustomFields": custom_fields,
            "DisplayName": display_name,
            "Email": email,
            "FactsCount": facts_count,
            "FirstMetAt": first_met_at,
            "LinkedinURL": linkedin_url,
            "Phone": phone,
            "PrimedAt": primed_at,
            "SourceID": source_id,
            "SourceType": source_type,
            "Timezone": timezone,
            "Title": title,
            "UpdatedAt": updated_at,
            "UserID": user_id,
            "WarmthScore": warmth_score,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_priming_metadata_custom_fields import UserPrimingMetadataCustomFields
        d = dict(src_dict)
        agent_id = d.pop("AgentID")

        company = d.pop("Company")

        created_at = isoparse(d.pop("CreatedAt"))




        custom_fields = UserPrimingMetadataCustomFields.from_dict(d.pop("CustomFields"))




        display_name = d.pop("DisplayName")

        email = d.pop("Email")

        facts_count = d.pop("FactsCount")

        def _parse_first_met_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_met_at_type_0 = isoparse(data)



                return first_met_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        first_met_at = _parse_first_met_at(d.pop("FirstMetAt"))


        linkedin_url = d.pop("LinkedinURL")

        phone = d.pop("Phone")

        primed_at = isoparse(d.pop("PrimedAt"))




        source_id = d.pop("SourceID")

        source_type = d.pop("SourceType")

        timezone = d.pop("Timezone")

        title = d.pop("Title")

        updated_at = isoparse(d.pop("UpdatedAt"))




        user_id = d.pop("UserID")

        warmth_score = d.pop("WarmthScore")

        schema = d.pop("$schema", UNSET)

        user_priming_metadata = cls(
            agent_id=agent_id,
            company=company,
            created_at=created_at,
            custom_fields=custom_fields,
            display_name=display_name,
            email=email,
            facts_count=facts_count,
            first_met_at=first_met_at,
            linkedin_url=linkedin_url,
            phone=phone,
            primed_at=primed_at,
            source_id=source_id,
            source_type=source_type,
            timezone=timezone,
            title=title,
            updated_at=updated_at,
            user_id=user_id,
            warmth_score=warmth_score,
            schema=schema,
        )

        return user_priming_metadata

