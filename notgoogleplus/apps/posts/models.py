from django.db import models
from django.conf import settings


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey('profiles.Profile', related_name='posts', on_delete=models.CASCADE)
    file = models.OneToOneField('posts.File', related_name='post_file', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

    def __repr__(self):
        return '<Post: {content}>'.format(content=self.content)


class PostComment(models.Model):
    user = models.ForeignKey('profiles.Profile', related_name='post_comments', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='post_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

    def __repr__(self):
        return '<PostComment: {content}>'.format(content=self.content)


def file_directory_path(instance, filename):
    return settings.FILE_UPLOAD_PATH + '{0}/{1}'.format(instance.user_id, instance.name)


class File(models.Model):
    user = models.ForeignKey('profiles.Profile', related_name='files', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=file_directory_path, max_length=255)
    file_type = models.CharField(max_length=5)
    file_content_type = models.CharField(max_length=20)
    size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<File: {name}>'.format(name=self.name)


# class LikesDislikes():
#     user = models.ForeignKey('profiles.Profile')
#     topic_type = models.CharField(max_length=255)
#     topic_id = models.BigIntegerField()
#     liked = models.NullBooleanField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __unicode__(self):
#         return self.topic_type + '_' + self.topic_id

#     def __repr__(self):
#         return '<LikesDislikes: {0}{1}>'.format(self.topic_type, self.topic_id)
