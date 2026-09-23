import binascii
import os

from django.db import models
from django.template.defaultfilters import slugify

from apps.audio_posts.constants import (AUDIO_POST_SLUG_MAX_LENGTH,
                                        AUDIO_POST_URL_MAX_LENGTH)
from apps.common.models import TimestampedModel


# Create your models here.
class AudioPost(TimestampedModel):
    profile = models.ForeignKey(
        "profiles.Profile", related_name="audio_posts", on_delete=models.DO_NOTHING
    )
    audio_file = models.URLField(max_length=AUDIO_POST_URL_MAX_LENGTH)  # S3 URL
    slug = models.SlugField(
        db_index=True,
        unique=True,
        max_length=AUDIO_POST_SLUG_MAX_LENGTH,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    duration = models.FloatField(null=True, blank=True)  # seconds
    # status = models.IntegerField(default=models.ACTIVE_STATUS)  # ACTIVE_STATUS = 1, INACTIVE_STATUS = 0

    def generate_slug(self, title=""):
        if self.slug is not None and self.slug != "":
            return ""

        slug = slugify(title)
        unique = binascii.hexlify(os.urandom(20)).decode()
        if len(slug) > AUDIO_POST_SLUG_MAX_LENGTH:
            slug = slug[:AUDIO_POST_SLUG_MAX_LENGTH]
        while len(slug + "-" + unique) > AUDIO_POST_SLUG_MAX_LENGTH:
            parts = slug.split("-")
            if len(parts) == 1:
                slug = slug[: AUDIO_POST_SLUG_MAX_LENGTH - len(unique) - 1]
            else:
                slug = "-".join(parts[:-1])

        final_slug = slug + "-" + unique
        return final_slug


# class ArticleAudio(TimestampedModel):
#     article = models.OneToOneField(
#         "articles.Article",
#         related_name="audio",
#         on_delete=models.CASCADE,
#     )
#     audio_file = models.URLField(max_length=AUDIO_POST_URL_MAX_LENGTH)
#     title = models.CharField(max_length=255, blank=True)
#     description = models.TextField(blank=True)
#     source_text = models.TextField(blank=True)
#     duration = models.FloatField(null=True, blank=True)
#     voice = models.CharField(max_length=50, blank=True)
#     output_format = models.CharField(
#         max_length=32,
#         choices=AUDIO_OUTPUT_FORMAT_CHOICES,
#         default=AUDIO_OUTPUT_FORMAT_MP3,
#     )
#     status = models.CharField(
#         max_length=32,
#         choices=AUDIO_STATUS_CHOICES,
#         default=AUDIO_STATUS_PENDING,
#     )
#     error_message = models.TextField(blank=True)
#     generated_at = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"ArticleAudio(article_id={self.article_id}, status={self.status})"


# class PostAudio(TimestampedModel):
#     post = models.OneToOneField(
#         "posts.Post",
#         related_name="audio",
#         on_delete=models.CASCADE,
#     )
#     audio_file = models.URLField(max_length=AUDIO_POST_URL_MAX_LENGTH)
#     title = models.CharField(max_length=255, blank=True)
#     description = models.TextField(blank=True)
#     source_text = models.TextField(blank=True)
#     duration = models.FloatField(null=True, blank=True)
#     voice = models.CharField(max_length=50, blank=True)
#     output_format = models.CharField(
#         max_length=32,
#         choices=AUDIO_OUTPUT_FORMAT_CHOICES,
#         default=AUDIO_OUTPUT_FORMAT_MP3,
#     )
#     status = models.CharField(
#         max_length=32,
#         choices=AUDIO_STATUS_CHOICES,
#         default=AUDIO_STATUS_PENDING,
#     )
#     error_message = models.TextField(blank=True)
#     generated_at = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"PostAudio(post_id={self.post_id}, status={self.status})"
