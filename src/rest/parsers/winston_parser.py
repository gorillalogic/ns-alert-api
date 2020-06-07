from src.rest.parsers.request_parser import RequestParser


class WinstonParser(RequestParser):
    def __init__(self, payload):
        schema = {
            "type": "object",
            "properties": {
                "reporter": {"type": "string"},
                "location": {
                    "type": "object",
                    "properties": {
                        "floor": {"type": "integer", "enum": [7, 10]},
                        "zone": {"type": "string"},
                        "column": {"type": "string"}
                    },
                    "required": ["floor"]
                },
                "force": {"type": "string"},
                "message": {"type": "string"}
            },
            "required": ["reporter", "location"]
        }
        super().__init__(payload, schema)

    def parse(self):
        return {
            "sender": self.payload["reporter"],
            "floor": self.payload["location"]["floor"]
        }
