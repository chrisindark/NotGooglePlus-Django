# from django.contrib.auth.backends import ModelBackend

# from .models import Account


# class OauthBackend(ModelBackend):
#     def authenticate(self, request, email=None, **kwargs):
#         if email is not None:
#             # Todo: return 'account' on checking some other parameter
#             try:
#                 # Try to find a user matching the email provided
#                 account = Account.objects.get(email=email)
#                 # If password is sent in request, do not authenticate with oauth
#                 if not kwargs.get("password"):
#                     return account
#             except Account.DoesNotExist:
#                 account = Account.objects.create_user(email=email)
#                 return account

#     # Required for your backend to work properly - unchanged in most scenarios
#     def get_user(self, user_id):
#         try:
#             return Account.objects.get(pk=user_id)
#         except Account.DoesNotExist:
#             return None


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
