from __future__ import annotations

import unittest
from unittest.mock import patch

from backend.helpers.service_classifier import Ambiguous, ClassifiedService
from backend.helpers.tool_selector import ResolvedTool
from backend.main import app
from fastapi.testclient import TestClient


class ChatEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_chat_endpoint_exists_and_accepts_messages(self) -> None:
        response = self.client.post(
            "/chat",
            json={"messages": [{"role": "user", "content": "hi"}]},
        )
        self.assertNotEqual(
            response.status_code, 404, "POST /chat should be registered"
        )
        self.assertNotEqual(
            response.status_code, 422, "POST /chat should accept the documented schema"
        )

    def test_chat_endpoint_rejects_malformed_payload(self) -> None:
        response = self.client.post("/chat", json={"messages": "nope"})
        self.assertEqual(response.status_code, 422)

    def test_slack_send_error_recovers_with_lookup_follow_up(self) -> None:
        with (
            patch(
                "backend.solution.classify_service",
                return_value=ClassifiedService(service="slack"),
            ),
            patch(
                "backend.solution.resolve_tool_for_service",
                return_value=ResolvedTool(
                    name="slack_send_message",
                    arguments={
                        "channel": "@avery",
                        "text": "Notification about the Linear issue.",
                    },
                ),
            ),
            patch(
                "backend.solution.resolve_follow_up_tool_with_llm",
                side_effect=[ResolvedTool(name="slack_list_users", arguments={}), None],
            ),
        ):
            response = self.client.post(
                "/chat",
                json={
                    "messages": [
                        {
                            "role": "user",
                            "content": "notify avery quinn about the linear issue mentioned",
                        }
                    ]
                },
            )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(2, len(payload["tool_calls"]))
        self.assertEqual("slack_send_message", payload["tool_calls"][0]["name"])
        self.assertIsNotNone(payload["tool_calls"][0]["error"])
        self.assertEqual("slack_list_users", payload["tool_calls"][1]["name"])

    def test_classifier_routes_from_recent_history_with_latest_marker(self) -> None:
        with patch(
            "backend.solution.classify_service",
            return_value=Ambiguous(
                question="Which service should I use?",
                candidates=["slack", "gmail"],
            ),
        ) as classify_mock:
            response = self.client.post(
                "/chat",
                json={
                    "messages": [
                        {"role": "user", "content": "Find Q1 revenue email"},
                        {"role": "assistant", "content": "I found one message."},
                        {
                            "role": "user",
                            "content": "take out the content then send as slack message",
                        },
                    ]
                },
            )

        self.assertEqual(response.status_code, 200)
        classify_mock.assert_called_once()
        routed_input = classify_mock.call_args.args[0]
        self.assertIn("Recent conversation history:", routed_input)
        self.assertIn("Latest user request:", routed_input)
        self.assertIn("Find Q1 revenue email", routed_input)
        self.assertIn("take out the content then send as slack message", routed_input)


if __name__ == "__main__":
    unittest.main()
