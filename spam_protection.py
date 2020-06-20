import time
import os
import logging

from constants import INVALID_HOURS, SPAM_MSG
from dynamo_operation import DynamoOperation

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SpamProtection:
    """
    SPAM Protection. Support only 9:00 AM - 4:00PM, excluding lunch hour 12:00
    PM, Costa Rica (UTC-6)
    """

    def __init__(self):
        self.error = None
        self.dynamo_operation = DynamoOperation()

    def __valid_working_hours(self):
        tz = -6  # UTC-6 / Costa Rica Time
        day_start = 9  # 9am
        day_end = 16  # 4pm
        lunch_start = 12  # 12pm
        lunch_end = 13  # 1pm

        utc_now = time.gmtime()
        hour = utc_now.tm_hour + tz

        morning = day_start <= hour <= lunch_start
        afternoon = lunch_end <= hour <= day_end

        condition = morning or afternoon or os.environ.get('debug') == 'true'

        if not condition:
            self.error = INVALID_HOURS.format(day_start, lunch_start,
                                              lunch_end % 12, day_end % 12)

        return condition

    def __valid_frequency(self):
        limit_in_minutes = 2 * 60  # 2 hours
        start = int((time.time() - (60 * limit_in_minutes)) * 1000000)
        now = int(time.time() * 1000000)

        count = self.dynamo_operation.query_messages_count(start, now)
        condition = (count == 0)

        logging.info(f"Found {count} messages from {start} to {now}")

        if not condition:
            self.error = SPAM_MSG

        return condition

    def validate(self):
        return self.__valid_frequency() and self.__valid_working_hours()
