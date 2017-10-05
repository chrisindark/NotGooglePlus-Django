from django.utils.translation import ugettext as _

CONTENT_UPLOAD_PATH = 'content/'
CONTENT_PREVIEW_UPLOAD_PATH = 'content_preview/'
CONTENT_THUMBNAIL_UPLOAD_PATH = 'content_thumbnails/'

CONTENT_TYPE_VIDEO = 1
CONTENT_TYPE_AUDIO = 2
CONTENT_TYPE_IMAGE = 3

CONTENT_TYPE_CHOICES = (
    (CONTENT_TYPE_VIDEO, _('Video')),
    (CONTENT_TYPE_AUDIO, _('Audio')),
    (CONTENT_TYPE_IMAGE, _('Image'))
)

PREVIEW_FILE = 1
CONTENT_FILE = 2
S3_UPLOAD_FILE_TYPE_CHOICES = (
    (PREVIEW_FILE, "Preview File"),
    (CONTENT_FILE, "Content File")
)

VIDEO_LESS_THAN_5_MINUTES = 1
VIDEO_GREATER_THAN_5_LESS_THAN_10 = 2
VIDEO_GREATER_THAN_10 = 3
VIDEO_GREATER_THAN_60 = 4
VIDEO_LENGTH_CHOICES = (
    (VIDEO_LESS_THAN_5_MINUTES, _('Less than 5 minutes')),
    (VIDEO_GREATER_THAN_5_LESS_THAN_10, _('Between 5 and 10 minutes')),
    (VIDEO_GREATER_THAN_10, _('Greater than 10 minutes')),
    (VIDEO_GREATER_THAN_60, _('Greater than 1 hour'))
)

THUMBNAIL_SIZES = {

}

CONTENT_STATUS_PAID = 1
CONTENT_STATUS_PAID_OUT = 2
CONTENT_STATUS_DISPUTED = 3
CONTENT_STATUS_NOT_PAID = 4

CONTENT_DOWNLOAD_STATUS_CHOICES = (
    (CONTENT_STATUS_PAID, _('Paid')),
    (CONTENT_STATUS_PAID_OUT, _('Paid Out')),
    (CONTENT_STATUS_DISPUTED, _('Disputed')),
    (CONTENT_STATUS_NOT_PAID, _('Not Paid')),
)