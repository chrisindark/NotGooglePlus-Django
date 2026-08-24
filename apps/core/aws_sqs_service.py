import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings

DELAY_SECONDS = 60
MESSAGE_RETENTION_PERIOD = 86400
DEFAULT_WAIT_TIME_SECONDS = 20
DEFAULT_VISIBILITY_TIMEOUT = 60
DEFAULT_MAX_NUMBER_OF_MESSAGES = 1

logger = logging.getLogger(__name__)


class AwsSqsService:
    def __init__(self, access_key, secret_key, region, endpoint_url=None):
        try:
            self.sqs = boto3.client(
                "sqs",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
                endpoint_url=endpoint_url,
            )
        except Exception as exc:
            logger.exception("Failed to create SQS client")
            raise RuntimeError("Unable to initialize SQS client") from exc

    def create_sqs_queue(self, queue_name=None, attributes=None):
        queue_name = queue_name or getattr(settings, "SQS_QUEUE_NAME", None)
        if not queue_name:
            raise ValueError("Queue name is required to create an SQS queue.")

        queue_attributes = {
            "DelaySeconds": str(DELAY_SECONDS),
            "MessageRetentionPeriod": str(MESSAGE_RETENTION_PERIOD),
        }
        if attributes:
            queue_attributes.update(attributes)

        try:
            return self.sqs.create_queue(
                QueueName=queue_name, Attributes=queue_attributes
            )
        except ClientError:
            logger.exception("Failed to create SQS queue %s", queue_name)
            raise

    def delete_sqs_queue(self, queue_url):
        try:
            return self.sqs.delete_queue(QueueUrl=queue_url)
        except ClientError:
            logger.exception("Failed to delete SQS queue %s", queue_url)
            raise

    def list_sqs_queues(self, **kwargs):
        try:
            return self.sqs.list_queues(**kwargs)
        except ClientError:
            logger.exception("Failed to list SQS queues")
            raise

    def get_sqs_queue_url(self, queue_name=None):
        queue_name = queue_name or getattr(settings, "SQS_QUEUE_NAME", None)
        if not queue_name:
            raise ValueError("Queue name is required to get an SQS queue URL.")

        try:
            return self.sqs.get_queue_url(QueueName=queue_name)
        except ClientError:
            logger.exception("Failed to get SQS queue URL for %s", queue_name)
            raise

    def send_message(
        self,
        queue_url=None,
        queue_name=None,
        message_body=None,
        message_attributes=None,
        delay_seconds=None,
        message_group_id=None,
        message_deduplication_id=None,
    ):
        if queue_url is None:
            queue_url = self.get_sqs_queue_url(queue_name)["QueueUrl"]

        if message_body is None:
            raise ValueError("message_body is required to send an SQS message.")

        params = {
            "QueueUrl": queue_url,
            "MessageBody": message_body,
            "DelaySeconds": delay_seconds or DELAY_SECONDS,
        }

        if message_attributes:
            params["MessageAttributes"] = message_attributes
        if message_group_id:
            params["MessageGroupId"] = message_group_id
        if message_deduplication_id:
            params["MessageDeduplicationId"] = message_deduplication_id

        try:
            return self.sqs.send_message(**params)
        except ClientError:
            logger.exception(
                "Failed to send SQS message to %s with params %s",
                queue_url,
                {k: v for k, v in params.items() if k != "MessageBody"},
            )
            raise

    def receive_message(
        self,
        queue_url,
        max_number_of_messages=DEFAULT_MAX_NUMBER_OF_MESSAGES,
        wait_time_seconds=DEFAULT_WAIT_TIME_SECONDS,
        visibility_timeout=DEFAULT_VISIBILITY_TIMEOUT,
        attribute_names=None,
        message_attribute_names=None,
    ):
        if attribute_names is None:
            attribute_names = ["All"]
        if message_attribute_names is None:
            message_attribute_names = ["All"]

        try:
            return self.sqs.receive_message(
                QueueUrl=queue_url,
                AttributeNames=attribute_names,
                MessageAttributeNames=message_attribute_names,
                MaxNumberOfMessages=max_number_of_messages,
                VisibilityTimeout=visibility_timeout,
                WaitTimeSeconds=wait_time_seconds,
            )
        except ClientError:
            logger.exception("Failed to receive SQS message from %s", queue_url)
            raise

    def delete_message(self, queue_url, receipt_handle):
        try:
            return self.sqs.delete_message(
                QueueUrl=queue_url, ReceiptHandle=receipt_handle
            )
        except ClientError:
            logger.exception("Failed to delete SQS message from %s", queue_url)
            raise
