from django.db import models

from apps.core.models import TimestampedModel


# Create your models here.
class Post(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', related_name='posts', on_delete=models.CASCADE)
    file = models.OneToOneField(
        'files.FileUpload', related_name='post_file',
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
