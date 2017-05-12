from django.contrib import admin

from .models import Tag, Article, ArticleComment

# Register your models here.
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(ArticleComment)
