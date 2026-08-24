from django.db import models

from apps.common.models import TimestampedModel
from apps.profiles.constants import BIO_MAX_LENGTH, NAME_MAX_LENGTH, TAGLINE_MAX_LENGTH


class Gender(models.IntegerChoices):
    UNKNOWN = 0, "Unknown"
    MALE = 1, "Male"
    FEMALE = 2, "Female"
    OTHER = 3, "Other"
    PREFER_NOT_TO_SAY = 4, "Prefer not to say"


class Profile(TimestampedModel):
    user = models.OneToOneField(
        "users.User", related_name="profile", on_delete=models.DO_NOTHING
    )
    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        blank=True,
    )
    nickname = models.CharField(
        max_length=NAME_MAX_LENGTH,
        blank=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(
        choices=Gender.choices, null=True, blank=True, default=Gender.UNKNOWN
    )
    tagline = models.CharField(max_length=TAGLINE_MAX_LENGTH, blank=True)
    bio = models.TextField(
        max_length=BIO_MAX_LENGTH,
        blank=True,
    )
    follows = models.ManyToManyField(
        "self", blank=True, related_name="followed_by", symmetrical=False
    )
    image = models.URLField(null=True, blank=True)

    def follow(self, profile):
        """Follow `profile` if we're not already following `profile`."""
        if profile == self:
            return
        if not self.is_following(profile):
            return
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile` if we're already following `profile`."""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Returns True if we're following `profile`; False otherwise."""
        return self.follows.filter(pk=profile.pk).exists()

    def is_follower(self, profile):
        """Return True if we're a follower of `profile`; False otherwise."""
        return profile.follows.filter(pk=self.pk).exists()

    @property
    def following_count(self):
        """The number of people who follow this user."""
        return self.follows.count()
