from django.db import models

from apps.common.models import TimestampedModel
from apps.posts.constants import TITLE_MAX_LENGTH


# Create your models here.
class Post(TimestampedModel):
    profile = models.ForeignKey(
        "profiles.Profile", related_name="posts", on_delete=models.DO_NOTHING
    )
    title = models.CharField(db_index=True, max_length=TITLE_MAX_LENGTH)
    content = models.TextField()
    # tags = models.JSONField(default=list)
    # tone = models.CharField(max_length=50, blank=True)
    # engagement_score = models.IntegerField(default=0)
    # file = models.OneToOneField(
    #     "files.FileUpload",
    #     related_name="post_file",
    #     null=True,
    #     blank=True,
    #     on_delete=models.DO_NOTHING,
    # )
