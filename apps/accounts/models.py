import jwt

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,
)


# Create your models here.
class AccountManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create an `Account`. 

    All we have to do is override the `create_user` function which we will use
    to create `Account` objects.
    """
    def create_user(self, username, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not username:
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email),
            username=username,
            **kwargs
        )
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, username, email, password, **kwargs):
        """
      Create and return a `User` with superuser powers.

      Superuser powers means that this user is an admin that can do anything
      they want.
      """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **kwargs)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(db_index=True, max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    security_key = models.CharField(max_length=40, null=True, blank=True)
    security_key_expires = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def is_admin(self):
        "Is the user an admin?"
        # Simplest possible answer: All superusers are admins
        return self.is_superuser

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        from datetime import datetime, timedelta
        from django.conf import settings

        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s')),
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def __str__(self):
        return self.email

    def __repr__(self):
        return '<User: {email}>'.format(email=self.email)


ACCOUNT_PERMISSION_CHOICES = (
    ('PUB', 'Public'),
    ('PVT', 'Private'),
    ('FRI', 'Friend'),
)


# class AccountDetailPermission(models.Model):
#     user = models.ForeignKey('Account')
#     email = models.CharField(max_length=3, choices=ACCOUNT_PERMISSION_CHOICES,
#                              default=ACCOUNT_PERMISSION_CHOICES[0][0])


# class OauthAccount(models.Model):
#     user = models.ForeignKey('accounts.Account', related_name='oauth', on_delete=models.CASCADE)
#     provider = models.CharField(max_length=32)
#     access_token = models.CharField(max_length=255)
#     refresh_token = models.CharField(max_length=255)
#     id_token = models.CharField(max_length=255)
#     expires_in = models.DateTimeField()
#     token_type = models.CharField(max_length=255)
