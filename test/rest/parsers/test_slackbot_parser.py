import unittest
import jsonschema
from src.rest.parsers.slackbot_parser import SlackbotParser


class TestSlackbotParser(unittest.TestCase):
    def test_valid_payload(self):
        payload = {
            "user_name": "@john_doe",
            "text": "7"
        }
        try:
            SlackbotParser(payload).validate()
        except Exception as e:
            self.fail(f"test_valid_schema() raised {e.__class__.__name__}")

    def test_invalid_floor(self):
        payload = {
            "user_name": "@john_doe",
            "text": "12"
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            SlackbotParser(payload).validate()
