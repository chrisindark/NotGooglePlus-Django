from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import FileUpload

@receiver(post_delete, sender=FileUpload)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding file object is deleted.
    """
    print(sender, instance, kwargs)
#    if instance.file:
#        if os.path.isfile(instance.file.path):
#            os.remove(instance.file.path)
