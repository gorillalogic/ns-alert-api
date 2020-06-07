import unittest
from src.rest.builders.winston_builder import WinstonBuilder


class TestWinstonBuilder(unittest.TestCase):
    def test_success(self):
        response = WinstonBuilder().success("Lorem Ipsum")
        expected_response = {
            "status_code": 200,
            "body": '{"message": "Lorem Ipsum"}'
        }
        self.assertEqual(response, expected_response)

    def test_error(self):
        response = WinstonBuilder().error("Lorem Ipsum")
        expected_response = {
            "status_code": 500,
            "body": '{"error": "Lorem Ipsum"}'
        }
        self.assertEqual(response, expected_response)
