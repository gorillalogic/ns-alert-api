from rest.parsers.request_parser import RequestParser


class SlackbotParser(RequestParser):
    """
    PAYLOAD SlackCommand
    json: {
        "user_name": "jose.carballo", <- REQUIRED *
        "text": "10" <- REQUIRED *
    }
    """

    def __init__(self, payload):
        schema = {
            "type": "object",
            "properties": {
                "user_name": {"type": "string"},
                "text": {"type": "string", "enum": ["7", "10"]}
            },
            "required": ["user_name", "text"]
        }
        super().__init__(payload, schema)

    def parse(self):
        return {
            "sender": self.payload["user_name"],
            "floor": self.payload["text"]
        }
