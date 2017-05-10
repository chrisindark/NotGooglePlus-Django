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
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not username:
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email),
            username=username
        )
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, username, email, password):
        """
      Create and return a `User` with superuser powers.

      Superuser powers means that this use is an admin that can do anything
      they want.
      """
        account = self.create_user(username, email, password)
        account.is_superuser = True
        account.is_staff = True
        account.save()

        return account


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
