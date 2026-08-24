from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from apps.users.models import User


class UsernameOrEmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        if username is None or password is None:
            raise ValueError(
                "Both username and password are required for authentication."
            )
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            # override django's user.is_active check with 'allow_inactive' flag
            if kwargs.get("allow_inactive") or self.user_can_authenticate(user):
                if user.check_password(password):
                    return user
