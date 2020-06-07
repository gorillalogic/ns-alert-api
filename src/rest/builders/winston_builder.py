import json


class WinstonBuilder:
    def success(self, message):
        body = {
            "message": message
        }
        return {"status_code": 200, "body": json.dumps(body)}

    def error(self, error):
        body = {
            "error": error
        }
        return {"status_code": 500, "body": json.dumps(body)}
