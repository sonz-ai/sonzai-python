"""Tests for the Sonzai client."""

import json

import httpx
import pytest
import respx

from sonzai import (
    AsyncSonzai,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    Sonzai,
)


@pytest.fixture
def base_url():
    return "https://api.test.sonz.ai"


@pytest.fixture
def client(base_url):
    c = Sonzai(api_key="test-key", base_url=base_url)
    yield c
    c.close()


@pytest.fixture
def async_client(base_url):
    return AsyncSonzai(api_key="test-key", base_url=base_url)


class TestClientInit:
    def test_requires_api_key(self):
        with pytest.raises(ValueError, match="api_key must be provided"):
            Sonzai()

    def test_accepts_api_key(self):
        client = Sonzai(api_key="test-key")
        assert client.agents is not None
        client.close()

    def test_env_var_api_key(self, monkeypatch):
        monkeypatch.setenv("SONZAI_API_KEY", "env-key")
        client = Sonzai()
        assert client.agents is not None
        client.close()

    def test_context_manager(self):
        with Sonzai(api_key="test-key") as client:
            assert client.agents is not None


class TestChat:
    @respx.mock
    def test_chat_sync(self, client, base_url):
        sse_body = (
            'data: {"choices":[{"delta":{"content":"Hello"},"finish_reason":null,"index":0}]}\n\n'
            'data: {"choices":[{"delta":{"content":" world"},"finish_reason":"stop","index":0}],'
            '"usage":{"promptTokens":10,"completionTokens":5,"totalTokens":15}}\n\n'
            "data: [DONE]\n\n"
        )
        respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=sse_body,
                headers={"content-type": "text/event-stream"},
            )
        )

        response = client.agents.chat(
            agent_id="agent-1",
            messages=[{"role": "user", "content": "Hi"}],
        )
        assert response.content == "Hello world"
        assert response.usage is not None
        assert response.usage.total_tokens == 15

    @respx.mock
    def test_chat_stream(self, client, base_url):
        sse_body = (
            'data: {"choices":[{"delta":{"content":"Hi"},"finish_reason":null,"index":0}]}\n\n'
            'data: {"choices":[{"delta":{"content":"!"},"finish_reason":"stop","index":0}]}\n\n'
            "data: [DONE]\n\n"
        )
        respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=sse_body,
                headers={"content-type": "text/event-stream"},
            )
        )

        events = list(
            client.agents.chat(
                agent_id="agent-1",
                messages=[{"role": "user", "content": "Hi"}],
                stream=True,
            )
        )
        assert len(events) == 2
        assert events[0].content == "Hi"
        assert events[1].content == "!"
        assert events[1].is_finished


class TestMemory:
    @respx.mock
    def test_list_memory(self, client, base_url):
        respx.get(f"{base_url}/api/v1/agents/agent-1/memory").mock(
            return_value=httpx.Response(
                200,
                json={
                    "nodes": [
                        {
                            "node_id": "n1",
                            "title": "Favorites",
                            "importance": 0.8,
                        }
                    ],
                    "contents": {},
                },
            )
        )

        result = client.agents.memory.list("agent-1")
        assert len(result.nodes) == 1
        assert result.nodes[0].node_id == "n1"
        assert result.nodes[0].title == "Favorites"

    @respx.mock
    def test_search_memory(self, client, base_url):
        respx.get(f"{base_url}/api/v1/agents/agent-1/memory/search").mock(
            return_value=httpx.Response(
                200,
                json={
                    "results": [
                        {
                            "fact_id": "f1",
                            "content": "Likes pizza",
                            "fact_type": "preference",
                            "score": 0.95,
                        }
                    ]
                },
            )
        )

        result = client.agents.memory.search("agent-1", query="food")
        assert len(result.results) == 1
        assert result.results[0].content == "Likes pizza"


class TestPersonality:
    @respx.mock
    def test_get_personality(self, client, base_url):
        respx.get(f"{base_url}/api/v1/agents/agent-1/personality").mock(
            return_value=httpx.Response(
                200,
                json={
                    "profile": {
                        "agent_id": "agent-1",
                        "name": "Luna",
                        "big5": {
                            "openness": {"score": 0.8, "percentile": 85},
                            "conscientiousness": {"score": 0.6, "percentile": 60},
                            "extraversion": {"score": 0.7, "percentile": 70},
                            "agreeableness": {"score": 0.9, "percentile": 95},
                            "neuroticism": {"score": 0.3, "percentile": 25},
                        },
                    },
                    "evolution": [],
                },
            )
        )

        result = client.agents.personality.get("agent-1")
        assert result.profile.name == "Luna"
        assert result.profile.big5.openness.score == 0.8


