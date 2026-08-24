import binascii
import os

from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from rest_framework import generics, permissions, viewsets

from apps.articles.constants import ARTICLE_SLUG_MAX_LENGTH
from apps.articles.filters import ArticleFilter
from apps.articles.models import Article
from apps.articles.pagination import ArticlePagination
from apps.articles.permissions import IsArticleOwner
from apps.articles.serializers import ArticleSerializer
from apps.core.mixins import ReadOnlyIdListMixin
from apps.profiles.models import Profile


# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filter_class = ArticleFilter

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsArticleOwner()]

    def get_queryset(self):
        # Set up eager loading to avoid N + 1 selects
        queryset = self.queryset
        serializer_class = self.get_serializer_class()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        # queryset = self.get_serializer_class().annotate_comments_count(queryset)
        # queryset = self.get_serializer_class().annotate_likes_dislikes_count(queryset)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)
        serializer.save(profile=profile)
        self.create_slug(serializer.instance)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.create_slug(serializer.instance)

    # Logic to be removed and instead call model class function
    def create_slug(self, article: Article):
        if article.slug is not None and article.slug != "":
            return article

        slug = slugify(article.title)
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

        # final_slug = article.generate_slug(article.title)
        # if final_slug == "":
        #     return
        article.slug = final_slug
        article.save()
        return article


class ArticleIdListView(ReadOnlyIdListMixin, generics.ListAPIView):
    queryset = Article.objects.all()
    pagination_class = ArticlePagination
    filter_class = ArticleFilter
