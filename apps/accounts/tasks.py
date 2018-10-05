from apps.profiles.models import Profile
from notgoogleplus.celery import app
from .models import Account


@app.task()
def create_user_profile(pk):
    account = Account.objects.get(pk=pk)
    account_profile = Profile.objects.get_or_create(user=account)
