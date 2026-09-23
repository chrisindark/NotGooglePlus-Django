import logging
import time
from typing import Any

from celery import shared_task
from django.db.models import Exists, OuterRef

from apps.articles.models import Article
from apps.audio_articles.models import AudioArticle
from apps.audio_articles.services import AudioGenerationService

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


def generate_and_save_audio_article(article: Article) -> AudioArticle:
    """Helper to generate audio for a article and create an AudioArticle record."""
    logger.info(f"Synthesizing audio for Article {article.pk}...")

    audio_service = AudioGenerationService()
    audio_bytes, output_format = audio_service.generate_audio(
        text=article.content,
        lang="en",
    )

    audio_url, _ = audio_service.upload_to_s3(
        audio_bytes=audio_bytes,
        title=f"Audio for Article {article.pk}",
        output_format=output_format,
        folder_prefix="audio_articles",
    )

    audio_article = AudioArticle.objects.create(
        profile=article.profile,
        title=f"Audio for Article {article.pk}",
        description=f"Auto-generated TTS for Article {article.pk}",
        audio_file=audio_url,
    )
    audio_article.slug = audio_article.generate_slug(title=audio_article.title)
    audio_article.save(update_fields=["slug"])

    return audio_article


@shared_task(bind=True, max_retries=3, queue="audio_queue")
def process_article_synthesis(self, article_id):
    """
    Async Celery task to consume article_id events, extract the text content,
    run it through a TTS model (e.g. Piper or gTTS), upload to S3, and create an AudioArticle.
    """
    start_time = time.perf_counter()
    logger.info(f"Received TTS generation event for Article ID: {article_id}")

    cron_task = None
    try:
        from django.contrib.contenttypes.models import ContentType

        from apps.cron_tasks.models import CronTask

        article_ct = ContentType.objects.get_for_model(Article)
        cron_task = CronTask.objects.filter(
            task_name="generate_audio_for_article",
            content_type=article_ct,
            object_id=article_id,
        ).first()

        update_cron_task_status(cron_task, CronTask.STATUS_PROCESSING)

        article = Article.objects.filter(id=article_id).first()
        if not article:
            raise ValueError(f"Article with id {article_id} does not exist.")

        if not article.content:
            logger.warning(f"Article {article_id} has no content to synthesize.")
            update_cron_task_status(cron_task, CronTask.STATUS_COMPLETED)
            return False

        detected_lang = detect_post_language(article.content)
        logger.info(f"Language detected for Article {article_id}: {detected_lang}")

        if detected_lang != "en":
            logger.info(
                f"Skipping audio generation for non-English article {article_id} (detected: {detected_lang})."
            )
            update_cron_task_status(cron_task, CronTask.STATUS_SKIPPED)
            return False

        audio_article = generate_and_save_audio_article(article)

        update_cron_task_status(cron_task, CronTask.STATUS_COMPLETED)

        logger.info(
            f"Successfully generated AudioArticle {audio_article.pk} for Article {article_id}"
        )
        end_time = time.perf_counter()
        logger.info(
            f"process_article_synthesis executed in {end_time - start_time} seconds"
        )
        return audio_article.pk

    except Exception as exc:
        logger.error(f"Error synthesizing audio for Article {article_id}: {exc}")
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
def enqueue_unprocessed_articles():
    """
    Periodic task to check for posts that haven't had their audio generated
    yet and enqueue them for processing.
    """
    from django.contrib.contenttypes.models import ContentType

    from apps.cron_tasks.models import CronTask

    start_time = time.perf_counter()
    logger.info("Checking for unprocessed articles to generate audio...")
    BATCH_SIZE = 10  # Adjust based on how many tasks your queue can handle per minute
    article_ct = ContentType.objects.get_for_model(Article)

    audio_task_exists = CronTask.objects.filter(
        task_name="generate_audio_for_article",
        content_type=article_ct,
        object_id=OuterRef("pk"),
    )

    unprocessed_articles = Article.objects.filter(~Exists(audio_task_exists))[
        :BATCH_SIZE
    ]

    count = 0
    for article in unprocessed_articles:
        CronTask.objects.create(
            task_name="generate_audio_for_article",
            content_type=article_ct,
            object_id=article.pk,
            status=CronTask.STATUS_PENDING,
        )

        process_article_synthesis.delay(article.pk)
        count += 1
    logger.info(f"Enqueued {count} articles for audio generation.")

    end_time = time.perf_counter()
    logger.info(
        f"enqueue_unprocessed_articles executed in {end_time - start_time} seconds"
    )
