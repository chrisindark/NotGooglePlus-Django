from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Account, AccountProfile
from .tasks import create_user_profile

@receiver(post_save, sender=Account)
def create_profile_on_user_save(sender, **kwargs):
    """Creates user profile when a user is created
    successfully.
    """
    if kwargs.get('created', False):
        user = kwargs.get('instance')
        account_profile = AccountProfile.objects.get_or_create(user=user)

        # calling celery task to run in background
        # create_user_profile.apply_async(args=[user.id])
