from rest.parsers.request_parser import RequestParser


class GrafanaParser(RequestParser):
    def __init__(self, payload):
        schema = {
            "type": "object",
            "properties": {
                "dashboardId": {"type": "integer", "enum": [3]},
                "evalMatches": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number"},
                            "metric": {"type": "string"}
                        }
                    }
                },
                "orgId": {"type": "integer", "enum": [1]},
                "panelId": {"type": "integer", "enum": [2]},
                "ruleId": {"type": "integer", "enum": [1]},
                "ruleName": {"type": "string"},
                "ruleUrl": {"type": "string"},
                "state": {"type": "string"},
                "title": {"type": "string"},
            }
        }
        super().__init__(payload, schema)

    def parse(self):
        value = self.payload["evalMatches"][0]["value"]
        sensor = self.payload["evalMatches"][0]["metric"]
        return {
            "sender": "grafana",
            "sensor": sensor,
            "value": int(value)
        }
