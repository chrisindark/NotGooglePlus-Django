from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied

from .models import AppModel


@receiver(pre_save, sender=AppModel)
def check_app_model_save(sender, **kwargs):
    instance = kwargs.get('instance')
    if sender.objects.count() > 0 and instance.id is None:
        raise PermissionDenied('AppModel object already present. Try updating the object.')
