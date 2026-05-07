"""End-to-end verifier for the proactive-message webhook flow.

Spawns a local HTTP receiver, brings up an ngrok tunnel, registers a
project-scoped webhook against the public URL, schedules a wakeup,
fast-forwards simulated time via the workbench, then asserts that a
signed webhook delivery arrived and the HMAC matches.

Usage:
  export SONZAI_API_KEY=sk_...
  python verify_webhook_e2e.py [--agent-id AGENT_ID] [--event-type on_wakeup_ready]
                               [--public-url URL]   # skip ngrok if you have your own tunnel

Notes:
- A reachable public URL is required. This script will spawn `ngrok http <port>`
  unless --public-url is given. Install ngrok and run `ngrok config add-authtoken ...`
  once before running.
- If you don't pass --agent-id, the most recently created agent in your tenant
  is reused (no agent is created or deleted by this script).
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import http.server
import json
import os
import socket
import socketserver
import subprocess
import sys
import threading
import time
import urllib.request
import uuid
from queue import Empty, Queue
from typing import Any

from sonzai import Sonzai


def pick_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_receiver(port: int, q: "Queue[dict[str, Any]]") -> socketserver.TCPServer:
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length) if length else b""
            q.put(
                {
                    "path": self.path,
                    "headers": {k: v for k, v in self.headers.items()},
                    "body": body,
                }
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')

        def log_message(self, *_a: Any, **_k: Any) -> None:  # silence
            return

    httpd = socketserver.TCPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def start_ngrok(port: int) -> tuple[subprocess.Popen[bytes], str]:
    proc = subprocess.Popen(
        ["ngrok", "http", "--log=stdout", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + 15
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(
                "http://127.0.0.1:4040/api/tunnels", timeout=1
            ) as r:
                data = json.loads(r.read())
            for t in data.get("tunnels", []):
                if t.get("proto") == "https":
                    return proc, t["public_url"]
        except Exception:
            pass
        time.sleep(0.3)
    proc.terminate()
    raise RuntimeError("ngrok did not expose an https tunnel within 15s")


def verify_signature(secret: str, sig_header: str, raw_body: bytes) -> bool:
    # The server strips the "whsec_" prefix before HMAC-keying — see
    # services/platform/api/internal/infrastructure/webhook/signer.go::ExtractRawSecret.
    # Our key must match. Without this, every signature mismatches.
    raw_key = secret[len("whsec_"):] if secret.startswith("whsec_") else secret
    parts = dict(p.split("=", 1) for p in sig_header.split(",") if "=" in p)
    ts, v1 = parts.get("t"), parts.get("v1")
    if not ts or not v1:
        return False
    signed = f"{ts}.".encode() + raw_body
    mac = hmac.new(raw_key.encode(), signed, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, v1)


def pick_agent(client: Sonzai, agent_id: str | None) -> tuple[str, str]:
    """Return (agent_id, project_id). Reuses most recent agent if none given."""
    if agent_id:
        for a in client.agents.list(page_size=100).first_page():
            if a.agent_id == agent_id:
                if not a.project_id:
                    raise RuntimeError(f"Agent {agent_id} has no project_id")
                return a.agent_id, a.project_id
        raise RuntimeError(f"Agent {agent_id} not found in tenant")
    items = client.agents.list(page_size=10).first_page()
    if not items:
        raise RuntimeError(
            "No agents in tenant — create one first or pass --agent-id"
        )
    a = items[0]
    if not a.project_id:
        raise RuntimeError(f"Agent {a.agent_id} has no project_id")
    return a.agent_id, a.project_id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent-id", default=None)
    parser.add_argument("--event-type", default="on_wakeup_ready")
    parser.add_argument("--public-url", default=None,
                        help="Skip ngrok and use this public URL (must reach this machine).")
    parser.add_argument("--user-id", default=f"e2e-user-{uuid.uuid4().hex[:8]}")
    parser.add_argument("--delay-hours", type=int, default=0,
                        help="Wakeup delay. 0 (default) means 'fire on next cron tick' "
                             "(<=60s in production). Use a positive value to combine with "
                             "--simulated-hours for the workbench path.")
    parser.add_argument("--simulated-hours", type=float, default=0.0,
                        help="If > 0, advance simulated time after scheduling (workbench path). "
                             "Default 0 = skip advance_time entirely; rely on the production cron.")
    parser.add_argument("--wait-secs", type=int, default=120,
                        help="How long to wait for a webhook delivery after scheduling.")
    parser.add_argument("--keep-webhook", action="store_true",
                        help="Don't delete the webhook on exit.")
    args = parser.parse_args()

    if not os.environ.get("SONZAI_API_KEY"):
        print("ERROR: SONZAI_API_KEY not set", file=sys.stderr)
        return 2

    # Bump timeout — workbench.advance_time(25h) routinely takes 1–3 min on prod.
    client = Sonzai(timeout=300.0)
    print("Picking agent...")
    agent_id, project_id = pick_agent(client, args.agent_id)
    print(f"  agent_id={agent_id}\n  project_id={project_id}")

    port = pick_free_port()
    q: "Queue[dict[str, Any]]" = Queue()
    httpd = start_receiver(port, q)
    print(f"Local receiver listening on http://127.0.0.1:{port}")

    ngrok_proc: subprocess.Popen[bytes] | None = None
    if args.public_url:
        public_url = args.public_url.rstrip("/")
    else:
        print("Starting ngrok...")
        ngrok_proc, public_base = start_ngrok(port)
        public_url = public_base.rstrip("/")
        print(f"  tunnel: {public_url} -> 127.0.0.1:{port}")

    # Add a unique path so we can correlate.
    webhook_path = f"/sonzai/{uuid.uuid4().hex[:8]}"
    webhook_url = public_url + webhook_path

    secret: str | None = None
    try:
        print(f"Registering webhook for {args.event_type} -> {webhook_url}")
        reg = client.webhooks.register_for_project(
            project_id, args.event_type, webhook_url=webhook_url
        )
        secret = reg.signing_secret or None
        if not secret:
            # PUT may have updated an existing webhook; rotate to get a fresh secret.
            print("  no secret on register (existing webhook?), rotating...")
            secret = client.webhooks.rotate_secret_for_project(
                project_id, args.event_type
            ).signing_secret
        assert secret, "could not obtain signing_secret"
        print(f"  signing_secret prefix: {secret[:10]}…  len={len(secret)}")

        print(f"Scheduling wakeup (delay_hours={args.delay_hours})...")
        wakeup = client.agents.schedule_wakeup(
            agent_id,
            user_id=args.user_id,
            check_type="interest_followup",
            intent="e2e_webhook_verify",
            delay_hours=args.delay_hours,
        )
        wakeup_id = getattr(wakeup, "wakeup_id", None) or getattr(wakeup, "id", None)
        print(f"  wakeup_id={wakeup_id}")

        if args.simulated_hours > 0:
            print(f"Advancing time by {args.simulated_hours}h (synchronous)...")
            t0 = time.time()
            resp = client.workbench.advance_time(
                agent_id, args.user_id, simulated_hours=args.simulated_hours
            )
            elapsed = time.time() - t0
            days = getattr(resp, "days_processed", None)
            wakeups = getattr(resp, "wakeups_executed", None) or []
            print(f"  advance_time done in {elapsed:.1f}s | days_processed={days} | wakeups returned={len(wakeups)}")
        else:
            print("Skipping advance_time. Waiting for the production wakeup cron (every ~60s).")

        print(f"Waiting up to {args.wait_secs}s for webhook delivery...")
        deadline = time.time() + args.wait_secs
        delivered: list[dict[str, Any]] = []
        while time.time() < deadline:
            try:
                delivered.append(q.get(timeout=1.0))
                break
            except Empty:
                continue

        # Always show what the backend recorded — this works even if the receiver missed.
        print("\nBackend delivery attempts (most recent first):")
        try:
            attempts_page = client.webhooks.list_delivery_attempts_for_project(
                project_id, args.event_type, limit=5
            )
            attempts = attempts_page.first_page()
            for a in attempts[:5]:
                print(f"  [{a.created_at}] status={a.status} http={a.response_code} "
                      f"dur={a.duration_ms}ms attempt={a.attempt_number} "
                      f"err={a.error_message!r}")
        except Exception as err:
            print(f"  (could not list attempts: {err!r})")

        if not delivered:
            print("\nFAIL: no webhook hit the local receiver within the wait window.", file=sys.stderr)
            return 1

        for d in delivered:
            sig = d["headers"].get("Sonzai-Signature") or d["headers"].get("sonzai-signature")
            ok = bool(sig) and verify_signature(secret, sig, d["body"])
            print("\nReceived webhook:")
            print(f"  path: {d['path']}")
            print(f"  Sonzai-Signature: {sig}")
            print(f"  HMAC valid: {ok}")
            try:
                payload = json.loads(d["body"].decode())
                print(f"  payload keys: {list(payload.keys())}")
                print(f"  event_type: {payload.get('event_type')}")
                if "data" in payload:
                    keys = list(payload["data"].keys()) if isinstance(payload["data"], dict) else "(non-dict)"
                    print(f"  data keys: {keys}")
            except Exception:
                print(f"  body: {d['body'][:200]!r}")
            if not ok:
                print("FAIL: HMAC did not verify.", file=sys.stderr)
                return 1

        print("\nPASS: webhook delivered, HMAC verified.")
        return 0
    finally:
        if not args.keep_webhook and secret is not None:
            try:
                client.webhooks.delete_for_project(project_id, args.event_type)
                print("Cleaned up webhook subscription.")
            except Exception as err:
                print(f"(cleanup) delete failed: {err!r}")
        httpd.shutdown()
        if ngrok_proc is not None:
            ngrok_proc.terminate()
            try:
                ngrok_proc.wait(timeout=3)
            except Exception:
                ngrok_proc.kill()


if __name__ == "__main__":
    raise SystemExit(main())
