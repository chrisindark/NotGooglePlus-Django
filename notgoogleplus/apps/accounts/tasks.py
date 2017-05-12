from notgoogleplus.celery import app
from notgoogleplus.apps.profiles.models import Profile

from .models import Account


@app.task()
def create_user_profile(pk):
    account = Account.objects.get(pk=pk)
    account_profile = Profile.objects.get_or_create(user=account)
