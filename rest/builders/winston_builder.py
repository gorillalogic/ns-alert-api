import json


class WinstonBuilder:
    def success(self, message):
        body = {
            "message": message
        }
        return {"status_code": 200, "body": json.dumps(body)}

    def error(self, message):
        body = {
            "error": message
        }
        return {"status_code": 500, "body": json.dumps(body)}
