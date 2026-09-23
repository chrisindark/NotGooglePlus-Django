from rest_framework import serializers

from .constants import (
    AWS_S3_FILE_NAME_MAX_LENGTH,
    FILE_CONTENT_TYPE_MAX_LENGTH,
    FOLDER_NAME_CHOICES,
)
from .models import AppConfig


class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        fields = "__all__"


class ReadOnlyIdSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ("id",)

    @staticmethod
    def get_id(obj):
        return obj

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CreateSignedUrlSerializer(serializers.Serializer):
    folder_name = serializers.ChoiceField(
        choices=FOLDER_NAME_CHOICES, write_only=True, required=True
    )
    file_name = serializers.CharField(
        write_only=True, required=True, max_length=AWS_S3_FILE_NAME_MAX_LENGTH
    )
    content_type = serializers.CharField(
        write_only=True, required=True, max_length=FILE_CONTENT_TYPE_MAX_LENGTH
    )

    class Meta:
        fields = ()

    def validate(self, data):
        folder_name = data.get("folder_name")
        content_type = data.get("content_type")

        # Layer 1 Validation: Ensure content_type matches the folder purpose
        if folder_name in ["audio", "recordings"] and not content_type.startswith(
            "audio/"
        ):
            raise serializers.ValidationError(
                {
                    "content_type": f"Invalid content type '{content_type}' for folder '{folder_name}'. Must be audio/*."
                }
            )
        elif folder_name == "videos" and not content_type.startswith("video/"):
            raise serializers.ValidationError(
                {
                    "content_type": f"Invalid content type '{content_type}' for folder '{folder_name}'. Must be video/*."
                }
            )
        elif folder_name == "images" and not content_type.startswith("image/"):
            raise serializers.ValidationError(
                {
                    "content_type": f"Invalid content type '{content_type}' for folder '{folder_name}'. Must be image/*."
                }
            )

        return data


#     def create(self, validated_data):
#         pass

#     def update(self, instance, validated_data):
#         pass
