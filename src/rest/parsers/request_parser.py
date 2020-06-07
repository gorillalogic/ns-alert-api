from jsonschema import validate


class RequestParser:
    def __init__(self, payload, schema):
        self.payload = payload
        self.schema = schema

    """
    Abstract class that represents a Request Parser.
    """
    def validate(self):
        """
        Validates a payload against a schema using 'jsonschema' lib.
        :return:
        """
        validate(instance=self.payload, schema=self.schema)
