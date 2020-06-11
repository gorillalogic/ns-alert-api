import json


class GrafanaBuilder:
    def success(self, message):
        body = {
            "ok": True
        }
        return {"status_code": 200, "body": json.dumps(body)}

    def error(self, message):
        body = {
            "ok": False
        }
        return {"status_code": 500, "body": json.dumps(body)}