class TestSessions:
    @respx.mock
    def test_start_session(self, client, base_url):
        respx.post(f"{base_url}/api/v1/agents/agent-1/sessions/start").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        result = client.agents.sessions.start(
            "agent-1", user_id="user-1", session_id="sess-1"
        )
        assert result.success

    @respx.mock
    def test_end_session(self, client, base_url):
        respx.post(f"{base_url}/api/v1/agents/agent-1/sessions/end").mock(
            return_value=httpx.Response(200, json={"success": True})
        )

        result = client.agents.sessions.end(
            "agent-1",
            user_id="user-1",
            session_id="sess-1",
            total_messages=10,
            duration_seconds=300,
        )
        assert result.success


class TestInstances:
    @respx.mock
    def test_list_instances(self, client, base_url):
        respx.get(f"{base_url}/api/v1/agents/agent-1/instances").mock(
            return_value=httpx.Response(
                200,
                json={
                    "instances": [
                        {
                            "instance_id": "inst-1",
                            "agent_id": "agent-1",
                            "name": "Default",
                            "status": "active",
                            "is_default": True,
                        }
                    ]
                },
            )
        )

        result = client.agents.instances.list("agent-1")
        assert len(result.instances) == 1
        assert result.instances[0].name == "Default"

    @respx.mock
    def test_create_instance(self, client, base_url):
        respx.post(f"{base_url}/api/v1/agents/agent-1/instances").mock(
            return_value=httpx.Response(
                201,
                json={
                    "instance_id": "inst-2",
                    "agent_id": "agent-1",
                    "name": "Test",
                    "status": "active",
                    "is_default": False,
                },
            )
        )

        result = client.agents.instances.create("agent-1", name="Test")
        assert result.instance_id == "inst-2"
        assert result.name == "Test"


class TestNotifications:
    @respx.mock
    def test_list_notifications(self, client, base_url):
        respx.get(f"{base_url}/api/v1/agents/agent-1/notifications").mock(
            return_value=httpx.Response(
                200,
                json={
                    "notifications": [
                        {
                            "message_id": "msg-1",
                            "agent_id": "agent-1",
                            "generated_message": "Hey there!",
                            "status": "pending",
                        }
                    ]
                },
            )
        )

        result = client.agents.notifications.list("agent-1")
        assert len(result.notifications) == 1
        assert result.notifications[0].generated_message == "Hey there!"

    @respx.mock
    def test_consume_notification(self, client, base_url):
        respx.post(
            f"{base_url}/api/v1/agents/agent-1/notifications/msg-1/consume"
        ).mock(return_value=httpx.Response(200, json={"success": True}))

        result = client.agents.notifications.consume("agent-1", "msg-1")
        assert result.success


class TestEvalTemplates:
    @respx.mock
    def test_list_templates(self, client, base_url):
        respx.get(f"{base_url}/api/v1/eval-templates").mock(
            return_value=httpx.Response(
                200,
                json={
                    "templates": [
                        {
                            "id": "tpl-1",
                            "name": "Quality Check",
                            "scoring_rubric": "Be helpful",
                        }
                    ]
                },
            )
        )

        result = client.eval_templates.list()
        assert len(result.templates) == 1
        assert result.templates[0].name == "Quality Check"

    @respx.mock
    def test_create_template(self, client, base_url):
        respx.post(f"{base_url}/api/v1/eval-templates").mock(
            return_value=httpx.Response(
                201,
                json={
                    "id": "tpl-2",
                    "name": "New Template",
                    "scoring_rubric": "Score well",
                },
            )
        )

        result = client.eval_templates.create(
            name="New Template", scoring_rubric="Score well"
        )
        assert result.id == "tpl-2"


class TestEvalRuns:
    @respx.mock
    def test_list_runs(self, client, base_url):
        respx.get(f"{base_url}/api/v1/eval-runs").mock(
            return_value=httpx.Response(
                200,
                json={
                    "runs": [
                        {
                            "id": "run-1",
                            "agent_id": "agent-1",
                            "status": "completed",
                            "total_turns": 20,
                        }
                    ],
                    "total_count": 1,
                },
            )
        )

        result = client.eval_runs.list()
        assert len(result.runs) == 1
        assert result.runs[0].status == "completed"


class TestErrorHandling:
    @respx.mock
    def test_401_raises_auth_error(self, client, base_url):
        respx.get(f"{base_url}/api/v1/agents/agent-1/memory").mock(
            return_value=httpx.Response(401, json={"error": "Invalid API key"})
        )

        with pytest.raises(AuthenticationError):
            client.agents.memory.list("agent-1")

    @respx.mock
    def test_404_raises_not_found(self, client, base_url):
        respx.get(f"{base_url}/api/v1/agents/bad-id/personality").mock(
            return_value=httpx.Response(404, json={"error": "Agent not found"})
        )

        with pytest.raises(NotFoundError):
            client.agents.personality.get("bad-id")

    @respx.mock
    def test_400_raises_bad_request(self, client, base_url):
        respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                400, json={"error": "messages is required"}
            )
        )

        with pytest.raises(BadRequestError):
            client.agents.chat(agent_id="agent-1", messages=[])
