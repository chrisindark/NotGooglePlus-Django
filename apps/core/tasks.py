from celery import shared_task

from apps.core.sqsutility import SqsUtility


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


sqs_utility = SqsUtility()


# @shared_task
# def process_sqs_messages():
#     queue_url = sqs_utility.get_sqs_queue_url('test_queue')['QueueUrl']
#     response = sqs_utility.receive_message(queue_url=queue_url)
#     print(response.get('Messages'))
#     if not response.get('Messages') or len(response.get('Messages')) == 0:
#         print('\n')
#         return
#
#     for i in range(len(response['Messages'])):
#         print(response['Messages'][i]['Body'])
#         sqs_utility.delete_message(
#             queue_url=queue_url,
#             receipt_handle=response['Messages'][i]['ReceiptHandle'])
