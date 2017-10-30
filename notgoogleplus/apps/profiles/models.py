from django.db import models


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)


class Profile(models.Model):
    user = models.OneToOneField('accounts.Account', on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=20, blank=True, default='')
    last_name = models.CharField(max_length=20, blank=True, default='')
    nickname = models.CharField(max_length=20, blank=True, default='')
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default='')
    tagline = models.CharField(max_length=140, blank=True, default='')
    bio = models.TextField(max_length=1000, blank=True, default='')
    # image = models.URLField(blank=True)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

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