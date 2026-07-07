"""Sonzai adapter-ingestion resource.

A customer-owned adapter (running in the customer's environment, e.g. a CRM
sidecar under app-runtime) normalizes its own events/contacts and POSTs them
here, so the platform's pipelines, lead-assignment ledger, and outbound
webhooks can react — without the platform ever holding CRM tables.

Endpoints live under ``/api/v1/ingest/*``
(docs/design/platform-deployment-tiers.md §8,
docs/design/rep-copilot-lead-distribution.md Tier 3.1).

These endpoints are not in the committed OpenAPI snapshot yet, so this
resource is fully hand-written (no ``_generated`` base class) — same posture
as the ``builtin_agents`` and ``ml`` resources. Mirrors the Go SDK's
``ingest.go``.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import IngestContact, IngestEventResult, ListIngestEventsResult

# DomainEvent v1 closed event-type enum (the `type` field of send_event).
INGEST_EVENT_LEAD_CREATED = "lead.created"
INGEST_EVENT_LEAD_UPDATED = "lead.updated"
INGEST_EVENT_LEAD_STAGE_CHANGED = "lead.stage_changed"
INGEST_EVENT_INVENTORY_UPDATED = "inventory.updated"
INGEST_EVENT_PRICE_CHANGED = "price.changed"
INGEST_EVENT_MESSAGE_RECEIVED = "message.received"
INGEST_EVENT_OUTCOME_RECORDED = "outcome.recorded"


def _event_body(
    event_id: str,
    type: str,
    occurred_at: datetime,
    lead_ref: str | None,
    contact_ref: str | None,
    payload: dict[str, Any] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "event_id": event_id,
        "type": type,
        "occurred_at": occurred_at.isoformat(),
    }
    if lead_ref is not None:
        body["lead_ref"] = lead_ref
    if contact_ref is not None:
        body["contact_ref"] = contact_ref
    if payload is not None:
        body["payload"] = payload
    return body


def _contact_body(
    contact_ref: str,
    kind: str,
    display_name: str | None,
    phone_e164: str | None,
    email: str | None,
    crm_owner_id: str | None,
    metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"contact_ref": contact_ref, "kind": kind}
    if display_name is not None:
        body["display_name"] = display_name
    if phone_e164 is not None:
        body["phone_e164"] = phone_e164
    if email is not None:
        body["email"] = email
    if crm_owner_id is not None:
        body["crm_owner_id"] = crm_owner_id
    if metadata is not None:
        body["metadata"] = metadata
    return body


def _list_events_params(since: datetime, limit: int | None, cursor: str | None) -> dict[str, Any]:
    params: dict[str, Any] = {"since": since.isoformat()}
    if limit is not None:
        params["limit"] = limit
    if cursor is not None:
        params["cursor"] = cursor
    return params


class Ingest:
    """Sync operations on the adapter-ingestion surface.

    Example::

        client.ingest.send_event(
            event_id="...",
            type=INGEST_EVENT_LEAD_CREATED,
            occurred_at=datetime.now(timezone.utc),
            lead_ref="sf-lead-001",
            payload={"source": "salesforce"},
        )
    """

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def send_event(
        self,
        *,
        event_id: str,
        type: str,
        occurred_at: datetime,
        lead_ref: str | None = None,
        contact_ref: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> IngestEventResult:
        """Store a normalized DomainEvent v1 and fan it out to the project's
        notification channels under the event's own type.

        Idempotent on ``event_id`` per project: replaying the same event_id
        is a no-op (``duplicate=True`` in the result, no fan-out).

        Args:
            event_id: Adapter-chosen idempotency key (UUID).
            type: One of the closed DomainEvent v1 types (see the
                ``INGEST_EVENT_*`` constants).
            occurred_at: When the event happened in the source system.
            lead_ref: Stable external lead identifier (CRM record id, ...).
            contact_ref: Stable external contact identifier.
            payload: Type-specific event body, stored verbatim.
        """
        data = self._http.post(
            "/api/v1/ingest/events",
            json_data=_event_body(event_id, type, occurred_at, lead_ref, contact_ref, payload),
        )
        return IngestEventResult.model_validate(data)

    def upsert_contact(
        self,
        *,
        contact_ref: str,
        kind: str,
        display_name: str | None = None,
        phone_e164: str | None = None,
        email: str | None = None,
        crm_owner_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> IngestContact:
        """Create or replace a contact/rep registry entry keyed by
        ``contact_ref`` within the project (last write wins).

        Args:
            contact_ref: Stable external identifier the adapter owns.
            kind: ``"rep"`` (the tenant's own salesperson) or
                ``"lead_contact"`` (an end customer).
            display_name: Human-readable name.
            phone_e164: E.164 phone number, e.g. ``+639171234567``.
            email: Contact email.
            crm_owner_id: CRM-side owner/user id (e.g. Salesforce OwnerId)
                for write-back routing.
            metadata: Free-form registry metadata (channel identities, desk,
                brand assignments, ...).
        """
        data = self._http.post(
            "/api/v1/ingest/contacts",
            json_data=_contact_body(
                contact_ref, kind, display_name, phone_e164, email, crm_owner_id, metadata
            ),
        )
        return IngestContact.model_validate(data)

    def list_events(
        self, *, since: datetime, limit: int | None = None, cursor: str | None = None
    ) -> ListIngestEventsResult:
        """Return a project's stored events in keyset order at/after
        ``since``, paged by ``cursor``.

        A read-only completeness/gap check for write-back adapters: webhook
        delivery is best-effort, so an adapter reconciles by listing
        platform-known events and re-applying any it has not yet synced.

        Args:
            since: Return events stored at/after this time.
            limit: Max events per page (platform default 200, max 1000).
            cursor: Opaque pagination token from a prior page's
                ``next_cursor``; when set it overrides ``since``.
        """
        data = self._http.get(
            "/api/v1/ingest/events", params=_list_events_params(since, limit, cursor)
        )
        return ListIngestEventsResult.model_validate(data)


class AsyncIngest:
    """Async operations on the adapter-ingestion surface.

    Mirror of :class:`Ingest`; see that class for usage examples.
    """

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def send_event(
        self,
        *,
        event_id: str,
        type: str,
        occurred_at: datetime,
        lead_ref: str | None = None,
        contact_ref: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> IngestEventResult:
        """Store a normalized DomainEvent v1 and fan it out to the project's
        notification channels under the event's own type."""
        data = await self._http.post(
            "/api/v1/ingest/events",
            json_data=_event_body(event_id, type, occurred_at, lead_ref, contact_ref, payload),
        )
        return IngestEventResult.model_validate(data)

    async def upsert_contact(
        self,
        *,
        contact_ref: str,
        kind: str,
        display_name: str | None = None,
        phone_e164: str | None = None,
        email: str | None = None,
        crm_owner_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> IngestContact:
        """Create or replace a contact/rep registry entry keyed by
        ``contact_ref`` within the project (last write wins)."""
        data = await self._http.post(
            "/api/v1/ingest/contacts",
            json_data=_contact_body(
                contact_ref, kind, display_name, phone_e164, email, crm_owner_id, metadata
            ),
        )
        return IngestContact.model_validate(data)

    async def list_events(
        self, *, since: datetime, limit: int | None = None, cursor: str | None = None
    ) -> ListIngestEventsResult:
        """Return a project's stored events in keyset order at/after
        ``since``, paged by ``cursor``."""
        data = await self._http.get(
            "/api/v1/ingest/events", params=_list_events_params(since, limit, cursor)
        )
        return ListIngestEventsResult.model_validate(data)


__all__ = [
    "INGEST_EVENT_LEAD_CREATED",
    "INGEST_EVENT_LEAD_UPDATED",
    "INGEST_EVENT_LEAD_STAGE_CHANGED",
    "INGEST_EVENT_INVENTORY_UPDATED",
    "INGEST_EVENT_PRICE_CHANGED",
    "INGEST_EVENT_MESSAGE_RECEIVED",
    "INGEST_EVENT_OUTCOME_RECORDED",
    "Ingest",
    "AsyncIngest",
]
