from datetime import timedelta
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from kombu import Queue, Exchange


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'notgoogleplus.settings.development')

app = Celery('notgoogleplus')
# Using a string here means the worker will not have to
# serialize the configuration object to child processes.
# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace="CELERY")
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.timezone = 'UTC'
app.conf.task_default_queue = 'default'
app.conf.tasks_queues = (
    Queue('default', exchange='default', routing_key='default'),
    Queue('queue1', exchange='queue1', routing_key='queue1'),
    Queue('queue2', exchange='queue2', routing_key='queue2'),
)

# _ALLOWED_QUEUES = ('default', 'queue1', 'queue2')
# task_queues = tuple(Queue(name=q, exchange=Exchange(q), routing_key=q)
#                     for q in _ALLOWED_QUEUES)

app.conf.task_routes = {
    'apps.core.tasks.subtract': {
        'queue': 'default',
        'routing_key': 'default'
    },
    'apps.core.tasks.add': {
        'queue': 'queue1',
        'routing_key': 'queue1'
    },
    'apps.core.tasks.mul': {
        'queue': 'queue2',
        'routing_key': 'queue2'
    },
}
app.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'apps.core.tasks.add',
        'schedule': timedelta(seconds=5),
        'args': (20, 20),
    },
    'subtract-every-1-minute': {
        'task': 'apps.core.tasks.subtract',
        'schedule': crontab(minute='*'),
        'args': (20, 20),
    },
    # 'process-sqs-messages-test_queue': {
    #    'task': 'apps.core.tasks.process_sqs_messages',
    #    'schedule': 1.0
    # }
}

# CELERY_QUEUES = (
#     Queue('default', exchange='default', routing_key='default'),
#     Queue('queue1', exchange='queue1', routing_key='queue1'),
#     Queue('queue2', exchange='queue2', routing_key='queue2'),
# )
# CELERY_ROUTES = {
#     'apps.core.tasks.subtract': {
#         'queue': 'default',
#         'routing_key': 'default'
#     },
#     'apps.core.tasks.add': {
#         'queue': 'queue1',
#         'routing_key': 'queue1'
#     },
#     'apps.core.tasks.mul': {
#         'queue': 'queue2',
#         'routing_key': 'queue2'
#     },
# }
# CELERY_BEAT_SCHEDULE = {
#     'add-every-5-seconds': {
#         'task': 'apps.core.tasks.add',
#         'schedule': timedelta(seconds=5),
#         'args': (20, 20),
#     },
#     'subtract-every-1-minute': {
#         'task': 'apps.core.tasks.subtract',
#         'schedule': crontab(minute='*'),
#         'args': (20, 20),
#     },
# }

# commands to run a single worker for all queues or separate workers for separate queues
# celery -A notgoogleplus worker -E -l INFO --autoscale 1,8 -n worker1 -Q default,queue1,queue2
# celery -A notgoogleplus worker -E -l INFO --autoscale 1,8 -n worker1 -Q default
# celery -A notgoogleplus worker -E -l INFO --autoscale 1,8 -n worker2 -Q queue1
# celery -A notgoogleplus worker -E -l INFO --autoscale 1,8 -n worker3 -Q queue2

# command to run celery beat for cron jobs
# celery -A notgoogleplus beat -l INFO
