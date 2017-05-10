from django.db import models

from notgoogleplus.apps.core.models import TimestampedModel


# Create your models here.
class Tag(TimestampedModel):
    slug = models.SlugField(db_index=True, unique=True)
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag

    def __repr__(self):
        return '<Tag: {tag}>'.format(tag=self.tag)


class Article(TimestampedModel):
    user = models.ForeignKey('accounts.Account', related_name='articles', on_delete=models.CASCADE)
    slug = models.SlugField(db_index=True, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField()
    content = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='article_tags')

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Article: {title}>'.format(title=self.title)


class ArticleComment(TimestampedModel):
    user = models.ForeignKey('accounts.Account', related_name='article_comments', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', related_name='article_comments', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content

    def __repr__(self):
        return '<ArticleComment: {content}>'.format(content=self.content)
