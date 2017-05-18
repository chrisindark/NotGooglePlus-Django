# import os

from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import File


@receiver(post_delete, sender=File)
def auto_delete_media_file(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding file object is deleted.
    """
    print(sender, instance, kwargs)
#    if instance.file:
#        if os.path.isfile(instance.file.path):
#            os.remove(instance.file.path)
