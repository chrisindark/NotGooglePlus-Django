from celery import shared_task

# from utils.mail import api_send_mail

# from apps.core.sqsutility import SqsUtility
from notgoogleplus.celery import app


@shared_task
def add(x, y):
    return x + y


@app.task
def subtract(x, y):
    return x - y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


def backoff(attempts):
    """Return a backoff delay, in seconds, given a number of attempts.

    The delay increases very rapidly with the number of attemps:
    1, 2, 4, 8, 16, 32, ...

    """
    return 2 ** attempts


class BaseTask(app.Task):
    """Abstract base class for all tasks in my app."""

    abstract = True

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry at retry."""
        # sentrycli.captureException(exc)
        super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        # sentrycli.captureException(exc)
        super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


# sqs_utility = SqsUtility()


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


@app.task(bind=True, default_retry_delay=300, max_retries=3, soft_time_limit=5, base=BaseTask)
def send_mail(self, recipients, sender_email, subject, body):
    """Send a plaintext email with argument subject, sender and body to a list of recipients."""
    try:
        # data = api_send_mail(recipients, sender_email, subject, body)
        pass
    except Exception as e:
        # No need to retry as the user provided an invalid input
        raise
    except Exception as exc:
        # Any other exception. Log the exception to sentry and retry in 10s.
        # sentrycli.captureException()
        self.retry(countdown=10, exc=exc)
    # return data


class Handle_Event(BaseTask):
    def validate_input(self, event):
        pass

    def get_or_create_model(self, event):
        pass

    def stream_event(self, event):
        pass

    def run(self, event):
        if not self.validate_input(event):
            raise Exception(event)
        try:
            model = self.get_or_create_model(event)
        except Exception as exc:
            self.retry(countdown=backoff(self.request.retries), exc=exc)
        else:
            self.stream_event(event)
