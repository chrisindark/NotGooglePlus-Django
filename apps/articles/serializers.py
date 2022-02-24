from apps.accounts.serializers import AccountSerializer
from rest_framework import serializers

from apps.profiles.serializers import ProfileSerializer
from .models import *


class TagSerializer(serializers.ModelSerializer):
    # tag = serializers.CharField(required=True)

    class Meta:
        model = Tag
        fields = ('id', 'tag', 'slug',)
        read_only_fields = ('slug', 'created_at', 'updated_at',)


class ArticleSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False)
    comments_count = serializers.IntegerField(read_only=True, required=False)
    likes_count = serializers.IntegerField(read_only=True, required=False)
    dislikes_count = serializers.IntegerField(read_only=True, required=False)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'content', 'description', 'slug', 'created_at', 'updated_at',
            'user',
            'tags',
            # 'user__user',
            'comments_count',
            'likes_count',
            'dislikes_count',
            'liked',
        )
        read_only_fields = (
            'slug', 'created_at', 'updated_at',
            'liked',
        )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user', 'user__user')
        return queryset

    @staticmethod
    def annotate_comments_count(queryset):
        queryset = queryset.annotate(
            comments_count=models.Count('article_comments', distinct=True))
        return queryset

    @staticmethod
    def annotate_likes_dislikes_count(queryset):
        queryset = queryset.annotate(likes_count=models.Count(models.Case(
            models.When(article_likes__liked=True,
                        then=models.F('article_likes__id')),
            output_field=models.IntegerField(),
            default=None
        ), distinct=True))

        queryset = queryset.annotate(dislikes_count=models.Count(models.Case(
            models.When(article_likes__liked=False,
                        then=models.F('article_likes__id')),
            output_field=models.IntegerField(),
            default=None
        ), distinct=True))

        return queryset

    def get_liked(self, obj):
        request = self.context.get('request')
        article_like_obj = None
        if not request.user.is_authenticated:
            return article_like_obj
        try:
            article_like_obj = ArticleLike.objects.get(
                user=request.user.profile, article__id=obj.id)
        except ArticleLike.DoesNotExist:
            return article_like_obj

        return article_like_obj.liked

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)

        for tag in tags:
            article.tags.add(tag)

        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)

        return instance


class ArticleLikeSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    article = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False)

    class Meta:
        model = ArticleLike
        fields = (
            'id', 'liked', 'created_at', 'updated_at',
            'article',
            'user',
        )
        read_only_fields = ('created_at', 'updated_at',)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user', 'user__user')
        return queryset

    def create(self, validated_data):
        request = self.context.get('request')
        kwargs = self.context.get('view').kwargs
        article = Article.objects.get(pk=kwargs.get('article__id'))
        if self.Meta.model.objects.filter(user=request.user.profile, article=article).exists():
            liked_obj = self.Meta.model.objects.get(
                user=request.user.profile, article=article)
            liked_obj.liked = validated_data.get('liked')
            liked_obj.save()
        else:
            liked_obj = self.Meta.model.objects.create(**validated_data)

        return liked_obj


class ArticleCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    # user = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    user__user = AccountSerializer(read_only=True, required=False)
    # article = ArticleSerializer(read_only=True, required=False)
    article = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False)
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = ArticleComment
        fields = (
            'id', 'content', 'created_at', 'updated_at',
            'user',
            'user__user',
            'article',
            'liked', 'likes_count', 'dislikes_count',
        )
        read_only_fields = ('created_at', 'updated_at', 'liked',)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user', 'user__user',)
        return queryset

    def get_liked(self, obj):
        request = self.context.get('request')
        article_comment_like_obj = None
        if not request.user.is_authenticated:
            return article_comment_like_obj
        try:
            article_comment_like_obj = ArticleCommentLike.objects.get(
                user=request.user.profile, article_comment__id=obj.id
            )
        except ArticleCommentLike.DoesNotExist:
            return article_comment_like_obj

        return article_comment_like_obj.liked

    def get_likes_count(self, obj):
        return obj.article_comment_likes.filter(liked=True).count()

    def get_dislikes_count(self, obj):
        return obj.article_comment_likes.filter(liked=False).count()


class ArticleCommentLikeSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    article_comment = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False)

    class Meta:
        model = ArticleCommentLike
        fields = (
            'id', 'created_at', 'updated_at',
            'article_comment',
            'user',
            'liked',
        )
        read_only_fields = ('created_at', 'updated_at',)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user', 'user__user')
        return queryset

    def create(self, validated_data):
        request = self.context.get('request')
        kwargs = self.context.get('view').kwargs
        if self.Meta.model.objects.filter(
            user=validated_data.get('user'), article_comment=validated_data.get('article_comment')
        ).exists():
            liked_obj = self.Meta.model.objects.get(
                user=validated_data.get('user'), article_comment=validated_data.get('article_comment')
            )
            liked_obj.liked = validated_data.get('liked')
            liked_obj.save()
        else:
            liked_obj = self.Meta.model.objects.create(**validated_data)

        return liked_obj
