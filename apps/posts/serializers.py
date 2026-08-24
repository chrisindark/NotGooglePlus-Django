from rest_framework import serializers

from apps.posts.constants import (
    CONTENT_MAX_LENGTH,
    CONTENT_MIN_LENGTH,
    TITLE_MAX_LENGTH,
    TITLE_MIN_LENGTH,
)

from .models import Post


class BasePostSerializer(serializers.Serializer):
    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("profile", "profile__user")
        return queryset


class PostSerializer(serializers.ModelSerializer, BasePostSerializer):
    title = serializers.CharField(
        max_length=TITLE_MAX_LENGTH, min_length=TITLE_MIN_LENGTH, required=True
    )
    content = serializers.CharField(
        max_length=CONTENT_MAX_LENGTH, min_length=CONTENT_MIN_LENGTH, required=True
    )
    username = serializers.SerializerMethodField()
    # comments_count = serializers.SerializerMethodField(read_only=True, required=False)
    # comments_count = serializers.IntegerField(read_only=True, required=False)
    # likes_count = serializers.IntegerField(read_only=True, required=False)
    # dislikes_count = serializers.IntegerField(read_only=True, required=False)
    # liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "profile_id",
            "username",
            # 'profile__user',
            # "file",
            # "comments_count",
            # "likes_count",
            # "dislikes_count",
            # "liked",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "profile_id",
            "username",
            # "liked",
        )

    def get_username(self, instance):
        return instance.profile.user.username

    # @staticmethod
    # def get_comments_count(post):
    #     return post.get_comments_count()

    # @staticmethod
    # def annotate_comments_count(queryset):
    #     queryset = queryset.annotate(
    #         comments_count=models.Count('post_comments', distinct=True))
    #     return queryset

    # @staticmethod
    # def annotate_likes_dislikes_count(queryset):
    #     queryset = queryset.annotate(likes_count=models.Count(models.Case(
    #         models.When(post_likes__liked=True,
    #                     then=models.F('post_likes__pk')),
    #         output_field=models.IntegerField()
    #     ), distinct=True))

    #     queryset = queryset.annotate(dislikes_count=models.Count(models.Case(
    #         models.When(post_likes__liked=False,
    #                     then=models.F('post_likes__pk')),
    #         output_field=models.IntegerField()
    #     ), distinct=True))

    #     return queryset

    # def get_liked(self, obj):
    #     request = self.context.get('request')
    #     post_like_obj = None
    #     if not request.user.is_authenticated:
    #         return post_like_obj
    #     try:
    #         post_like_obj = PostLike.objects.get(
    #             user=request.user.profile, post__id=obj.id)
    #     except PostLike.DoesNotExist:
    #         return post_like_obj

    #     return post_like_obj.liked


class PostCreateUpdateDeleteSerializer(PostSerializer):
    #     file = serializers.PrimaryKeyRelatedField(
    #         queryset=FileUpload.objects.all(), required=False, allow_null=True)
    pass


class PostListRetrieveSerializer(PostSerializer):
    #     file = FileUploadSerializer(read_only=True)
    pass
