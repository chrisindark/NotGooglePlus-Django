import logging.config
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notgoogleplus_django.settings.development')

app = Celery('notgoogleplus_django')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Use Django's LOGGING config for Celery worker logs
@setup_logging.connect
def config_loggers(*args, **kwargs):
    logging.config.dictConfig(settings.LOGGING)

# app.conf.timezone = 'UTC'

app.conf.task_routes = {
    # 'apps.core.tasks.subtract': {
    #     'queue': 'default',
    #     'routing_key': 'default'
    # },
    # 'apps.core.tasks.add': {
    #     'queue': 'queue1',
    #     'routing_key': 'queue1'
    # },
    # 'apps.core.tasks.mul': {
    #     'queue': 'queue2',
    #     'routing_key': 'queue2'
    # },
}
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

app.conf.beat_schedule = {
    'enqueue-unprocessed-posts-every-minute': {
        'task': 'apps.audio_posts.tasks.enqueue_unprocessed_posts',
        # 'schedule': crontab(minute='*'),  # Run every minute
        'schedule': 10  # Runs every 10 seconds
    },
    'enqueue-unprocessed-articles-every-minute': {
        'task': 'apps.audio_articles.tasks.enqueue_unprocessed_articles',
        # 'schedule': crontab(minute='*'),  # Run every minute
        'schedule': 10  # Runs every 10 seconds
    },
    'cleanup-successful-cron-tasks-daily': {
        'task': 'apps.cron_tasks.tasks.cleanup_successful_cron_tasks',
        # 'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
        'schedule': 10  # Runs every 10 seconds
    },
    'reset-stale-cron-tasks-hourly': {
        'task': 'apps.cron_tasks.tasks.reset_stale_cron_tasks',
        # 'schedule': crontab(minute=0),  # Run every hour
        'schedule': 10  # Runs every 10 seconds
    },
}
