from rest.parsers.request_parser import RequestParser


class GrafanaParser(RequestParser):
    def __init__(self, payload):
        schema = {

        }
        super().__init__(payload, schema)

    def parse(self):
        return {
            "sender": "grafana",
            "floor": 7
        }
