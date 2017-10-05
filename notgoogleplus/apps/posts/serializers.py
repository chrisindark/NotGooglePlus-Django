from django.utils.crypto import get_random_string

from rest_framework import serializers

from notgoogleplus.apps.profiles.serializers import ProfileSerializer
from notgoogleplus.apps.accounts.serializers import AccountSerializer

from .models import *
from .constants import *


class FileUploadSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)

    class Meta:
        model = FileUpload
        fields = (
            'id', 'file', 'file_name', 'file_type', 'file_content_type',
            'file_size', 'file_path', 'created_at', 'updated_at',
            'user',
        )
        read_only_fields = (
            'id', 'file_name', 'file_type', 'file_content_type',
            'file_size', 'file_path', 'created_at', 'updated_at',
        )

    def validate(self, data):
        if len(data['file'].name) > 75:
            raise serializers.ValidationError({
                'file': 'File name should be less than or equal to 75 characters.'
            })

        data['file_type'] = self.get_filetype(data['file'])

        if data['file_type'] == 'image' and data['file'].content_type not in ALLOWED_IMAGE_TYPES:
            raise serializers.ValidationError({'file': 'Image format should be of {0}.'.format(
                ', '.join(ALLOWED_IMAGE_TYPES))})
        elif data['file_type'] == 'audio' and data['file'].content_type not in ALLOWED_AUDIO_TYPES:
            raise serializers.ValidationError({'file': 'Audio format should be of {0}.'.format(
                ', '.join(ALLOWED_AUDIO_TYPES))})
        elif data['file_type'] == 'video' and data['file'].content_type not in ALLOWED_VIDEO_TYPES:
            raise serializers.ValidationError({'file': 'Video format should be of {0}.'.format(
                ', '.join(ALLOWED_VIDEO_TYPES))})

        return data

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user', 'user__user')
        return queryset

    # @staticmethod
    # def set_filename(file):
    #     filename_list = file.name.lower().replace(' ', '_').split('.')
    #     ext = filename_list.pop()
    #     filename = ''.join(filename_list) + get_random_string(25) + '.' + ext
    #     return filename

    @staticmethod
    def get_filetype(file):
        if file.content_type.split('/')[0] not in ALLOWED_FILE_TYPES:
            raise serializers.ValidationError({'file': 'File type should be of {0}'.format(', '.join(ALLOWED_FILE_TYPES))})
        return ALLOWED_FILE_TYPES[ALLOWED_FILE_TYPES.index(file.content_type.split('/')[0])]


class PostSerializer(serializers.ModelSerializer):
    # user__user = AccountSerializer(read_only=True, required=False)
    user = ProfileSerializer(read_only=True, required=False)
    # comments_count = serializers.SerializerMethodField(read_only=True, required=False)
    comments_count = serializers.IntegerField(read_only=True, required=False)
    likes_count = serializers.IntegerField(read_only=True, required=False)
    dislikes_count = serializers.IntegerField(read_only=True, required=False)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'content', 'created_at', 'updated_at',
            'file',
            'user',
            # 'user__user',
            'comments_count',
            'likes_count',
            'dislikes_count',
            'liked',
        )
        read_only_fields = (
            'created_at', 'updated_at',
            'liked',
        )

    # @staticmethod
    # def get_comments_count(post):
    #     return post.get_comments_count()

    # def get_user(self, instance):
    #     request = self.context.get('request')
    #     serializer = ProfileSerializer(instance.user, context={'request': request})
    #     return serializer.data

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('file', 'user', 'user__user')
        return queryset

    @staticmethod
    def annotate_comments_count(queryset):
        queryset = queryset.annotate(comments_count=models.Count('post_comments', distinct=True))
        return queryset

    @staticmethod
    def annotate_likes_dislikes_count(queryset):
        queryset = queryset.annotate(likes_count=models.Count(models.Case(
            models.When(post_likes__liked=True, then=models.F('post_likes__pk')),
            output_field=models.IntegerField()
        ), distinct=True))

        queryset = queryset.annotate(dislikes_count=models.Count(models.Case(
            models.When(post_likes__liked=False, then=models.F('post_likes__pk')),
            output_field=models.IntegerField()
        ), distinct=True))

        return queryset

    def get_liked(self, obj):
        request = self.context.get('request')
        post_like_obj = None
        if not request.user.is_authenticated():
            return post_like_obj
        try:
            post_like_obj = PostLike.objects.get(user=request.user.profile, post__id=obj.id)
        except PostLike.DoesNotExist:
            return post_like_obj

        return post_like_obj.liked

    # def to_representation(self, obj):
    #     obj = super(PostSerializer, self).to_representation(obj)
    #     depth = self.context.get('request').query_params.get('depth')
    #     if depth != '1':
    #         obj.pop('user')

    #     return obj


class PostCreateUpdateDeleteSerializer(PostSerializer):
    file = serializers.PrimaryKeyRelatedField(queryset=FileUpload.objects.all(), required=False, allow_null=True)


class PostListRetrieveSerializer(PostSerializer):
    file = FileUploadSerializer(read_only=True)


class PostLikeSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    post = serializers.PrimaryKeyRelatedField(read_only=True, required=False)

    class Meta:
        model = PostLike
        fields = (
            'id', 'created_at', 'updated_at',
            'post',
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
            user=validated_data.get('user'), post=validated_data.get('post')
        ).exists():
            liked_obj = self.Meta.model.objects.get(
                user=validated_data.get('user'), post=validated_data.get('post')
            )
            liked_obj.liked = validated_data.get('liked')
            liked_obj.save()
        else:
            liked_obj = self.Meta.model.objects.create(**validated_data)

        return liked_obj


class PostCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    # post = PostSerializer(read_only=True, required=False)
    post = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ('id', 'content', 'created_at', 'updated_at', 'post', 'user', 'liked',)
        read_only_fields = ('created_at', 'updated_at', 'liked',)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user', 'user__user')
        return queryset

    def get_liked(self, obj):
        request = self.context.get('request')
        post_comment_like_obj = None
        if not request.user.is_authenticated():
            return post_comment_like_obj
        try:
            post_comment_like_obj = PostCommentLike.objects.get(
                user=request.user.profile, post_comment__id=obj.id
            )
        except PostCommentLike.DoesNotExist:
            return post_comment_like_obj

        return post_comment_like_obj.liked


class PostCommentLikeSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    post_comment = serializers.PrimaryKeyRelatedField(read_only=True, required=False)

    class Meta:
        model = PostCommentLike
        fields = (
            'id', 'created_at', 'updated_at',
            'post_comment',
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
            user=validated_data.get('user'), post_comment=validated_data.get('post_comment')
        ).exists():
            liked_obj = self.Meta.model.objects.get(
                user=validated_data.get('user'), post_comment=validated_data.get('post_comment')
            )
            liked_obj.liked = validated_data.get('liked')
            liked_obj.save()
        else:
            liked_obj = self.Meta.model.objects.create(**validated_data)

        return liked_obj
