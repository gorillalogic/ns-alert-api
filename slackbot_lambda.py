import logging
import os
import time
import uuid

# Logger
from src.dynamo_operation import DynamoOperation
from src.rest.parsers.grafana_parser import GrafanaParser
from src.rest.parsers.slackbot_parser import SlackbotParser
from src.rest.parsers.winston_parser import WinstonParser
from src.rest.builders.grafana_builder import GrafanaBuilder
from src.rest.builders.slackbot_builder import SlackbotBuilder
from src.rest.builders.winston_builder import WinstonBuilder
from src.slack_notification import post_slack
from src.spam_protection import SpamProtection
from src.constants import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def __retrieve_handlers(event):
    if 'reporter' in event:
        return WinstonParser, WinstonBuilder
    if 'user_name' in event:
        return SlackbotParser, SlackbotBuilder
    return GrafanaParser, GrafanaBuilder


def post_handler(event, context):
    """
    Lambda invocation entry point.
    :param event:
    :param context:
    :return:
    """
    logger.info(f"Received event: {event}")

    record = event
    record['DataID'] = str(uuid.uuid4())
    record['CreatedAt'] = int(time.time() * 10000)
    record['Enabled'] = os.environ.get('enabled', 'true') == 'true'

    spam_protection = SpamProtection()
    if not spam_protection.valid_working_hours():
        logger.error("Function invoked on non-working hours.")
    elif not spam_protection.valid_frequency():
        record['Delayed'] = 1
        logger.info("Event Delayed.")

    DynamoOperation.store_event(record)

    request_parser, response_builder = __retrieve_handlers(event)

    error = None
    message = None
    try:
        request_parser.validate()
        data = request_parser.parse()
        floor = data["floor"]

        if record['Delayed']:
            message = DELAYED_MSG
        elif record['Enabled']:
            msg = event.get('msg', ALERTS_MSG.format(floor))
            response = post_slack(msg)

            if response['ok']:
                message = response
            else:
                error = response
        else:
            message = DISABLED_MSG
    except Exception as err:
        error = str(err)
        logger.error(err)

    if error is not None:
        response = response_builder.error(error)
    else:
        response = response_builder.success(message)
    return response
