from rest_framework import serializers

from apps.articles.constants import (
    ARTICLE_TITLE_MAX_LENGTH,
    ARTICLE_TITLE_MIN_LENGTH,
    CONTENT_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    DESCRIPTION_MIN_LENGTH,
)
from apps.posts.constants import CONTENT_MIN_LENGTH

from .models import Article


class BaseArticleSerializer(serializers.Serializer):
    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("profile", "profile__user")
        return queryset


class ArticleSerializer(serializers.ModelSerializer, BaseArticleSerializer):
    title = serializers.CharField(
        max_length=ARTICLE_TITLE_MAX_LENGTH,
        min_length=ARTICLE_TITLE_MIN_LENGTH,
        required=True,
    )
    content = serializers.CharField(
        max_length=CONTENT_MAX_LENGTH, min_length=CONTENT_MIN_LENGTH, required=True
    )
    description = serializers.CharField(
        max_length=DESCRIPTION_MAX_LENGTH,
        min_length=DESCRIPTION_MIN_LENGTH,
        required=True,
    )
    username = serializers.SerializerMethodField()
    # tags = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Tag.objects.all(), required=False)
    # comments_count = serializers.IntegerField(read_only=True, required=False)
    # likes_count = serializers.IntegerField(read_only=True, required=False)
    # dislikes_count = serializers.IntegerField(read_only=True, required=False)
    # liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "content",
            "description",
            "slug",
            "created_at",
            "updated_at",
            "profile_id",
            "username",
            # 'profile__user',
            # 'tags',
            # 'comments_count',
            # 'likes_count',
            # 'dislikes_count',
            # 'liked',
        )
        read_only_fields = (
            "id",
            "slug",
            "created_at",
            "updated_at",
            "profile_id",
            "username",
        )

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        article = Article.objects.create(**validated_data)

        for tag in tags:
            article.tags.add(tag)

        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)

        return instance

    def get_username(self, instance):
        return instance.profile.user.username

    # @staticmethod
    # def annotate_comments_count(queryset):
    #     queryset = queryset.annotate(
    #         comments_count=models.Count('article_comments', distinct=True))
    #     return queryset

    # @staticmethod
    # def annotate_likes_dislikes_count(queryset):
    #     queryset = queryset.annotate(likes_count=models.Count(models.Case(
    #         models.When(article_likes__liked=True,
    #                     then=models.F('article_likes__id')),
    #         output_field=models.IntegerField(),
    #         default=None
    #     ), distinct=True))

    #     queryset = queryset.annotate(dislikes_count=models.Count(models.Case(
    #         models.When(article_likes__liked=False,
    #                     then=models.F('article_likes__id')),
    #         output_field=models.IntegerField(),
    #         default=None
    #     ), distinct=True))

    #     return queryset

    # def get_liked(self, obj):
    #     request = self.context.get('request')
    #     article_like_obj = None
    #     if not request.user.is_authenticated:
    #         return article_like_obj
    #     try:
    #         article_like_obj = ArticleLike.objects.get(
    #             user=request.user.profile, article__id=obj.id)
    #     except ArticleLike.DoesNotExist:
    #         return article_like_obj

    #     return article_like_obj.liked
