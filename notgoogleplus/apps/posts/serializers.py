from django.utils.crypto import get_random_string

from rest_framework import serializers

from notgoogleplus.apps.profiles.serializers import ProfileSerializer

from .models import *


class FileSerializer(serializers.ModelSerializer):
    # user = ProfileSerializer(read_only=True, required=False)

    class Meta:
        model = File
        fields = ('id', 'file', 'name', 'file_type', 'file_content_type', 'size', 'created_at', 'updated_at', 'user',)
        read_only_fields = ('name', 'file_type', 'file_content_type', 'size', 'created_at', 'updated_at',)

    def validate(self, data):
        if len(data['file'].name) > 75:
            raise serializers.ValidationError({
                'file': 'File name should be less than or equal to 75 characters.'
            })
        data['name'] = self.set_filename(data['file'])

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
        data['file_content_type'] = data['file'].content_type
        data['size'] = data['file'].size
        return data

    @staticmethod
    def set_filename(file):
        filename_list = file.name.lower().replace(' ', '_').split('.')
        ext = filename_list.pop()
        filename = ''.join(filename_list) + get_random_string(25) + '.' + ext
        return filename

    @staticmethod
    def get_filetype(file):
        if file.content_type.split('/')[0] not in ALLOWED_FILE_TYPES:
            raise serializers.ValidationError({'file': 'File type should be of {0}'.format(', '.join(ALLOWED_FILE_TYPES))})
        return ALLOWED_FILE_TYPES[ALLOWED_FILE_TYPES.index(file.content_type.split('/')[0])]


class PostSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    file = FileSerializer(required=False)

    class Meta:
        model = Post
        fields = ('id', 'content', 'created_at', 'updated_at', 'user', 'file',)
        read_only_fields = ('created_at', 'updated_at',)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user')
        return queryset

    # def to_representation(self, obj):
    #     obj = super(PostSerializer, self).to_representation(obj)
    #     depth = self.context.get('request').query_params.get('depth')
    #     if depth != '1':
    #         obj.pop('user')

    #     return obj


class PostCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True, required=False)
    post = PostSerializer(read_only=True, required=False)

    class Meta:
        model = PostComment
        fields = ('id', 'content', 'created_at', 'updated_at', 'post', 'user',)
        read_only_fields = ('created_at', 'updated_at',)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user')
        return queryset


ALLOWED_FILE_TYPES = ('image', 'audio', 'video',)
ALLOWED_IMAGE_TYPES = ('image/jpeg', 'image/gif', 'image/png',
                       'image/bmp', 'image/webp',)
ALLOWED_AUDIO_TYPES = ('audio/mpeg', 'audio/mp4', 'audio/wav', 'audio/ogg',)
ALLOWED_VIDEO_TYPES = ('video/mp4', 'video/webm', 'video/ogg',)



