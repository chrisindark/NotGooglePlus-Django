import logging
import time
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.cron_tasks.models import CronTask

logger = logging.getLogger(__name__)

@shared_task
def cleanup_successful_cron_tasks():
    """
    Periodic task to delete successful cron tasks that are older than 7 days
    to keep the table size small.
    """
    start_time = time.perf_counter()
    days_ago = timezone.now() - timedelta(days=7)
    old_tasks = CronTask.objects.filter(
        status=CronTask.STATUS_COMPLETED,
        created_at__lte=days_ago
    )
    count = old_tasks.count()
    old_tasks.delete()
    logger.info(f"Deleted {count} successful cron tasks older than 7 days.")
    end_time = time.perf_counter()
    logger.info(f"cleanup_successful_cron_tasks executed in {end_time - start_time} seconds")

@shared_task
def reset_stale_cron_tasks():
    """
    Periodic task to find tasks stuck in PENDING or PROCESSING for too long
    and reset them so they can be retried.
    """
    start_time = time.perf_counter()
    timeout_threshold = timezone.now() - timedelta(hours=48)
    BATCH_SIZE = 10  # Adjust based on how many tasks your queue can handle per minute
    # Find tasks stuck for more than 1 hour
    stale_tasks = CronTask.objects.filter(
        status__in=[CronTask.STATUS_PENDING, CronTask.STATUS_PROCESSING],
        updated_at__lte=timeout_threshold
    )[:BATCH_SIZE]
    
    count = stale_tasks.count()
    if count > 0:
        # Reset them to FAILED so the retry mechanism or a manual trigger can pick them up
        # Alternatively, we could reset to PENDING and trigger their respective Celery tasks again
        stale_tasks.update(
            status=CronTask.STATUS_FAILED,
            error_message="Task timed out and was marked as stale by sweeper."
        )
        logger.warning(f"Reset {count} stale cron tasks to FAILED state.")
    else:
        logger.info("No stale cron tasks found.")
    
    end_time = time.perf_counter()
    logger.info(f"reset_stale_cron_tasks executed in {end_time - start_time} seconds")
