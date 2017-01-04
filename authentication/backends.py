# from django.db.models import Q
# from .models import Account

# class UsernameOrEmailBackend(object):
#     def authenticate(self, username=None, password=None, **kwargs):
#         try:
#            # Try to fetch the user by searching the username or email field
#             user = Account.objects.get(Q(username=username)|Q(email=username))
#             if user.check_password(password):
#                 return user
#         except MyUser.DoesNotExist:
#             # Run the default password hasher once to reduce the timing
#             # difference between an existing and a non-existing user (#20760).
#             Account().set_password(password)

# AUTHENTICATION_BACKENDS = ('path.to.UsernameOrEmailBackend',)
