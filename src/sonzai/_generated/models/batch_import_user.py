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
  from ..models.prime_content_block import PrimeContentBlock
  from ..models.prime_fact import PrimeFact
  from ..models.prime_message import PrimeMessage
  from ..models.prime_user_metadata import PrimeUserMetadata





T = TypeVar("T", bound="BatchImportUser")



@_attrs_define
class BatchImportUser:
    """ 
        Attributes:
            user_id (str):
            content (list[PrimeContentBlock] | None | Unset):
            display_name (str | Unset):
            facts (list[PrimeFact] | None | Unset):
            first_met_at (datetime.datetime | Unset):
            messages (list[PrimeMessage] | None | Unset):
            metadata (PrimeUserMetadata | Unset):
     """

    user_id: str
    content: list[PrimeContentBlock] | None | Unset = UNSET
    display_name: str | Unset = UNSET
    facts: list[PrimeFact] | None | Unset = UNSET
    first_met_at: datetime.datetime | Unset = UNSET
    messages: list[PrimeMessage] | None | Unset = UNSET
    metadata: PrimeUserMetadata | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.prime_content_block import PrimeContentBlock
        from ..models.prime_fact import PrimeFact
        from ..models.prime_message import PrimeMessage
        from ..models.prime_user_metadata import PrimeUserMetadata
        user_id = self.user_id

        content: list[dict[str, Any]] | None | Unset
        if isinstance(self.content, Unset):
            content = UNSET
        elif isinstance(self.content, list):
            content = []
            for content_type_0_item_data in self.content:
                content_type_0_item = content_type_0_item_data.to_dict()
                content.append(content_type_0_item)


        else:
            content = self.content

        display_name = self.display_name

        facts: list[dict[str, Any]] | None | Unset
        if isinstance(self.facts, Unset):
            facts = UNSET
        elif isinstance(self.facts, list):
            facts = []
            for facts_type_0_item_data in self.facts:
                facts_type_0_item = facts_type_0_item_data.to_dict()
                facts.append(facts_type_0_item)


        else:
            facts = self.facts

        first_met_at: str | Unset = UNSET
        if not isinstance(self.first_met_at, Unset):
            first_met_at = self.first_met_at.isoformat()

        messages: list[dict[str, Any]] | None | Unset
        if isinstance(self.messages, Unset):
            messages = UNSET
        elif isinstance(self.messages, list):
            messages = []
            for messages_type_0_item_data in self.messages:
                messages_type_0_item = messages_type_0_item_data.to_dict()
                messages.append(messages_type_0_item)


        else:
            messages = self.messages

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "user_id": user_id,
        })
        if content is not UNSET:
            field_dict["content"] = content
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if facts is not UNSET:
            field_dict["facts"] = facts
        if first_met_at is not UNSET:
            field_dict["first_met_at"] = first_met_at
        if messages is not UNSET:
            field_dict["messages"] = messages
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.prime_content_block import PrimeContentBlock
        from ..models.prime_fact import PrimeFact
        from ..models.prime_message import PrimeMessage
        from ..models.prime_user_metadata import PrimeUserMetadata
        d = dict(src_dict)
        user_id = d.pop("user_id")

        def _parse_content(data: object) -> list[PrimeContentBlock] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_0 = []
                _content_type_0 = data
                for content_type_0_item_data in (_content_type_0):
                    content_type_0_item = PrimeContentBlock.from_dict(content_type_0_item_data)



                    content_type_0.append(content_type_0_item)

                return content_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PrimeContentBlock] | None | Unset, data)

        content = _parse_content(d.pop("content", UNSET))


        display_name = d.pop("display_name", UNSET)

        def _parse_facts(data: object) -> list[PrimeFact] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                facts_type_0 = []
                _facts_type_0 = data
                for facts_type_0_item_data in (_facts_type_0):
                    facts_type_0_item = PrimeFact.from_dict(facts_type_0_item_data)



                    facts_type_0.append(facts_type_0_item)

                return facts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PrimeFact] | None | Unset, data)

        facts = _parse_facts(d.pop("facts", UNSET))


        _first_met_at = d.pop("first_met_at", UNSET)
        first_met_at: datetime.datetime | Unset
        if isinstance(_first_met_at,  Unset):
            first_met_at = UNSET
        else:
            first_met_at = isoparse(_first_met_at)




        def _parse_messages(data: object) -> list[PrimeMessage] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                messages_type_0 = []
                _messages_type_0 = data
                for messages_type_0_item_data in (_messages_type_0):
                    messages_type_0_item = PrimeMessage.from_dict(messages_type_0_item_data)



                    messages_type_0.append(messages_type_0_item)

                return messages_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PrimeMessage] | None | Unset, data)

        messages = _parse_messages(d.pop("messages", UNSET))


        _metadata = d.pop("metadata", UNSET)
        metadata: PrimeUserMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = PrimeUserMetadata.from_dict(_metadata)




        batch_import_user = cls(
            user_id=user_id,
            content=content,
            display_name=display_name,
            facts=facts,
            first_met_at=first_met_at,
            messages=messages,
            metadata=metadata,
        )

        return batch_import_user

