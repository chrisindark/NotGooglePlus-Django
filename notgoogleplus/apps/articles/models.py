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
    user = models.ForeignKey('profiles.Profile', related_name='articles', on_delete=models.CASCADE)
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
    user = models.ForeignKey('profiles.Profile', related_name='article_comments', on_delete=models.CASCADE)
    article = models.ForeignKey('articles.Article', related_name='article_comments', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content

    def __repr__(self):
        return '<ArticleComment: {content}>'.format(content=self.content)


class ArticleLike(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', related_name='article_likes', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', related_name='article_likes', on_delete=models.CASCADE)
    liked = models.NullBooleanField(default=None)

    class Meta:
        unique_together = (('user', 'article',),)

    def __str__(self):
        return self.article.content

    def __repr__(self):
        return '<Like: {0}{1}>'.format(self.article, self.liked)


class ArticleCommentLike(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', related_name='article_comment_l', on_delete=models.CASCADE)
    article_comment = models.ForeignKey('ArticleComment', related_name='article_comment_l', on_delete=models.CASCADE)
    liked = models.NullBooleanField(default=None)

    class Meta:
        unique_together = (('user', 'article_comment',),)

    def __str__(self):
        return self.article_comment.content

    def __repr__(self):
        return '<ArticleCommentLike: {0}{1}>'.format(self.article_comment, self.liked)
