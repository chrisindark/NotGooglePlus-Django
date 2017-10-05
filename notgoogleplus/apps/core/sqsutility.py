import os
import boto3

from django.conf import settings

DELAY_SECONDS = 60
MESSAGE_RETENTION_PERIOD = 86400


class SqsUtility(object):
    sqs = None

    def __init__(self):
        self.sqs = boto3.client(
            'sqs',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_SQS_HOST,
            region_name=settings.AWS_SQS_DEFAULT_REGION
        )
        pass

    def create_sqs_queue(self, queue_name=None):
        queue_name = queue_name or settings.SQS_QUEUE_NAME
        sqs_queue = self.sqs.create_queue(
            QueueName=queue_name,
            Attributes={
                'DelaySeconds': str(DELAY_SECONDS),
                'MessageRetentionPeriod': str(MESSAGE_RETENTION_PERIOD)
            }
        )

        return sqs_queue

    def delete_sqs_queue(self, queue_url=None):
        sqs_queue = self.sqs.delete_queue(
            QueueUrl=queue_url
        )

        return sqs_queue

    def list_sqs_queues(self):
        return self.sqs.list_queues()

    def get_sqs_queue_url(self, queue_name=None):
        queue_name = queue_name or settings.SQS_QUEUE_NAME
        sqs_queue = self.sqs.get_queue_url(QueueName=queue_name)
        return sqs_queue

    def send_message(self, queue_url, **kwargs):
        message_attributes = kwargs.get('message_attributes', None)
        message_body = kwargs.get('message_body', None)

        response = self.sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=DELAY_SECONDS,
            MessageAttributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': 'The Whistler'
                },
                'Author': {
                    'DataType': 'String',
                    'StringValue': 'John Grisham'
                },
                'WeeksOn': {
                    'DataType': 'Number',
                    'StringValue': '6'
                }
            },
            MessageBody=(
                'Information about current NY Times fiction bestseller for '
                'week of 12/11/2016.'
            )
        )

        return response

    def receive_message(self, queue_url):
        """
        Receives a single message from the queue url
        :param queue_url:
        :return:
        """
        response = self.sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            # MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )

        # message = response['Messages'][0]
        # receipt_handle = message['ReceiptHandle']

        return response

    def delete_message(self, queue_url, receipt_handle):
        # Delete received message from queue
        return self.sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
