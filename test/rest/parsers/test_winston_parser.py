import unittest
import jsonschema
from src.rest.parsers.winston_parser import WinstonParser


class TestWinstonParser(unittest.TestCase):
    def test_valid_payload(self):
        payload = {
            "reporter": "John Doe",
            "location": {
                "floor": 7
            }
        }
        try:
            WinstonParser(payload).validate()
        except Exception as e:
            self.fail(f"test_valid_schema() raised {e.__class__.__name__}")

    def test_invalid_payload(self):
        payload = {
            "reporter": "John Doe"
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            WinstonParser(payload).validate()
