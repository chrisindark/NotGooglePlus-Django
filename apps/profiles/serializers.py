import logging

from rest_framework import serializers

from apps.profiles.constants import (BIO_MAX_LENGTH, DATE_OF_BIRTH_DATE_FORMAT,
                                     NAME_MAX_LENGTH, NAME_MIN_LENGTH,
                                     TAGLINE_MAX_LENGTH)
from apps.users.serializers import UserSerializer
from apps.users.validators import ALPHABET_VALIDATOR

from .models import Gender, Profile

logger = logging.getLogger(__name__)


class BaseProfileSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("user")
        return queryset


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[ALPHABET_VALIDATOR],
        max_length=NAME_MAX_LENGTH,
        min_length=NAME_MIN_LENGTH,
    )
    last_name = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[ALPHABET_VALIDATOR],
        max_length=NAME_MAX_LENGTH,
        min_length=NAME_MIN_LENGTH,
    )

    class Meta:
        model = Profile
        fields = (
            "id",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "user_id",
        )
        read_only_fields = ("id", "created_at", "updated_at", "user_id")

    def validate(self, data):
        logger.info(f"Validating data: {data}")

        return data

    def save(self):
        pass


class AuthorizedProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[ALPHABET_VALIDATOR],
        max_length=NAME_MAX_LENGTH,
        min_length=NAME_MIN_LENGTH,
    )
    last_name = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[ALPHABET_VALIDATOR],
        max_length=NAME_MAX_LENGTH,
        min_length=NAME_MIN_LENGTH,
    )
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[ALPHABET_VALIDATOR],
        max_length=NAME_MAX_LENGTH,
        min_length=NAME_MIN_LENGTH,
    )
    date_of_birth = serializers.DateField(
        format=DATE_OF_BIRTH_DATE_FORMAT,
        input_formats=[DATE_OF_BIRTH_DATE_FORMAT, "iso-8601"],
        required=False,
        allow_null=True,
    )
    gender = serializers.ChoiceField(
        required=False, allow_blank=True, choices=Gender.choices
    )
    tagline = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=TAGLINE_MAX_LENGTH,
        min_length=NAME_MIN_LENGTH,
    )
    bio = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=BIO_MAX_LENGTH,
        min_length=NAME_MIN_LENGTH,
    )
    username = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)
    follower = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "first_name",
            "last_name",
            "nickname",
            "date_of_birth",
            "gender",
            "tagline",
            "bio",
            "created_at",
            "updated_at",
            "user_id",
            "username",
            "following",
            "follower",
        )
        read_only_fields = ("id", "created_at", "updated_at", "username", "user_id")

    def validate(self, data):
        pass

    def save(self):
        pass

    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user")
        if request is None and user is None:
            raise serializers.ValidationError("User is not authenticated.")

        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def get_following(self, instance):
        request = self.context.get("request")
        user = getattr(request, "user")
        if request is None and user is None:
            return None

        if not hasattr(user, "profile"):
            return False

        # instance is the object of the profile we are viewing
        # check if the profile we are viewing is followed
        # by the current logged in user
        followee = instance
        return user.profile.is_following(followee)

    def get_follower(self, instance):  # method to check follower count in profile mode
        request = self.context.get("request")
        user = getattr(request, "user")
        if request is None and user is None:
            return None

        if not hasattr(user, "profile"):
            return False

        return user.profile.is_follower(instance)

    def get_user(self, instance):
        request = self.context.get("request")
        user = getattr(request, "user")
        if request is None and user is None:
            return None

        # instance is the object of the user's profile we are viewing
        # if the profile being viewed is not of the current user, return None
        if user.id == instance.user_id:
            user_serializer = UserSerializer(user, context={"request": request})
            return user_serializer.data

    def get_username(self, instance):
        request = self.context.get("request")
        user = getattr(request, "user")
        if request is None and user is None:
            return None

        return user.username
