import binascii
import os

from django.db import models
from django.template.defaultfilters import slugify

from apps.common.models import TimestampedModel
from apps.tags.constants import TAG_MAX_LENGTH, TAG_SLUG_MAX_LENGTH


# Create your models here.
class Tag(TimestampedModel):
    slug = models.SlugField(
        db_index=True,
        unique=True,
        max_length=TAG_SLUG_MAX_LENGTH,
        null=True,
        blank=True,
    )
    tag = models.CharField(max_length=TAG_MAX_LENGTH, db_index=True, unique=True)
    created_by = models.ForeignKey(
        "profiles.Profile",
        related_name="tag_created_by",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "profiles.Profile",
        related_name="tag_updated_by",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    def generate_slug(self, title=""):
        if self.slug is not None and self.slug != "":
            return ""

        slug = slugify(title)
        unique = binascii.hexlify(os.urandom(20)).decode()
        if len(slug) > TAG_SLUG_MAX_LENGTH:
            slug = slug[:TAG_SLUG_MAX_LENGTH]
        while len(slug + "-" + unique) > TAG_SLUG_MAX_LENGTH:
            parts = slug.split("-")
            if len(parts) == 1:
                slug = slug[: TAG_SLUG_MAX_LENGTH - len(unique) - 1]
            else:
                slug = "-".join(parts[:-1])

        final_slug = slug + "-" + unique
        return final_slug
