import binascii
import os

from django.db import models
from django.template.defaultfilters import slugify
from django_mysql.models import SizedTextField

from apps.articles.constants import (
    ARTICLE_SLUG_MAX_LENGTH,
    ARTICLE_TITLE_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
)
from apps.common.models import TimestampedModel


# Create your models here.
class Article(TimestampedModel):
    profile = models.ForeignKey(
        "profiles.Profile", related_name="articles", on_delete=models.DO_NOTHING
    )
    slug = models.SlugField(
        db_index=True,
        unique=True,
        max_length=ARTICLE_SLUG_MAX_LENGTH,
        null=True,
        blank=True,
    )
    title = models.CharField(db_index=True, max_length=ARTICLE_TITLE_MAX_LENGTH)
    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH)
    content = SizedTextField()
    tags = models.ManyToManyField("tags.Tag", related_name="article_tags")
    # status = models.IntegerField(default=models.ACTIVE_STATUS)  # ACTIVE_STATUS = 1, INACTIVE_STATUS = 0

    def generate_slug(self, title=""):
        if self.slug is not None and self.slug != "":
            return ""

        slug = slugify(title)
        unique = binascii.hexlify(os.urandom(20)).decode()
        if len(slug) > ARTICLE_SLUG_MAX_LENGTH:
            slug = slug[:ARTICLE_SLUG_MAX_LENGTH]
        while len(slug + "-" + unique) > ARTICLE_SLUG_MAX_LENGTH:
            parts = slug.split("-")
            if len(parts) == 1:
                slug = slug[: ARTICLE_SLUG_MAX_LENGTH - len(unique) - 1]
            else:
                slug = "-".join(parts[:-1])

        final_slug = slug + "-" + unique
        return final_slug
