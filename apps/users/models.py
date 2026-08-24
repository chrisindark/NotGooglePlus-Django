from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create an `Account`.

    All we have to do is override the `create_user` function which we will use
    to create `Account` objects.
    """

    def create_user(self, username, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have a valid email address.")

        if not username:
            raise ValueError("Users must have a valid username.")

        user = self.model(
            email=self.normalize_email(email), username=username, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """
        Create and return a `User` with superuser powers.

        Superuser powers means that this user is an admin that can do anything
        they want.
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(db_index=True, max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    security_key = models.CharField(max_length=40, null=True, blank=True)
    security_key_expires = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    @property
    def is_user_staff(self):
        "Is the user a member of staff?"
        return self.is_staff
