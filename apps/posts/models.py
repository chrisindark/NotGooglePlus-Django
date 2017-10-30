from django.conf import settings
from django.db import models

from apps.core.models import TimestampedModel


# Create your models here.
def file_path_fn(instance, filename):
    # file_path = settings.FILE_UPLOAD_PATH + '{0}/{1}'.format(instance.user_id, instance.file_name)
    file_path = settings.FILE_UPLOAD_PATH + '{0}/{1}'.format(instance.file_name, instance.file_name)
    return file_path


def file_directory_path_fn(instance):
    # file_directory_path = settings.MEDIA_PATH + settings.FILE_UPLOAD_PATH + '{0}'.format(instance.user_id)
    file_directory_path = settings.MEDIA_PATH + settings.FILE_UPLOAD_PATH + '{0}'.format(instance.file_name)
    return file_directory_path


def thumbnail_file_directory_fn(instance):
    thumbnail_file_directory_path = settings.MEDIA_PATH + settings.FILE_THUMBNAIL_PATH + '{0}'.format(instance.file_name)
    return thumbnail_file_directory_path


class FileUpload(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', related_name='files', on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=file_path_fn, max_length=255
    )
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=5)
    file_content_type = models.CharField(max_length=20)
    file_size = models.BigIntegerField(default=0)
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name

    def __repr__(self):
        return '<FileUpload: {file_name}>'.format(file_name=self.file_name)


class Post(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', related_name='posts', on_delete=models.CASCADE)
    file = models.OneToOneField(
        'posts.FileUpload', related_name='post_file',
        null=True, blank=True, on_delete=models.DO_NOTHING
    )
    title = models.CharField(db_index=True, max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Post: {content}>'.format(content=self.content)

    def get_comments_count(self):
        return self.post_comments.count()


class PostLike(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', related_name='post_likes', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='post_likes', on_delete=models.CASCADE)
    liked = models.NullBooleanField(default=None)

    class Meta:
        unique_together = (('user', 'post',),)

    def __str__(self):
        return self.post.content

    def __repr__(self):
        return '<Like: {0}{1}>'.format(self.post, self.liked)


class PostComment(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', related_name='post_comments', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='post_comments', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content

    def __repr__(self):
        return '<PostComment: {content}>'.format(content=self.content)


class PostCommentLike(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', related_name='post_comment_likes', on_delete=models.CASCADE)
    post_comment = models.ForeignKey('PostComment', related_name='post_comment_likes', on_delete=models.CASCADE)
    liked = models.NullBooleanField(default=None)

    class Meta:
        unique_together = (('user', 'post_comment',),)

    def __str__(self):
        return self.post_comment.content

    def __repr__(self):
        return '<PostCommentLike: {0}{1}>'.format(self.post_comment, self.liked)
