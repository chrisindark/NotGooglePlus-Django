import os
import binascii

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from django.utils.text import slugify
from django.conf import settings

from notgoogleplus.apps.core.ffmpegutility import FFmpegUtility
from notgoogleplus.apps.core.sqsutility import SqsUtility

from .models import FileUpload, file_directory_path_fn
from .constants import (
    MAXIMUM_FILE_NAME_LENGTH,
)


@receiver(post_delete, sender=FileUpload)
def auto_delete_media_file(sender, instance, **kwargs):
    """
    Deletes file object from filesystem
    when corresponding file record is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


def set_filename(instance):
    filename_list = instance.file.name.split('.')
    file_extension = filename_list.pop()  # remove the extension from the filename_list
    filename_list = ''.join(filename_list)  # create the filename from the list
    slug = slugify(filename_list)  # slugify the filename
    unique = binascii.hexlify(os.urandom(20)).decode()

    if len(slug) > MAXIMUM_FILE_NAME_LENGTH:
        slug = slug[:MAXIMUM_FILE_NAME_LENGTH]

    while len(slug + '_' + unique + '.' + file_extension) > MAXIMUM_FILE_NAME_LENGTH:
        slug = slug[:MAXIMUM_FILE_NAME_LENGTH - len(unique + '.' + file_extension) - 1]
    # while len(slug + '_' + unique) > MAXIMUM_FILE_NAME_LENGTH:
    #     slug = slug[:MAXIMUM_FILE_NAME_LENGTH - len(unique) - 1]

    filename = slug + '_' + unique + '.' + file_extension
    # filename = slug + '_' + unique

    return filename


@receiver(pre_save, sender=FileUpload)
def check_file_pre_save(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.file_name:
        return

    instance.file_name = set_filename(instance)
    # instance.file is the property,
    # instance.file.file is the file object.
    instance.file_content_type = instance.file.file.content_type
    instance.file_size = instance.file.file.size
    instance.file_path = file_directory_path_fn(instance)

    return instance


@receiver(post_save, sender=FileUpload)
def check_file_post_save(sender, **kwargs):
    instance = kwargs.get('instance')

    # sqs_utility = SqsUtility()
    # sqs_queue = None
    # try:
    #     sqs_queue = sqs_utility.get_sqs_queue_url('test_queue')
    # except Exception as e:
    #     sqs_queue = sqs_utility.create_sqs_queue('test_queue')
    #
    # sqs_utility.send_message(sqs_queue['QueueUrl'])

    if instance.file_type == 'video':
        input_file_path = os.path.join(
            settings.PROJECT_PATH, instance.file_path + '/' + instance.file_name
        )
        output_file_path = os.path.join(
            settings.PROJECT_PATH, instance.file_path + '/'
        )
        ffmpeg_utility = FFmpegUtility()
        hls_result = ffmpeg_utility.convert_to_hls(input_file_path, output_file_path)
        print('\n'*2)
        print(hls_result)
        print('\n' * 2)
    elif instance.file_type == 'image':
        input_file_path = os.path.join(
            settings.PROJECT_PATH, instance.file_path + '/' + instance.file_name
        )
        output_file_path = os.path.join(
            settings.PROJECT_PATH, settings.MEDIA_PATH + settings.FILE_THUMBNAIL_PATH + instance.file_name
        )
        ffmpeg_utility = FFmpegUtility()
        if not ffmpeg_utility.check_dir_exists(output_file_path):
            os.makedirs(output_file_path)
        ffmpeg_utility.create_thumbnail_from_image(input_file_path, output_file_path + '/' + instance.file_name + '.png')

    return instance
