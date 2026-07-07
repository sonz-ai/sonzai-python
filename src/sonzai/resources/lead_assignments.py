"""Sonzai Lead Assignments resource.

The tenant-generic work-distribution primitive (any vertical — leads,
tickets, shifts): offer a unit of work to one rep from a candidate roster,
chosen by the named policy (``round_robin`` default, or ``load_balanced``).
At most one active assignment can exist per lead: offering a lead that
already has an active (offered/claimed) assignment returns the existing
assignment with ``deduplicated=True`` instead of creating a second one. The
offer expires after ``sla_seconds`` (platform default 900); the background
sweep then re-offers it to the next candidate who hasn't had it yet, or
expires it when the roster is exhausted.

Endpoints live under ``/api/v1/lead-assignments*``
(docs/design/rep-copilot-lead-distribution.md Tier 2.1).

These endpoints are not in the committed OpenAPI snapshot yet, so this
resource is fully hand-written (no ``_generated`` base class) — same posture
as the ``builtin_agents`` and ``ml`` resources. Mirrors the Go SDK's
``lead_assignments.go``.
"""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import LeadAssignment, ListLeadAssignmentsResult, OfferLeadAssignmentResult


def _offer_body(
    lead_ref: str,
    candidates: list[str],
    policy: str | None,
    features: dict[str, Any] | None,
    sla_seconds: int | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"lead_ref": lead_ref, "candidates": candidates}
    if policy is not None:
        body["policy"] = policy
    if features is not None:
        body["features"] = features
    if sla_seconds is not None:
        body["sla_seconds"] = sla_seconds
    return body


def _list_params(rep_user_id: str | None, state: str | None, limit: int | None) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if rep_user_id is not None:
        params["rep_user_id"] = rep_user_id
    if state is not None:
        params["state"] = state
    if limit is not None:
        params["limit"] = limit
    return params


class LeadAssignments:
    """Sync operations on the Lead Assignment service.

    Example::

        result = client.lead_assignments.offer(
            lead_ref="lead-123",
            candidates=["rep-1", "rep-2"],
        )
        if not result.deduplicated:
            print("offered to", result.assignment.rep_user_id)

        client.lead_assignments.claim(result.assignment.assignment_id)
    """

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def offer(
        self,
        *,
        lead_ref: str,
        candidates: list[str],
        policy: str | None = None,
        features: dict[str, Any] | None = None,
        sla_seconds: int | None = None,
    ) -> OfferLeadAssignmentResult:
        """Distribute a unit of work to one rep from the candidate roster.

        Args:
            lead_ref: Caller-owned external key for the unit of work (CRM
                lead id, ticket id, shift id, ...).
            candidates: Eligible rep user ids to distribute among.
            policy: Distribution policy: ``"round_robin"`` (default) or
                ``"load_balanced"``.
            features: Optional context/ML signals captured at offer time.
            sla_seconds: Offer window in seconds before re-offer to the next
                candidate (platform default 900).
        """
        data = self._http.post(
            "/api/v1/lead-assignments/offer",
            json_data=_offer_body(lead_ref, candidates, policy, features, sla_seconds),
        )
        return OfferLeadAssignmentResult.model_validate(data)

    def list(
        self,
        *,
        rep_user_id: str | None = None,
        state: str | None = None,
        limit: int | None = None,
    ) -> ListLeadAssignmentsResult:
        """List the project's assignment ledger rows, newest offer first.

        Args:
            rep_user_id: Only assignments offered to this rep.
            state: Only assignments in this state (offered, claimed, expired,
                reassigned, released, completed).
            limit: Max rows (platform default 50, max 200).
        """
        data = self._http.get(
            "/api/v1/lead-assignments",
            params=_list_params(rep_user_id, state, limit),
        )
        return ListLeadAssignmentsResult.model_validate(data)

    def get(self, assignment_id: str) -> LeadAssignment:
        """Read one lead assignment by id."""
        data = self._http.get(f"/api/v1/lead-assignments/{assignment_id}")
        return LeadAssignment.model_validate(data)

    def claim(self, assignment_id: str) -> LeadAssignment:
        """Claim an offered lead — the rep accepted the work before the SLA
        lapsed. Raises on 409 when the assignment is not in the offered state.
        """
        data = self._http.post(f"/api/v1/lead-assignments/{assignment_id}/claim")
        return LeadAssignment.model_validate(data)

    def release(self, assignment_id: str) -> LeadAssignment:
        """Release an offered or claimed lead back to the pool, freeing it to
        be offered again. Raises on 409 when the assignment is already
        terminal.
        """
        data = self._http.post(f"/api/v1/lead-assignments/{assignment_id}/release")
        return LeadAssignment.model_validate(data)

    def complete(self, assignment_id: str) -> LeadAssignment:
        """Mark a claimed lead completed. Raises on 409 when the assignment
        is not in the claimed state.
        """
        data = self._http.post(f"/api/v1/lead-assignments/{assignment_id}/complete")
        return LeadAssignment.model_validate(data)


class AsyncLeadAssignments:
    """Async operations on the Lead Assignment service.

    Mirror of :class:`LeadAssignments`; see that class for usage examples.
    """

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def offer(
        self,
        *,
        lead_ref: str,
        candidates: list[str],
        policy: str | None = None,
        features: dict[str, Any] | None = None,
        sla_seconds: int | None = None,
    ) -> OfferLeadAssignmentResult:
        """Distribute a unit of work to one rep from the candidate roster."""
        data = await self._http.post(
            "/api/v1/lead-assignments/offer",
            json_data=_offer_body(lead_ref, candidates, policy, features, sla_seconds),
        )
        return OfferLeadAssignmentResult.model_validate(data)

    async def list(
        self,
        *,
        rep_user_id: str | None = None,
        state: str | None = None,
        limit: int | None = None,
    ) -> ListLeadAssignmentsResult:
        """List the project's assignment ledger rows, newest offer first."""
        data = await self._http.get(
            "/api/v1/lead-assignments",
            params=_list_params(rep_user_id, state, limit),
        )
        return ListLeadAssignmentsResult.model_validate(data)

    async def get(self, assignment_id: str) -> LeadAssignment:
        """Read one lead assignment by id."""
        data = await self._http.get(f"/api/v1/lead-assignments/{assignment_id}")
        return LeadAssignment.model_validate(data)

    async def claim(self, assignment_id: str) -> LeadAssignment:
        """Claim an offered lead. Raises on 409 when not in the offered state."""
        data = await self._http.post(f"/api/v1/lead-assignments/{assignment_id}/claim")
        return LeadAssignment.model_validate(data)

    async def release(self, assignment_id: str) -> LeadAssignment:
        """Release an offered or claimed lead back to the pool."""
        data = await self._http.post(f"/api/v1/lead-assignments/{assignment_id}/release")
        return LeadAssignment.model_validate(data)

    async def complete(self, assignment_id: str) -> LeadAssignment:
        """Mark a claimed lead completed. Raises on 409 when not claimed."""
        data = await self._http.post(f"/api/v1/lead-assignments/{assignment_id}/complete")
        return LeadAssignment.model_validate(data)


__all__ = ["LeadAssignments", "AsyncLeadAssignments"]
