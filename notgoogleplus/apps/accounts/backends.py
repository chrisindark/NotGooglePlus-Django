from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import Account


class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(Account.USERNAME_FIELD)
        try:
            user = Account.objects.get(Q(username=username) | Q(email=username))
        except Account.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            Account().set_password(password)
        else:
            # override django's user.is_active check with 'allow_inactive' flag
            if kwargs.get('allow_inactive') or self.user_can_authenticate(user):
                if user.check_password(password):
                    return user


# import datetime

# from django.utils.timezone import utc

# from rest_framework.authentication import TokenAuthentication, get_authorization_header
# from rest_framework.exceptions import AuthenticationFailed

# EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 24)

# class ExpiringTokenAuthentication(TokenAuthentication):
#     def authenticate_credentials(self, key):
#         try:
#             token = self.model.objects.get(key=key)
#         except self.model.DoesNotExist:
#             raise exceptions.AuthenticationFailed('Invalid token')

#         if not token.user.is_active:
#             raise exceptions.AuthenticationFailed('User inactive or deleted')

#         # This is required for the time comparison
#         utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

#         if token.created < utc_now - datetime.timedelta(hours=EXPIRE_HOURS):
#             raise exceptions.AuthenticationFailed('Token has expired')

#         return (token.user, token)


# class ObtainExpiringAuthToken(ObtainAuthToken):
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])

#             utc_now = datetime.datetime.utcnow()
#             if not created and token.created < utc_now - datetime.timedelta(hours=24):
#                 token.delete()
#                 token = Token.objects.create(user=serializer.object['user'])
#                 token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
#                 token.save()

#             return Response({'token': token.key})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'notgoogleplus.apps.accounts.backends.ExpiringTokenAuthentication',
#     ),
# }
