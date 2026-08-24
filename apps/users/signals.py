import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_profile_on_user_save(sender, **kwargs):
    """Creates user profile when a user is created
    successfully.
    """
    if kwargs.get("created", False):
        user = kwargs.get("instance", None)
        if user is not None:
            logger.debug("")
            # create_user_profile(user.pk)
            # calling celery task to run in background
            # create_user_profile.apply_async(args=[user.pk])
            pass
