from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email),
            username=kwargs.get('username'),
        )
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_superuser = True
        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # return self.first_name + ' ' + self.last_name
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def is_staff(self):
        return self.is_admin

    def __unicode__(self):
        return self.email

    def __repr__(self):
        return '<User: {email}>'.format(email=self.email)


GENDER_CHOICES = (
('M', 'Male'),
('F', 'Female'),
('O', 'Other'),
)


class AccountProfile(models.Model):
    user = models.OneToOneField('Account', related_name='profile')
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    tagline = models.CharField(max_length=140, null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    # followers = models.ManyToManyField('self', related_name='followees', symmetrical=False)

    def __str__(self):
        return self.user.email

    def __repr__(self):
        return '<UserProfile: {email}>'.format(email=self.user.email)
