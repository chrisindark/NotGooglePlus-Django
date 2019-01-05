from django.db import models

from apps.core.models import TimestampedModel


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)


class Profile(TimestampedModel):
    user = models.OneToOneField('accounts.Account', related_name='profile', on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=20, blank=True, default='')
    last_name = models.CharField(max_length=20, blank=True, default='')
    nickname = models.CharField(max_length=20, blank=True, default='')
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default='')
    tagline = models.CharField(max_length=140, blank=True, default='')
    bio = models.TextField(max_length=1000, blank=True, default='')
    follows = models.ManyToManyField('self', blank=True, related_name='followed_by', symmetrical=False)
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.email

    def __repr__(self):
        return '<UserProfile: {email}>'.format(email=self.user.email)

    def follow(self, profile):
        """Follow `profile` if we're not already following `profile`."""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile` if we're already following `profile`."""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Returns True if we're following `profile`; False otherwise."""
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        """Returns True if `profile` is following us; False otherwise."""
        return self.followed_by.filter(pk=profile.pk).exists()
