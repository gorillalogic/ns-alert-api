import time
from datetime import datetime
from src.dynamo_operation import DynamoOperation


class SpamProtection:
    """
    SPAM Protection. Support only 9:00 AM - 4:00PM, excluding lunch hour 12:00
    PM, Costa Rica (UTC-6)
    """

    def __init__(self):
        self.error = ""

    def valid_working_hours(self):
        utc_now = datetime.now()
        tz = 6  # UTC-6 / Costa Rica Time
        day_start = 9  # 9am
        day_end = 4  # 4pm
        lunch_start = 12  # 12pm
        lunch_end = 1  # 1pm

        condition = utc_now.hour < day_start + tz \
            or utc_now.hour > day_end + tz \
            or (lunch_start + tz <= utc_now.hour <= lunch_end + tz)

        if condition:
            self.error = f"Hey! I'm only available from {day_start}:00 AM " \
                         f"to {lunch_start}:00 PM and from {lunch_end}:00 " \
                         f"PM to {day_end}:00 PM, UTC-6. Cheers! "

        return condition

    def valid_frequency(self):
        limit_in_minutes = 2 * 60  # 2 hours
        start = int((time.time() - (60 * limit_in_minutes)) * 1000000)
        now = int(time.time() * 1000000)

        condition = DynamoOperation().query_messages_count(start, now) == 0

        if condition:
            self.error = "Thanks for your alert! The event was recorded, but " \
                         "we reported an alert less than 2 hours ago. Please " \
                         "try again in a while, or ask nicely to your fellow " \
                         "Gorilla to keep it down. Cheers!"

        return condition
