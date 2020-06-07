import unittest
from src.rest.builders.grafana_builder import GrafanaBuilder


class TestGrafanaBuilder(unittest.TestCase):
    def test_success(self):
        response = GrafanaBuilder().success()
        expected_response = {
            "status_code": 200,
            "body": '{"ok": true}'
        }
        self.assertEqual(response, expected_response)

    def test_error(self):
        response = GrafanaBuilder().error()
        expected_response = {
            "status_code": 500,
            "body": '{"ok": true}'
        }
        self.assertEqual(response, expected_response)
