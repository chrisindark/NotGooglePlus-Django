import logging
import time
from typing import Any

from celery import shared_task
from django.db.models import Exists, OuterRef

from apps.audio_posts.models import AudioPost
from apps.audio_posts.services import AudioGenerationService
from apps.posts.models import Post

logger = logging.getLogger(__name__)


def update_cron_task_status(
    cron_task: Any,
    status: str,
    error_message: str | None = None,
    increment_retry: bool = False,
):
    """Helper to update a CronTask's status safely."""
    if not cron_task:
        return

    update_fields = ["status"]
    cron_task.status = status

    if error_message is not None:
        cron_task.error_message = error_message
        update_fields.append("error_message")

    if increment_retry:
        cron_task.retries += 1
        update_fields.append("retries")

    cron_task.save(update_fields=update_fields)


def detect_post_language(text_content: str) -> str:
    """Helper to detect language using langdetect."""
    if not text_content:
        return "unknown"
    try:
        from langdetect import detect

        detected_lang = detect(text_content)
        logger.info(f"Language detected: {detected_lang}")
        return detected_lang
    except Exception as e:
        logger.warning(f"Could not detect language: {e}")
        return "unknown"


def generate_and_save_audio_post(post: Post) -> AudioPost:
    """Helper to generate audio for a post and create an AudioPost record."""
    logger.info(f"Synthesizing audio for Post {post.pk}...")

    audio_service = AudioGenerationService()
    audio_bytes, output_format = audio_service.generate_audio(
        text=post.content,
        lang="en",
    )

    audio_url, _ = audio_service.upload_to_s3(
        audio_bytes=audio_bytes,
        title=f"Audio for Post {post.pk}",
        output_format=output_format,
        folder_prefix="audio_posts",
    )

    audio_post = AudioPost.objects.create(
        profile=post.profile,
        title=f"Audio for Post {post.pk}",
        description=f"Auto-generated TTS for Post {post.pk}",
        audio_file=audio_url,
    )
    audio_post.slug = audio_post.generate_slug(title=audio_post.title)
    audio_post.save(update_fields=["slug"])

    return audio_post


@shared_task(bind=True, max_retries=3, queue="audio_queue")
def process_post_synthesis(self, post_id):
    """
    Async Celery task to consume post_id events, extract the text content,
    run it through a TTS model (e.g. Piper or gTTS), upload to S3, and create an AudioPost.
    """
    start_time = time.perf_counter()
    logger.info(f"Received TTS generation event for Post ID: {post_id}")

    cron_task = None
    try:
        from django.contrib.contenttypes.models import ContentType

        from apps.cron_tasks.models import CronTask

        post_ct = ContentType.objects.get_for_model(Post)
        cron_task = CronTask.objects.filter(
            task_name="generate_audio_for_post", content_type=post_ct, object_id=post_id
        ).first()

        update_cron_task_status(cron_task, CronTask.STATUS_PROCESSING)

        post = Post.objects.filter(id=post_id).first()
        if not post:
            raise ValueError(f"Post with id {post_id} does not exist.")

        if not post.content:
            logger.warning(f"Post {post_id} has no content to synthesize.")
            update_cron_task_status(cron_task, CronTask.STATUS_COMPLETED)
            return False

        detected_lang = detect_post_language(post.content)
        logger.info(f"Language detected for Post {post_id}: {detected_lang}")

        if detected_lang != "en":
            logger.info(
                f"Skipping audio generation for non-English post {post_id} (detected: {detected_lang})."
            )
            update_cron_task_status(cron_task, CronTask.STATUS_SKIPPED)
            return False

        audio_post = generate_and_save_audio_post(post)

        update_cron_task_status(cron_task, CronTask.STATUS_COMPLETED)

        logger.info(
            f"Successfully generated AudioPost {audio_post.pk} for Post {post_id}"
        )
        end_time = time.perf_counter()
        logger.info(
            f"process_post_synthesis executed in {end_time - start_time} seconds"
        )
        return audio_post.pk

    except Exception as exc:
        logger.error(f"Error synthesizing audio for Post {post_id}: {exc}")
        if cron_task:
            from apps.cron_tasks.models import CronTask

            status = (
                CronTask.STATUS_FAILED
                if self.request.retries >= self.max_retries
                else CronTask.STATUS_PENDING
            )
            update_cron_task_status(
                cron_task, status, error_message=str(exc), increment_retry=True
            )
        raise self.retry(exc=exc, countdown=2**self.request.retries)


@shared_task
def enqueue_unprocessed_posts():
    """
    Periodic task to check for posts that haven't had their audio generated
    yet and enqueue them for processing.
    """
    from django.contrib.contenttypes.models import ContentType

    from apps.cron_tasks.models import CronTask

    start_time = time.perf_counter()
    logger.info("Checking for unprocessed posts to generate audio...")
    BATCH_SIZE = 10  # Adjust based on how many tasks your queue can handle per minute
    post_ct = ContentType.objects.get_for_model(Post)

    # processed_post_ids = CronTask.objects.filter(
    #     task_name="generate_audio_for_post",
    #     content_type=post_ct
    # ).values_list("object_id", flat=True)

    # unprocessed_posts = Post.objects.exclude(id__in=processed_post_ids)

    audio_task_exists = CronTask.objects.filter(
        task_name="generate_audio_for_post",
        content_type=post_ct,
        object_id=OuterRef("pk"),
    )

    unprocessed_posts = Post.objects.filter(~Exists(audio_task_exists))[:BATCH_SIZE]

    count = 0
    for post in unprocessed_posts:
        CronTask.objects.create(
            task_name="generate_audio_for_post",
            content_type=post_ct,
            object_id=post.pk,
            status=CronTask.STATUS_PENDING,
        )

        process_post_synthesis.delay(post.pk)
        count += 1
    logger.info(f"Enqueued {count} posts for audio generation.")

    end_time = time.perf_counter()
    logger.info(
        f"enqueue_unprocessed_posts executed in {end_time - start_time} seconds"
    )
