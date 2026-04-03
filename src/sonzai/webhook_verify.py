"""Webhook signature verification for the Sonzai SDK.

Use ``verify_webhook_signature`` in your webhook handler to authenticate
incoming Sonzai webhook requests:

    from sonzai import verify_webhook_signature, WebhookVerificationError

    @app.post("/webhook")
    def handle_webhook(request: Request):
        body = request.body()
        sig = request.headers.get("Sonzai-Signature", "")
        try:
            verify_webhook_signature(body, sig, WEBHOOK_SECRET)
        except WebhookVerificationError:
            return Response(status_code=401)
        ...
"""

from __future__ import annotations

import hashlib
import hmac
import time

__all__ = [
    "WebhookVerificationError",
    "verify_webhook_signature",
    "verify_webhook_signature_with_tolerance",
]

_WEBHOOK_SECRET_PREFIX = "whsec_"
_DEFAULT_TIMESTAMP_TOLERANCE = 300  # 5 minutes in seconds


class WebhookVerificationError(Exception):
    """Raised when a webhook signature cannot be verified."""


def verify_webhook_signature(
    payload: bytes,
    sig_header: str,
    secret: str,
) -> None:
    """Verify a Sonzai webhook payload signature.

    Uses the default timestamp tolerance of 5 minutes.

    Args:
        payload: The raw request body bytes.
        sig_header: The value of the ``Sonzai-Signature`` request header.
        secret: Your webhook signing secret (``whsec_...``).

    Raises:
        WebhookVerificationError: If the signature is missing, expired, or invalid.
    """
    verify_webhook_signature_with_tolerance(
        payload, sig_header, secret, _DEFAULT_TIMESTAMP_TOLERANCE
    )


def verify_webhook_signature_with_tolerance(
    payload: bytes,
    sig_header: str,
    secret: str,
    tolerance: int,
) -> None:
    """Verify a Sonzai webhook payload signature with a custom timestamp tolerance.

    Args:
        payload: The raw request body bytes.
        sig_header: The value of the ``Sonzai-Signature`` request header.
        secret: Your webhook signing secret (``whsec_...``).
        tolerance: Maximum allowed age of the signature in seconds.
            Pass ``0`` to skip timestamp checking.

    Raises:
        WebhookVerificationError: If the signature is missing, expired, or invalid.
    """
    if not secret:
        raise WebhookVerificationError("invalid or empty webhook secret")
    if not sig_header:
        raise WebhookVerificationError("missing or empty signature header")

    # Strip the whsec_ prefix to get the raw signing key.
    signing_key = secret
    if secret.startswith(_WEBHOOK_SECRET_PREFIX):
        signing_key = secret[len(_WEBHOOK_SECRET_PREFIX):]
    if not signing_key:
        raise WebhookVerificationError("invalid or empty webhook secret")

    # Parse "t={timestamp},v1={sig1},v1={sig2},..."
    timestamp, signatures = _parse_signature_header(sig_header)

    if not signatures:
        raise WebhookVerificationError("missing or empty signature header")

    # Check timestamp tolerance.
    if tolerance > 0:
        age = abs(time.time() - timestamp)
        if age > tolerance:
            raise WebhookVerificationError("webhook timestamp is outside tolerance")

    # Compute expected HMAC-SHA256("{timestamp}.{payload}")
    signed_payload = f"{timestamp}.".encode() + payload
    expected = hmac.new(
        signing_key.encode(), signed_payload, hashlib.sha256
    ).hexdigest()

    # Accept if any of the provided signatures match (supports secret rotation).
    for sig in signatures:
        if hmac.compare_digest(sig, expected):
            return

    raise WebhookVerificationError("webhook signature is invalid")


def _parse_signature_header(header: str) -> tuple[int, list[str]]:
    """Parse ``t={ts},v1={sig1},v1={sig2}`` into (timestamp, [signatures])."""
    timestamp = 0
    signatures: list[str] = []

    for part in header.split(","):
        part = part.strip()
        if part.startswith("t="):
            try:
                timestamp = int(part[2:])
            except ValueError as exc:
                raise WebhookVerificationError(
                    f"invalid timestamp in signature header: {part!r}"
                ) from exc
        elif part.startswith("v1="):
            sig = part[3:]
            if sig:
                signatures.append(sig)

    if timestamp == 0:
        raise WebhookVerificationError("missing timestamp in signature header")

    return timestamp, signatures
