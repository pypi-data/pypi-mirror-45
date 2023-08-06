import boto3
from django.conf import settings
import json
from rest_framework.utils.encoders import JSONEncoder

"""
Description: Class helper for messages sns, sqs AWS
"""

class SqsService:
    """
    Function to send message to sqs
    Params: queue_name, msg
    """
    def push(self, queue_name, msg):
        sqs = boto3.resource('sqs',
                             region_name=settings.AWS_REGION_NAME,
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        queue = sqs.get_queue_by_name(QueueName=queue_name)

        try:
            queue.send_message(MessageBody=json.dumps(msg, cls=JSONEncoder))
            return True
        except Exception as exp:
            raise ValueError('Could not send message to SQS')


class SnsService:
    """
    Function to send message to topic sns
    Params: arn, atrribute, msg
    """
    def push(self, arn, attribute, msg):
        sns = boto3.client('sns',
                           region_name=settings.AWS_REGION_NAME,
                           aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        try:
            if attribute is None:
                sns.publish(TopicArn=arn,
                            Message=json.dumps(msg, cls=JSONEncoder))
            else:
                sns.publish(TopicArn=arn,
                            Message=json.dumps(msg, cls=JSONEncoder),
                            MessageAttributes=attribute)
            return True

        except Exception as exp:
            raise ValueError('Could not send message to SNS')

    """
    Function to make an object attribute
    Params: entity, type, status, event
    """
    def make_attributes(self, entity=None, type=None, status=None, event=None):

        attributes = {}
        if entity:
            attributes["entity"] = {
                "DataType": "String",
                "StringValue": entity
            }
        if type:
            attributes["type"] = {
                "DataType": "String",
                "StringValue": type
            }
        if status:
            attributes["status"] = {
                "DataType": "String",
                "StringValue": status
            }
        if event:
            attributes["event"] = {
                "DataType": "String",
                "StringValue": event
            }
        return attributes

    """
    Function to get complete string arn by topic name
    Params: name (topic name)
    """
    def get_arn_by_name(self, name):

        sns = boto3.client('sns',
                           region_name=settings.AWS_REGION_NAME,
                           aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        for arn in sns.list_topics()['Topics']:
            if arn['TopicArn'].split(':')[5] == name:
                return arn['TopicArn']

        raise Exception("Topic Not Found")
