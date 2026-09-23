import binascii
import os

from django.db import models
from django.template.defaultfilters import slugify

from apps.audio_articles.constants import (AUDIO_ARTICLE_SLUG_MAX_LENGTH,
                                           AUDIO_ARTICLE_URL_MAX_LENGTH)
from apps.common.models import TimestampedModel


# Create your models here.
class AudioArticle(TimestampedModel):
    profile = models.ForeignKey(
        "profiles.Profile", related_name="audio_articles", on_delete=models.DO_NOTHING
    )
    audio_file = models.URLField(max_length=AUDIO_ARTICLE_URL_MAX_LENGTH)  # S3 URL
    slug = models.SlugField(
        db_index=True,
        unique=True,
        max_length=AUDIO_ARTICLE_SLUG_MAX_LENGTH,
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
        if len(slug) > AUDIO_ARTICLE_SLUG_MAX_LENGTH:
            slug = slug[:AUDIO_ARTICLE_SLUG_MAX_LENGTH]
        while len(slug + "-" + unique) > AUDIO_ARTICLE_SLUG_MAX_LENGTH:
            parts = slug.split("-")
            if len(parts) == 1:
                slug = slug[: AUDIO_ARTICLE_SLUG_MAX_LENGTH - len(unique) - 1]
            else:
                slug = "-".join(parts[:-1])

        final_slug = slug + "-" + unique
        return final_slug
