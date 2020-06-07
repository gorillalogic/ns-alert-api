import boto3
from boto3.dynamodb.conditions import Attr


class DynamoOperation:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('prod-noisealertreporttable')

    def query_messages_count(self, start_time, end_time):
        """
        :param start_time:
        :param end_time:
        :return: the amount of messages between start_time and end_time.
        """
        last_sent_filter = Attr('CreatedAt').between(start_time, end_time) & \
            Attr('Delayed').eq(False) & Attr('Enabled').eq(True)
        return len(self.table.scan(FilterExpression=last_sent_filter)['Items'])

    def store_event(self, record):
        """
        Stores an event to DynamoDB.
        :param record:
        :return:
        """
        self.table.put_item(Item=record)
