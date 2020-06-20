import os
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Attr


class DynamoOperation:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

        table_name = os.environ.get("DYNAMODB_TABLE_NAME")
        self.table = self.dynamodb.Table(table_name)

    def __convert_float_into_decimal(self, elem):
        """
        Converts all sub-elements of type Float into Decimal.
        This is required because a DynamoDB limitation.
        :param elem: hash, array or obj
        """
        if isinstance(elem, dict):
            for k, v in elem.items():
                elem[k] = self.__convert_float_into_decimal(v)
        elif isinstance(elem, list):
            for i in range(0, len(elem)):
                elem[i] = self.__convert_float_into_decimal(elem[i])
        elif isinstance(elem, float):
            elem = Decimal(f'{elem}')
        return elem

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
        transformed_record = self.__convert_float_into_decimal(record)
        self.table.put_item(Item=transformed_record)
