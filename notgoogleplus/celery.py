# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os

from celery import Celery

from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notgoogleplus.settings.development')

app = Celery('notgoogleplus')
# Using a string here means the worker will not have to
# serialize the configuration object to child processes.
# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    # 'add-every-5-seconds': {
    #     'task': 'apps.core.tasks.add',
    #     'schedule': 1.0,
    #     'args': (16, 16),
    # },
    'process-sqs-messages-test_queue': {
        'task': 'apps.core.tasks.process_sqs_messages',
        'schedule': 1.0
    }
}
app.conf.timezone = 'UTC'
