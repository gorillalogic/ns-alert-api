import time
import unittest

from handler import post_handler
from moto.dynamodb2 import dynamodb_backend2, mock_dynamodb2
from mock import patch
import os
import json
from freezegun import freeze_time
import responses

from constants import SPAM_MSG
from dynamo_operation import DynamoOperation

BUSINESS_HOUR = "2020-01-01 15:00:00"  # or 9AM in UTC-6
LUNCH_HOUR = "2020-01-01 18:00:00"  # or 12:00 in UTC-6
OFF_HOUR = "2020-01-01 23:00:00"  # or 5:00 in UTC-6

ENV = {
    'enabled': 'true',
    'SLACK_API_TOKEN': 'tok_testing',
    'AWS_DEFAULT_REGION': 'us-east-1',
    'AWS_ACCESS_KEY_ID': 'testing',
    'AWS_SECRET_ACCESS_KEY': 'testing',
    'AWS_SECURITY_TOKEN': 'testing',
    'AWS_SESSION_TOKEN': 'testing',
    'DYNAMODB_TABLE_NAME': 'testing_table'
}


def mock_slack():
    responses.add(responses.POST, 'https://slack.com/api/chat.postMessage',
                  json={'ok': 'true'}, status=200)


def mock_failed_slack():
    responses.add(responses.POST, 'https://slack.com/api/chat.postMessage',
                  json={'ok': 'false'}, status=400)


def mock_dynamo_table():
    dynamodb_backend2.create_table(ENV['DYNAMODB_TABLE_NAME'], schema=[
        {"AttributeName": "DataID", "KeyType": "HASH"}])


def mock_existent_record():
    record = {
        'DataID': '0401c7ed-beb5-4d9f-be1a-69586cfc01e7',
        'CreatedAt': int(time.time() * 1e6),
        'Enabled': True,
        'Delayed': False
    }
    DynamoOperation().store_event(record)


@mock_dynamodb2
class TestSlackbotLambda(unittest.TestCase):
    @patch.dict(os.environ, ENV)
    def setUp(self):
        mock_dynamo_table()

    @patch.dict(os.environ, ENV)
    def tearDown(self):
        dynamodb_backend2.delete_table(ENV['DYNAMODB_TABLE_NAME'])

    @responses.activate
    @patch.dict(os.environ, ENV)
    @freeze_time(BUSINESS_HOUR, tz_offset=-6)
    def test_slackbot_request(self):
        mock_slack()
        event = {
            "user_name": "@johndoe",
            "text": "7"
        }
        response = post_handler(event, None)
        expected_response = {
            "status_code": 200,
            "body": json.dumps(
                {
                    "response_type": "ephemeral",
                    "text": "Alert triggered!"
                }
            )
        }
        self.assertEqual(response, expected_response)

    @responses.activate
    @patch.dict(os.environ, ENV)
    @freeze_time(BUSINESS_HOUR, tz_offset=-6)
    def test_winston_request(self):
        mock_slack()
        event = {
            "reporter": "John Doe",
            "location": {
                "floor": 7
            },
            "message": "Alert triggered!"
        }
        response = post_handler(event, None)
        expected_response = {
            "status_code": 200,
            "body": json.dumps(
                {
                    "message": "Alert triggered!"
                }
            )
        }
        self.assertEqual(response, expected_response)

    @responses.activate
    @patch.dict(os.environ, ENV)
    @freeze_time(BUSINESS_HOUR, tz_offset=-6)
    def test_grafana_request(self):
        mock_slack()
        event = {

        }
        response = post_handler(event, None)
        expected_response = {
            "status_code": 200,
            "body": json.dumps(
                {
                    "ok": True
                }
            )
        }
        self.assertEqual(response, expected_response)

    @responses.activate
    @patch.dict(os.environ, ENV)
    @freeze_time(BUSINESS_HOUR, tz_offset=-6)
    def test_slack_failure(self):
        mock_failed_slack()
        event = {
            "reporter": "John Doe",
            "location": {
                "floor": 7
            },
            "message": "Alert triggered!"
        }
        response = post_handler(event, None)
        expected_response = {
            "status_code": 500,
            "body": json.dumps(
                {
                    "error": "Slack failure"
                }
            )
        }
        self.assertEqual(response, expected_response)

    @responses.activate
    @patch.dict(os.environ, ENV)
    @freeze_time(BUSINESS_HOUR, tz_offset=-6)
    def test_spam_protection(self):
        mock_slack()
        mock_existent_record()
        event = {
            "reporter": "John Doe",
            "location": {
                "floor": 7
            }
        }
        response = post_handler(event, None)
        expected_response = {
            "status_code": 200,
            "body": json.dumps(
                {
                    "message": SPAM_MSG
                }
            )
        }
        self.assertEqual(response, expected_response)
