import unittest
from slackbot_lambda import post_handler
from test.support import EnvironmentVarGuard
from moto.dynamodb import dynamodb_backend, mock_dynamodb


def dynamodb_table(table_name):
    with mock_dynamodb():
        dynamodb_backend.create_table(
            table_name,
            schema=[{u'KeyType': u'HASH', u'AttributeName': u'name'}])
        yield table_name


@mock_dynamodb
class TestSlackbotLambda(unittest.TestCase):
    def setupUp(self):
        self.env = EnvironmentVarGuard()
        self.env.set('enabled', 'true')
        self.env.set('SLACK_API_TOKEN', 'tok_testing')
        self.env.set('AWS_ACCESS_KEY_ID', 'testing')
        self.env.set('AWS_SECRET_ACCESS_KEY', 'testing')
        self.env.set('AWS_SECURITY_TOKEN', 'testing')
        self.env.set('AWS_SESSION_TOKEN', 'testing')
        self.env.set('DYNAMODB_TABLE_NAME', 'testing_table')

        dynamodb_backend.create_table("testing_table", schema=[
            {u'KeyType': u'HASH', u'AttributeName': u'name'}])

    def test_slackbot_request(self):
        event = {
            "user_name": "@johndoe",
            "text": "Alert triggered!"
        }
        context = None
        response = post_handler(event, context)
        expected_response = {

        }

        self.assertEqual(response, expected_response)

    def test_winston_request(self):
        event = {
            "reporter": "John Doe",
            "location": {
                "floor": "7"
            },
            "message": "Alert triggered!"
        }
        context = None
        response = post_handler(event, context)
        expected_response = {

        }
        self.assertEqual(response, expected_response)

    def test_grafana_request(self):
        event = {

        }
        context = None
        response = post_handler(event, context)
        expected_response = {

        }
        self.assertEqual(response, expected_response)
