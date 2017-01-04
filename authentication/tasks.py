from notgoogleplus.celery import app
from .models import Account, AccountProfile


@app.task()
def create_user_profile(user_id):
    account = Account.objects.get(pk=user_id)
    account_profile = AccountProfile.objects.get_or_create(user=account)
