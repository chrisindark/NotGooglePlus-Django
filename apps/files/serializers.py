from rest_framework import serializers

from apps.profiles.serializers import ProfileSerializer

from .models import FileUpload
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
        if data.get('file', None) is None:
            raise serializers.ValidationError({'file': 'No file was submitted.'})

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
            raise serializers.ValidationError({'file': 'File type should be of {0}'.format(
                ', '.join(ALLOWED_FILE_TYPES)
            )})
        return ALLOWED_FILE_TYPES[ALLOWED_FILE_TYPES.index(file.content_type.split('/')[0])]
