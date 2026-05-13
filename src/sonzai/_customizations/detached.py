"""Detached streaming helpers — Python port of sonzai-go's detached.go.

Background
----------
A queue worker (NATS / Watermill), an asyncio task with a short deadline, or
a short-lived HTTP request frequently needs to kick off a long-running AI
streaming call. The caller's lifetime (request handler, ack timeout, parent
asyncio task) is unrelated to — and almost always shorter than — the LLM
generation. If the caller's cancellation is allowed to propagate into the
chat call, the AI stream aborts mid-generation, the user sees an error, and
the Gemini / OpenAI quota burn was for nothing.

The Go SDK fixes this with ``ChatDetached`` / ``ChatStreamChannelDetached``
helpers that build a context via ``context.WithoutCancel(parent)`` and watch
for parent cancellation in a goroutine.

The Python equivalent is :func:`asyncio.shield` around the streaming
coroutine plus a background watchdog task that observes the *caller's* task
and emits a warning (or invokes :attr:`DetachOptions.on_parent_cancel`) if
the caller is cancelled while the detached call is still in flight.

Usage
-----

::

    async def handle_nats_message(msg):
        # The NATS handler's task will be cancelled when the message is
        # ack'd or the handler returns — but we want the AI call to run
        # to completion.
        resp = await client.agents.chat_detached(
            agent_id,
            messages=[...],
            timeout_seconds=300.0,
            on_parent_cancel=lambda exc: metrics.inc("detached.parent_cancelled"),
        )

The same helper exists for streaming::

    async for event in client.agents.chat_stream_detached(
        agent_id,
        messages=[...],
        timeout_seconds=300.0,
    ):
        ...

What "detached" guarantees
--------------------------

* The upstream HTTP call is wrapped in :func:`asyncio.shield`, so the
  caller's ``task.cancel()`` does *not* propagate into the call.
* The detached call still has an upper bound — :data:`DEFAULT_DETACHED_TIMEOUT_SECONDS`
  (300s) by default — applied *inside* the shielded coroutine via
  :func:`asyncio.wait_for`. This prevents leaked tasks if the upstream
  hangs forever.
* If the caller's task is cancelled while the detached call is still
  running, a watchdog logs a warning (or invokes
  :attr:`DetachOptions.on_parent_cancel`) so accidental misuse is caught
  during dev without aborting the in-flight request.

What it does NOT do
-------------------

* It does not retry. Failures from the upstream surface to the caller as
  ``await chat_detached(...)`` re-raising — unless the caller's task was
  cancelled, in which case the detached coroutine continues but its result
  is discarded.
* It does not magically make a sync ``chat`` call cancellable. Python sync
  blocking calls aren't interruptible by callers anyway — the detached
  helpers exist on the *async* API for asyncio task-cancellation, and the
  sync mirrors are provided only for surface parity.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)


# Upper bound applied to detached calls when DetachOptions.timeout_seconds is
# None. Mirrors the Go SDK's DefaultDetachedTimeout (5 minutes). AI generations
# rarely exceed a couple of minutes, but the 5-minute ceiling tolerates a slow
# LLM, a retrying upstream, or a long tool-use chain while still guaranteeing
# the call eventually returns instead of leaking a task.
DEFAULT_DETACHED_TIMEOUT_SECONDS: float = 300.0


@dataclass(frozen=True)
class DetachOptions:
    """Tunables for the ``*_detached`` chat variants.

    Mirror of sonzai-go's ``DetachOptions``. All fields are optional; the
    zero value (``DetachOptions()``) is valid and gives sensible defaults.

    Attributes:
        timeout_seconds: Hard cap on the detached call's wall-clock duration.
            ``None`` falls back to :data:`DEFAULT_DETACHED_TIMEOUT_SECONDS`
            (300s). Pass a negative or zero value to disable the timeout
            entirely — rarely what you want; prefer an explicit cap to
            guard against leaked tasks if the upstream hangs.

        logger: Logger used for the misuse warning when the parent task is
            cancelled mid-stream. Defaults to this module's logger so
            existing ``logging.getLogger("sonzai")`` configuration applies.

        on_parent_cancel: Optional callback invoked *instead of* the
            logging warning when the caller's task is cancelled while the
            detached call is still running. Useful for surfacing the
            condition to metrics / structured tracing rather than logs
            alone. The callback receives the
            :class:`asyncio.CancelledError` that caused the parent task to
            exit (or ``None`` if the parent was cancelled by some other
            mechanism). It must NOT raise — exceptions are caught and
            logged but do not affect the in-flight detached call.
    """

    timeout_seconds: float | None = None
    logger: logging.Logger | None = None
    on_parent_cancel: Callable[[BaseException | None], None] | None = None


def _resolve_timeout(timeout_seconds: float | None) -> float | None:
    """Apply the default if the caller didn't pick one.

    Returns ``None`` when the caller explicitly disables the timeout
    (negative or zero value). The streaming helpers translate ``None``
    into "no :func:`asyncio.wait_for` wrapper".
    """
    if timeout_seconds is None:
        return DEFAULT_DETACHED_TIMEOUT_SECONDS
    if timeout_seconds <= 0:
        return None
    return timeout_seconds


def _resolve_logger(opt_logger: logging.Logger | None) -> logging.Logger:
    return opt_logger if opt_logger is not None else logger


def _emit_parent_cancel_warning(
    log: logging.Logger,
    cb: Callable[[BaseException | None], None] | None,
    parent_exc: BaseException | None,
    timeout_seconds: float | None,
) -> None:
    """Surface a parent-cancelled-mid-stream condition.

    Prefers the user-supplied callback over the log warning. Callback
    exceptions are caught and logged so a buggy metric hook can't poison
    the detached call.
    """
    if cb is not None:
        try:
            cb(parent_exc)
        except Exception:  # pragma: no cover — defensive
            log.exception("on_parent_cancel callback raised; ignoring")
        return

    log.warning(
        "sonzai: parent task cancelled during detached streaming call; "
        "call continues until completion or detached timeout — "
        "this usually indicates the wrong helper is being used "
        "(use the cancellation-honoring variant when the caller's "
        "lifetime exceeds the generation). parent_exc=%r timeout=%s",
        parent_exc,
        timeout_seconds,
    )


async def _watch_parent_task(
    parent: asyncio.Task[object],
    done_event: asyncio.Event,
    log: logging.Logger,
    cb: Callable[[BaseException | None], None] | None,
    timeout_seconds: float | None,
) -> None:
    """Run alongside the detached call.

    Exits cleanly when the call finishes (``done_event`` set). If the
    parent task is cancelled or otherwise completes before the detached
    call returns, emit the misuse warning / callback exactly once.
    """
    done_task = asyncio.ensure_future(done_event.wait())
    # asyncio.wait accepts the Task[object] directly; type checkers see the
    # set as heterogeneous but the runtime cost is identical.
    try:
        finished, _ = await asyncio.wait(
            {done_task, parent},
            return_when=asyncio.FIRST_COMPLETED,
        )
    finally:
        if not done_task.done():
            done_task.cancel()

    if done_task in finished:
        # Detached call finished first — nothing to warn about.
        return

    # Parent finished/cancelled while the detached call is still running.
    parent_exc: BaseException | None = None
    try:
        # parent.exception() raises CancelledError if the task was
        # cancelled, otherwise returns the exception (or None on success).
        if parent.cancelled():
            parent_exc = asyncio.CancelledError(
                "caller task cancelled during detached chat call"
            )
        else:
            parent_exc = parent.exception()
    except (asyncio.CancelledError, asyncio.InvalidStateError):
        # InvalidStateError shouldn't happen — `parent` is in `finished`.
        parent_exc = None

    _emit_parent_cancel_warning(log, cb, parent_exc, timeout_seconds)


def _current_task_or_none() -> asyncio.Task[object] | None:
    """Best-effort lookup of the calling task.

    Used by the watchdog so we don't blow up when invoked outside an
    asyncio task (e.g. tests calling the helper from a plain coroutine
    via ``asyncio.run``). When ``None``, the watchdog is skipped — the
    shielding still works, only the misuse warning is silenced.
    """
    try:
        return asyncio.current_task()
    except RuntimeError:
        return None


__all__ = [
    "DEFAULT_DETACHED_TIMEOUT_SECONDS",
    "DetachOptions",
    "_current_task_or_none",
    "_emit_parent_cancel_warning",
    "_resolve_logger",
    "_resolve_timeout",
    "_watch_parent_task",
]
