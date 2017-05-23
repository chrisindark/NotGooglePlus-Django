from rest_framework import serializers

from notgoogleplus.apps.profiles.serializers import ProfileSerializer

from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tag',)
        read_only_fields = ()

    # def to_representation(self, obj):
        # return obj.tag


class ArticleSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    # title = serializers.CharField(required=False)
    # content = serializers.CharField(required=False)
    # slug = serializers.SlugField(required=False)
    description = serializers.CharField(required=False)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Article
        fields = ('id', 'content', 'description', 'tags', 'slug', 'user',)
        read_only_fields = ('slug', 'created_at', 'updated_at',)

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
        # author = self.context.get('user', None)
        tags = validated_data.pop('tags', [])
        instance.save()
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)

        return instance


class ArticleCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    article = ArticleSerializer(read_only=True, required=False)

    class Meta:
        model = ArticleComment
        fields = ('id', 'content', 'user', 'article', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at',)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user')
        return queryset
