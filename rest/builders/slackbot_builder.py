import json


class SlackbotBuilder:
    def success(self, message):
        body = {
            "response_type": "ephemeral",
            "text": message
        }
        return {"status_code": 200, "body": json.dumps(body)}

    def error(self, message):
        body = {
            "response_type": "ephemeral",
            "text": message
        }
        return {"status_code": 500, "body": json.dumps(body)}