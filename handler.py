import logging
import os
import time
import uuid
from decimal import *

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
    if 'ruleId' in event:
        return GrafanaParser(event), GrafanaBuilder()


def __new_dynamo_record(event):
    record = event
    record['DataID'] = str(uuid.uuid4())
    record['CreatedAt'] = int(time.time() * 1000000)
    record['Enabled'] = True
    record['Delayed'] = False
    return record


def __enabled():
    return os.environ.get('enabled', 'true') == 'true'


def __process_request(event, request_parser):
    try:
        request_parser.validate()
        data = request_parser.parse()

        if 'sensor' in data:
            msg = data.get('msg', GRAFANA_ALERT_MSG.format(data['sensor'],
                                                           data['value']))
        else:
            msg = data.get('msg', ALERT_MSG.format(data['floor']))

        success, slack_response = post_slack(msg)
        if success:
            message = SUCCESS_MSG
            logger.info(f"Slack status: {success} with {slack_response}")
        else:
            message = FAILURE_SLACK_MSG
            logger.error(f"Slack status: {success} with {slack_response}")
    except Exception as err:
        success = False
        message = GENERIC_FAILURE_MSG
        logger.error(f"Process Request error: {err}", exc_info=True)
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

    if request_parser and response_builder:
        logger.info(f"Using parser {request_parser.__class__.__name__}")
        logger.info(f"Using builder {response_builder.__class__.__name__}")

        spam_protection = SpamProtection()

        if not __enabled():
            record['Enabled'] = True
            success = False
            message = DISABLED_MSG
        elif spam_protection.validate():
            success, message = __process_request(event, request_parser)
        else:
            record['Delayed'] = False
            success = True
            message = spam_protection.error

        DynamoOperation().store_event(record)
    else:
        success = False
        message = UNKNOWN_AGENT

    return __build_request(response_builder, message, success)
