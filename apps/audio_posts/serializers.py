from rest_framework import serializers

from apps.audio_posts.constants import (AUDIO_POST_DESCRIPTION_MAX_LENGTH,
                                        AUDIO_POST_DESCRIPTION_MIN_LENGTH,
                                        AUDIO_POST_TITLE_MAX_LENGTH,
                                        AUDIO_POST_TITLE_MIN_LENGTH)
from apps.audio_posts.models import AudioPost


class BaseAudioPostSerializer(serializers.Serializer):
    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("profile", "profile__user")
        return queryset


class AudioPostSerializer(serializers.ModelSerializer, BaseAudioPostSerializer):
    title = serializers.CharField(
        max_length=AUDIO_POST_TITLE_MAX_LENGTH,
        min_length=AUDIO_POST_TITLE_MIN_LENGTH,
        required=True,
    )
    description = serializers.CharField(
        max_length=AUDIO_POST_DESCRIPTION_MAX_LENGTH,
        min_length=AUDIO_POST_DESCRIPTION_MIN_LENGTH,
        required=True,
    )

    class Meta:
        model = AudioPost
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


class AudioPostDetailSerializer(serializers.ModelSerializer, BaseAudioPostSerializer):
    pass
