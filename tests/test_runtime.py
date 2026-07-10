"""Runtime control-plane and cross-language metering contract tests."""

from __future__ import annotations

import json

import httpx
import respx

from sonzai import (
    AsyncSonzai,
    RuntimeUsageCounter,
    RuntimeUsageReport,
    Sonzai,
    canonical_runtime_usage_report,
    sign_runtime_usage_report,
)

BASE_URL = "https://api.test.sonz.ai"


def usage_report() -> RuntimeUsageReport:
    return RuntimeUsageReport(
        report_id="r1",
        tenant_id="t1",
        instance_id="i1",
        period_start="2026-07-10T08:00:00.000000123Z",
        period_end="2026-07-10T08:01:00.000000123Z",
        heartbeat_at="2026-07-10T08:01:00.000000123Z",
        counters=[
            RuntimeUsageCounter(
                project_id="p1",
                agent_id="a1",
                provider="openrouter",
                model="m1",
                use_case="chat",
                billing_mode="byok",
                tokens_in=10,
                tokens_out=20,
                cache_read_tokens=3,
                turns=1,
            ),
            RuntimeUsageCounter(
                project_id="p1",
                agent_id="a2",
                provider="gemini",
                model="m2",
                use_case="chat",
                billing_mode="standard",
                tokens_in=30,
                tokens_out=40,
                cache_creation_tokens=2,
                turns=1,
            ),
        ],
    )


@respx.mock
def test_runtime_context_bundle_uses_control_plane_not_chat() -> None:
    route = respx.post(f"{BASE_URL}/api/v1/agents/agent%2Fone/context-bundle").mock(
        return_value=httpx.Response(
            200,
            json={
                "system_prompt_parts": ["system"],
                "memory_context": {},
                "tool_definitions": [],
                "ttl": 300,
            },
        )
    )
    with Sonzai(api_key="test-key", base_url=BASE_URL) as client:
        result = client.runtime.context_bundle(
            "agent/one", user_id="u1", session_id="s1", current_message="hello"
        )
    assert result.ttl == 300
    assert json.loads(route.calls.last.request.content) == {
        "user_id": "u1",
        "session_id": "s1",
        "current_message": "hello",
    }


def test_runtime_usage_signature_matches_shared_vector() -> None:
    report = usage_report()
    assert sign_runtime_usage_report(report, "secret") == (
        "4d209106751b9768c4e8afe82c544fbdfc43b83c3bb9fb42e79bb81765301308"
    )
    report.counters.reverse()
    assert sign_runtime_usage_report(report, "secret") == (
        "4d209106751b9768c4e8afe82c544fbdfc43b83c3bb9fb42e79bb81765301308"
    )
    assert canonical_runtime_usage_report(report).startswith("2\nr1\nt1\ni1\n")


@respx.mock
def test_runtime_backend_agent_artifacts_are_configuration_only() -> None:
    respx.get(f"{BASE_URL}/api/v1/runtime/backend-agent-artifacts").mock(
        return_value=httpx.Response(
            200,
            json={
                "artifacts": [
                    {
                        "slug": "lead_score",
                        "name": "Lead score",
                        "description": "Scores locally",
                        "model_hint": "claude",
                        "system": "score locally",
                        "disable_tools": True,
                        "max_tool_rounds": 0,
                        "version": "v1",
                    }
                ]
            },
        )
    )
    with Sonzai(api_key="test-key", base_url=BASE_URL) as client:
        artifacts = client.runtime.backend_agent_artifacts()
    assert artifacts[0].slug == "lead_score"


@respx.mock
def test_runtime_submit_usage_mirrors_signature_header() -> None:
    report = usage_report()
    report.signature = sign_runtime_usage_report(report, "secret")
    route = respx.post(f"{BASE_URL}/api/v1/usage/reports").mock(
        return_value=httpx.Response(202, json={"accepted": True, "report_id": "r1"})
    )
    with Sonzai(api_key="test-key", base_url=BASE_URL) as client:
        result = client.runtime.submit_usage_report(report)
    assert result.accepted
    assert route.calls.last.request.headers["X-Sonzai-Metering-Signature"] == report.signature


@respx.mock
def test_generic_request_exposes_future_platform_operations() -> None:
    respx.get(f"{BASE_URL}/api/v1/future-capability").mock(
        return_value=httpx.Response(200, json={"available": True})
    )
    with Sonzai(api_key="test-key", base_url=BASE_URL) as client:
        assert client.request("GET", "/api/v1/future-capability") == {"available": True}


@respx.mock
async def test_async_runtime_resource_is_wired() -> None:
    respx.get(f"{BASE_URL}/api/v1/future-capability").mock(
        return_value=httpx.Response(200, json={"available": True})
    )
    client = AsyncSonzai(api_key="test-key", base_url=BASE_URL)
    try:
        assert await client.request("GET", "/api/v1/future-capability") == {"available": True}
        assert client.runtime is not None
    finally:
        await client.close()
