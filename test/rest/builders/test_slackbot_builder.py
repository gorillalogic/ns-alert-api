import unittest
from src.rest.builders.slackbot_builder import SlackbotBuilder


class TestSlackbotBuilder(unittest.TestCase):
    def test_success(self):
        response = SlackbotBuilder().success("Lorem Ipsum")
        expected_response = {
            "status_code": 200,
            "body": '{"response_type": "ephemeral", "text": "Lorem Ipsum"}'
        }
        self.assertEqual(response, expected_response)

    def test_error(self):
        response = SlackbotBuilder().error("Lorem Ipsum")
        expected_response = {
            "status_code": 500,
            "body": '{"response_type": "ephemeral", "text": "Lorem Ipsum"}'
        }
        self.assertEqual(response, expected_response)