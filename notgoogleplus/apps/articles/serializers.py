from rest_framework import serializers

from notgoogleplus.apps.accounts.serializers import AccountSerializer

from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tag',)
        read_only_fields = ()

    # def to_representation(self, obj):
        # return obj.tag


class ArticleSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)
    # title = serializers.CharField(required=False)
    # content = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    # slug = serializers.SlugField(required=False)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Article
        fields = ('id', 'content', 'description', 'tags', 'slug', 'user',)
        read_only_fields = ('slug', 'created_at', 'updated_at', 'user',)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user')
        return queryset

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)

        for tag in tags:
            print(tag)
            article.tags.add(tag)

        return article

    def update(self, instance, validated_data):
        # author = self.context.get('author', None)
        tags = validated_data.pop('tags', [])
        instance.save()
        instance.tags.clear()
        for tag in tags:
            article.tags.add(tag)

        return instance


class ArticleCommentSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True, required=False)
    article = ArticleSerializer(read_only=True, required=False)

    class Meta:
        model = ArticleComment
        fields = ('id', 'content', 'created_at', 'updated_at', 'post', 'user', 'article',)
        read_only_fields = ('created_at', 'updated_at', 'user', 'article',)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user')
        return queryset