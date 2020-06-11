import unittest
from rest.parsers.grafana_parser import GrafanaParser


class TestGrafanaParser(unittest.TestCase):
    def test_all_payloads_are_valid(self):
        # TODO: Define what must be a minimum payload to pass this test.
        # Work on grafana dashboards are still in progress, so this tests is
        # not completed yet.
        payload = {}
        try:
            GrafanaParser(payload).validate()
        except Exception as e:
            self.fail(f"test_valid_schema() raised {e.__class__.__name__}")
