from rest_framework import serializers

from apps.tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    # tag = serializers.CharField(required=True)

    class Meta:
        model = Tag
        fields = (
            "id",
            "tag",
            "slug",
        )
        read_only_fields = (
            "slug",
            "created_at",
            "updated_at",
        )
