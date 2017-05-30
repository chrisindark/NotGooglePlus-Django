from rest_framework import serializers

from notgoogleplus.apps.profiles.serializers import ProfileSerializer
from notgoogleplus.apps.accounts.serializers import AccountSerializer

from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tag', 'slug',)
        read_only_fields = ('slug', 'created_at', 'updated_at',)

    # def to_representation(self, obj):
        # return obj.tag


class ArticleSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    # user__user = AccountSerializer(read_only=True, required=False)
    # tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    comments_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'content', 'description', 'slug', 'created_at', 'updated_at',
            'user',
            # 'user__user',
            'comments_count',
        )
        read_only_fields = (
            'slug', 'created_at', 'updated_at',
        )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user', 'user__user')
        return queryset

    @staticmethod
    def annotate_comments_count(queryset):
        queryset = queryset.annotate(comments_count=models.Count('article_comments', distinct=True))
        return queryset

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)

        for tag in tags:
            print(tag)
            article.tags.add(tag)

        return article

    def update(self, instance, validated_data):
        # user = self.context.get('user', None)
        tags = validated_data.pop('tags', [])
        for key in validated_data.keys():
            setattr(instance, key, validated_data[key])
        instance.save()
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)

        return instance


class ArticleCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    # user = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    user__user = AccountSerializer(read_only=True, required=False)
    # article = ArticleSerializer(read_only=True, required=False)
    article = serializers.PrimaryKeyRelatedField(read_only=True, required=False)

    class Meta:
        model = ArticleComment
        fields = (
            'id', 'content', 'created_at', 'updated_at',
            'user',
            'user__user',
            'article',
        )
        read_only_fields = ('created_at', 'updated_at',)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user', 'user__user',)
        return queryset
