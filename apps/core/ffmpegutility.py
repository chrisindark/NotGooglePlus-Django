import os
import subprocess
import traceback
from PIL import Image

from django.conf import settings


FFMPEG_BINARY_PATH = '/usr/bin/ffmpeg'
VIDEOSTREAM_SIZE = getattr(settings, 'VIDEOSTREAM_SIZE', '320x240')
VIDEOSTREAM_THUMBNAIL_SIZE = getattr(settings,
        'VIDEOSTREAM_THUMBNAIL_SIZE', '320x240')


class FFmpegUtility(object):
    ffmpeg_path = '/usr/bin/ffmpeg'
    # h.264 profile
    PROFILE = 'high'
    # encoding speed:compression ratio
    PRESET = 'fast'

    def __init__(self):
        pass

    def check_dir_exists(self, dirname):
        return os.path.isdir(os.path.join(settings.PROJECT_PATH, settings.MEDIA_PATH + dirname))

    def list_dir_files(self, dirpath):
        return os.listdir(os.path.join(
            settings.PROJECT_PATH,
            settings.MEDIA_PATH + settings.FILE_UPLOAD_PATH + dirpath
        ))

    def create_thumbnail(self, input_file, output_file):
        # command = ['/usr/bin/ffmpeg', '-i', input_file,
        #             '-vf', 'scale=400:-2', '-frames:v', '1', output_file]
        # subprocess.call(command)

        # ffmpeg command to create the thumbnail for a video
        get_thumb = [
            FFMPEG_BINARY_PATH, '-y', '-i', input_file, '-vframes', '1', '-ss',
            '00:00:02', '-an', '-vcodec', 'png', '-f', 'rawvideo', '-s',
            VIDEOSTREAM_THUMBNAIL_SIZE, output_file
        ]

        try:
            thumb_result = subprocess.call(get_thumb)
        except Exception as e:
            thumb_result = None
            print("Failed to generate thumbnail file for %s to %s" % (input_file, output_file))
            print(traceback.format_exc())
        print('/n' * 2)
        print(thumb_result)
        print('/n' * 2)

    def convert_to_mp4(self, input_file_path, output_file_path):
        get_mp4 = [
            FFMPEG_BINARY_PATH, '-i', input_file_path, '-map', '0', '-codec:v',
            'libx264', '-codec:a', 'libvo_aacenc', '-c:s', 'mov_text', output_file_path
        ]
        try:
            mp4_result = subprocess.call(get_mp4)
            print("FFMPEG_RESULT: %s" % mp4_result)
        except Exception as e:
            mp4_result = None
            print("Failed to convert video file %s to %s" % (input_file_path, output_file_path))
            print(traceback.format_exc())

        return mp4_result

    def convert_to_hls(self, input_file_path, output_file_path):
        get_hls = [
            FFMPEG_BINARY_PATH, '-i', input_file_path, '-map', '0', '-codec:v',
            'libx264', '-codec:a', 'libvo_aacenc', '-c:s', 'mov_text', '-f',
            'stream_segment', '-segment_list', output_file_path + 'playlist.m3u8', '-segment_list_flags',
            'live', '-segment_time', '10', output_file_path + 'out%03d.ts'
        ]
        try:
            hls_result = subprocess.call(get_hls)
        except Exception as e:
            hls_result = None
            print("Failed to generate hls video for %s to %s" % (input_file_path, output_file_path + 'playlist.m3u8'))

        return hls_result

    def create_thumbnail_from_image(self, input_file, output_file):
        # create a thumbnail for the file downloaded into the tmp folder
        # and return the thumbnail object
        im = Image.open(input_file)
        im.thumbnail((320, 240), Image.ANTIALIAS)
        im.save(output_file, "PNG")
        return
