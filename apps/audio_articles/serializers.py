from rest_framework import serializers

from apps.audio_articles.constants import (AUDIO_ARTICLE_DESCRIPTION_MAX_LENGTH,
                                        AUDIO_ARTICLE_DESCRIPTION_MIN_LENGTH,
                                        AUDIO_ARTICLE_TITLE_MAX_LENGTH,
                                        AUDIO_ARTICLE_TITLE_MIN_LENGTH)
from apps.audio_articles.models import AudioArticle


class BaseAudioArticleSerializer(serializers.Serializer):
    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("profile", "profile__user")
        return queryset


class AudioArticleSerializer(serializers.ModelSerializer, BaseAudioArticleSerializer):
    title = serializers.CharField(
        max_length=AUDIO_ARTICLE_TITLE_MAX_LENGTH,
        min_length=AUDIO_ARTICLE_TITLE_MIN_LENGTH,
        required=True,
    )
    description = serializers.CharField(
        max_length=AUDIO_ARTICLE_DESCRIPTION_MAX_LENGTH,
        min_length=AUDIO_ARTICLE_DESCRIPTION_MIN_LENGTH,
        required=True,
    )

    class Meta:
        model = AudioArticle
        fields = (
            "id",
            "audio_file",
            "slug",
            "title",
            "description",
            "duration",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("profile",)


class AudioArticleDetailSerializer(serializers.ModelSerializer, BaseAudioArticleSerializer):
    pass
