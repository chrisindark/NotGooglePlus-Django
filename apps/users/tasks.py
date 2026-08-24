from apps.profiles.models import Profile

from .models import User


# @app.task()
def create_user_profile(pk):
    user = User.objects.get(pk=pk)
    (user_profile, created) = Profile.objects.get_or_create(user=user)
    return user_profile
