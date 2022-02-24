from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .awsutility import (
    AwsUtility, content_file_path
)
# from .models import S3FileUpload


class ModelIdSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('id',)

    @staticmethod
    def get_id(obj):
        return obj

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


# class S3CreateFileSignatureSerializer(serializers.Serializer):
#     url = serializers.CharField(read_only=True)
#     fields = serializers.DictField(read_only=True)

#     class Meta:
#         fields = ()

#     def validate(self, data):
#         aws_utility = AwsUtility()

#         # presigned_post = aws_utility.get_presigned_post(key=content_file_path, expires_in=600)
#         # url = presigned_post['url']
#         # key = presigned_post['fields']['key']
#         # params = {
#         #     'AWSAccessKeyId': presigned_post['fields']['AWSAccessKeyId'],
#         #     'signature': presigned_post['fields']['signature'],
#         #     'policy': presigned_post['fields']['policy'],
#         # }
#         # from urllib.parse import urlencode
#         # presigned_post['url'] = url + '/' + key + '?' + urlencode(params)

#         # multipart_upload = aws_utility.get_multipart_upload(key=content_file_path, expires_in=600)
#         # print('\n'*2, '*'*2)
#         # print(multipart_upload)
#         # print('\n'*2, '*'*2)

#         presigned_url = {
#             'url': aws_utility.get_presigned_put_url(key=content_file_path, expires_in=9000),
#             'fields': {
#                 'key': content_file_path
#             }
#         }

#         # return presigned_post
#         return presigned_url

#     def create(self, validated_data):
#         pass

#     def update(self, instance, validated_data):
#         pass


# class S3UpdateFileSignatureSerializer(serializers.Serializer):
#     url = serializers.CharField(read_only=True)
#     fields = serializers.DictField(read_only=True)
#     key = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         fields = ()

#     def validate(self, data):
#         key = data.get('key')
#         aws_utility = AwsUtility()
#         presigned_url = {
#             'url': aws_utility.get_presigned_put_url(key=key, expires_in=600)
#         }

#         return presigned_url

#     def create(self, validated_data):
#         pass

#     def update(self, instance, validated_data):
#         pass


# class S3FileUploadSerializer(serializers.ModelSerializer):
#     file_name = serializers.CharField(max_length=255,)
#     file_size = serializers.IntegerField()
#     file_type = serializers.ChoiceField(
#         choices=('image', 'audio', 'video',),
#     )
#     file_content_type = serializers.ChoiceField(
#         choices=('image/jpeg', 'image/gif', 'image/png',
#                  'image/bmp', 'image/webp', 'audio/mpeg', 'audio/mp4',
#                  'audio/wav', 'audio/ogg', 'video/mp4', 'video/webm',
#                  'video/ogg', 'video/quicktime',)
#     )
#     key = serializers.CharField(max_length=255)
#     last_modified = serializers.DateTimeField(read_only=True, required=False)

#     class Meta:
#         model = S3FileUpload
#         fields = (
#             'id', 'file_name', 'file_size', 'file_type',
#             'file_content_type', 'key', 'last_modified',
#             'created_at', 'updated_at',
#         )
#         read_only_fields = ('created_at', 'updated_at',)

#     @staticmethod
#     def setup_eager_loading(queryset):
#         return queryset

    # def validate(self, data):
    #     key = data.get('key')
    #     file_name = data.get('file_name')
    #     file_size = data.get('file_size')
    #     file_content_type = data.get('file_content_type')
    #     aws_utility = AwsUtility()
    #     try:
    #         object_metadata = aws_utility.get_object_metadata(key=key)
    #     except Exception as e:
    #         raise NotFound

    #     if S3FileUpload.objects.filter(key=key).exists():
    #         raise serializers.ValidationError({'key': 'Key already exists.'})
    #     if key != file_name:
    #         raise serializers.ValidationError({'file_name': 'File name is not valid.'})
    #     if file_size != object_metadata['ContentLength']:
    #         raise serializers.ValidationError({'file_size': 'File content length is not valid.'})
    #     if file_content_type != object_metadata['ContentType']:
    #         raise serializers.ValidationError({'file': 'File content type is not valid.'})

    #     data['last_modified'] = object_metadata['LastModified']

    #     return data

    # def create(self, validated_data):
    #     self.create_thumbnail(validated_data)
    #     super(S3FileUploadSerializer, self).save()

    # def create_thumbnail(self, validated_data):
    #     aws_utility = AwsUtility()
    #     key = validated_data.get('key')
    #     try:
    #         object_metadata = aws_utility.get_object_metadata(key=key)
    #     except Exception as e:
    #         raise NotFound

    #     return validated_data


# class S3FileSignedSerializer(serializers.Serializer):
#     key = serializers.CharField(required=True)
#     url = serializers.CharField(read_only=True)

#     class Meta:
#         fields = ('url',)

#     def create(self, validated_data):
#         pass

#     def update(self, instance, validated_data):
#         pass

#     def validate(self, data):
#         key = data.get('key')
#         aws_utility = AwsUtility()
#         try:
#             object_metadata = aws_utility.get_object_metadata(key=key)
#         except Exception as e:
#             raise NotFound

#         data['url'] = aws_utility.get_presigned_get_url(key=key, expires_in=600)

#         return data
