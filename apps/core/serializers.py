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
        # aws_utility = AwsS3Service()

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
        return data


#     def create(self, validated_data):
#         pass

#     def update(self, instance, validated_data):
#         pass
