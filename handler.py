import logging
import os
import time
import uuid

# Logger
from dynamo_operation import DynamoOperation
from rest.parsers.grafana_parser import GrafanaParser
from rest.parsers.slackbot_parser import SlackbotParser
from rest.parsers.winston_parser import WinstonParser
from rest.builders.grafana_builder import GrafanaBuilder
from rest.builders.slackbot_builder import SlackbotBuilder
from rest.builders.winston_builder import WinstonBuilder
from slack_notification import post_slack
from spam_protection import SpamProtection
from constants import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def __retrieve_handlers(event):
    if 'reporter' in event:
        return WinstonParser(event), WinstonBuilder()
    if 'user_name' in event:
        return SlackbotParser(event), SlackbotBuilder()
    return GrafanaParser(event), GrafanaBuilder()


def __new_dynamo_record(event):
    record = event
    record['DataID'] = str(uuid.uuid4())
    record['CreatedAt'] = int(time.time() * 10000)
    record['Enabled'] = 1
    record['Delayed'] = 0
    return record


def __enabled():
    return os.environ.get('enabled', 'true') == 'true'


def __process_request(event, request_parser):
    try:
        request_parser.validate()
        data = request_parser.parse()
        floor = data["floor"]

        msg = data.get('msg', ALERTS_MSG.format(floor))
        logger.info(f"Using custom message: {msg}")

        success, slack_json_response = post_slack(msg)
        if success:
            message = SUCCESS_MSG
        else:
            logger.error(f"Slack: {slack_json_response}")
            message = FAILURE_SLACK_MSG
    except Exception as err:
        success = False
        message = GENERIC_FAILURE_MSG
        logger.error(f"Process Request error: {err}")
    return success, message


def __build_request(response_builder, message, success):
    if success:
        return response_builder.success(message)
    return response_builder.error(message)


def post_handler(event, context):
    """
    Lambda invocation entry point.
    :param event:
    :param context:
    :return:
    """
    logger.info(f"Received event: {event}")
    record = __new_dynamo_record(event)
    request_parser, response_builder = __retrieve_handlers(event)
    spam_protection = SpamProtection()

    if not __enabled():
        record['Enabled'] = 0
        success = False
        message = DISABLED_MSG
    elif spam_protection.validate():
        success, message = __process_request(event, request_parser)
    else:
        record['Delayed'] = 1
        success = True
        message = spam_protection.error

    DynamoOperation().store_event(record)

    return __build_request(response_builder, message, success)
