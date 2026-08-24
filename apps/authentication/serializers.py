from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.common.jwt import JWT
from apps.users.constants import (
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
)
from apps.users.models import User


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
        write_only=True,
        required=True,
    )
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "token",
        )

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        username = data.get("username", None)
        password = data.get("password", None)
        request = self.context.get("request")

        user = authenticate(
            request=request, username=username, password=password, allow_inactive=True
        )
        if user is None:
            msg = "Unable to log in with provided credentials."
            raise serializers.ValidationError(msg, code="authorization")

        if not user.is_active:
            msg = "The user has been deactivated."
            raise serializers.ValidationError(msg, code="authorization")

        token, created = Token.objects.get_or_create(user=user)
        data["token"] = token

        return data

    def save(self):
        pass


class JWTSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
        write_only=True,
        required=True,
    )
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "token",
        )

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        username = data.get("username", None)
        password = data.get("password", None)
        request = self.context.get("request")

        user = authenticate(
            request=request, username=username, password=password, allow_inactive=True
        )
        if user is None:
            msg = "Unable to log in with provided credentials."
            raise serializers.ValidationError(msg, code="authorization")

        if not user.is_active:
            msg = "The user has been deactivated."
            raise serializers.ValidationError(msg, code="authorization")

        data["token"] = JWT(settings.SECRET_KEY).encode(user)

        return data

    def save(self):
        pass
