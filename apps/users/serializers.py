import logging

from django.conf import settings
from django.db.models import F
from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.constants import (
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
)
from apps.users.models import User
from apps.users.utils import UserEmailManager
from apps.users.validators import ALPHANUMERIC_VALIDATOR

logger = logging.getLogger(__name__)


class BaseUserSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField(source="profile.id", read_only=True)
    # profile_id = serializers.IntegerField(read_only=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("profile")
        return queryset

    @staticmethod
    def annotate_profile_id(queryset):
        return queryset.annotate(profile_id=F("profile__id"))


class UserSerializer(serializers.ModelSerializer, BaseUserSerializer):
    username = serializers.CharField(
        required=False,
        validators=[ALPHANUMERIC_VALIDATOR],
        max_length=USERNAME_MAX_LENGTH,
        min_length=USERNAME_MIN_LENGTH,
    )

    class Meta:
        model = User
        fields = ("id", "username", "created_at", "updated_at", "profile_id")
        read_only_fields = ("id", "username", "created_at", "updated_at", "profile_id")

    def validate(self, data):
        request = self.context.get("request")

        if not request or not request.user:
            raise serializers.ValidationError("User is not authenticated.")

        # username = data.get("username")
        # # Check that the username does not already exist
        # if not self.instance:
        #     raise serializers.ValidationError(
        #         "User instance is required for validation."
        #     )

        # user = (
        #     User.objects.exclude(pk=self.instance.pk).filter(username=username).first()
        # )
        # if user is not None:
        #     raise serializers.ValidationError(
        #         {"username": "Username already exists. Please try another."}
        #     )

        return data

    def save(self):
        pass


class AuthorizedUserSerializer(serializers.ModelSerializer, BaseUserSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
            "profile_id",
        )
        read_only_fields = (
            "id",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
            "profile_id",
        )

    def validate(self, data):
        pass

    def save(self):
        pass


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=255)
    username = serializers.CharField(
        required=True,
        validators=[ALPHANUMERIC_VALIDATOR],
        max_length=USERNAME_MAX_LENGTH,
        min_length=USERNAME_MIN_LENGTH,
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        max_length=PASSWORD_MAX_LENGTH,
        min_length=PASSWORD_MIN_LENGTH,
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "confirm_password",
        )

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if (email == "") or (email is None):
            raise serializers.ValidationError({"email": "This field is required."})

        user = User.objects.filter(email=email).first()
        # Check that the email does not already exist
        if user is not None:
            raise serializers.ValidationError(
                {"email": "Email already exists. Was it you?"}
            )

        user = User.objects.filter(username=username).first()
        # Check that the username does not already exist
        if user is not None:
            raise serializers.ValidationError(
                {"username": "Username already exists. Please try another."}
            )

        # Check that the password entries match
        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords don't match."}
            )

        return data

    def create(self, validated_data):
        user = User(
            email=validated_data.get("email"), username=validated_data.get("username")
        )
        user.set_password(validated_data.get("password"))
        # set user is_active as false to allow verification of email
        user.is_active = True
        user.save()

        return user


class UserActivateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    user = None

    class Meta:
        model = User
        fields = ("email",)

    def validate(self, data):
        email = data.get("email", None)

        if (email == "") or (email is None):
            raise serializers.ValidationError({"email": "This field is required."})

        user = User.objects.get(email=email)

        if not user:
            raise serializers.ValidationError({"email": "Email does not exist."})

        self.user = user
        if self.user.is_active:
            raise serializers.ValidationError({"email": "User is already active."})

        return data

    def save(self, **kwargs):
        if not self.user:
            raise serializers.ValidationError("User instance is required for saving.")

        self.user.security_key, self.user.security_key_expires = (
            UserEmailManager.generate_activation_key()
        )
        subject_template_name = settings.USER_ACTIVATION_EMAIL_SUBJECT
        email_template_name = settings.USER_ACTIVATION_EMAIL_TEMPLATE
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL")
        to_email = self.user.email

        request = self.context.get("request")
        protocol = "http"
        if request is not None:
            protocol = "https" if request.is_secure() else "http"

        context = {
            "url": settings.USER_ACTIVATION_URL,
            "domain": settings.DOMAIN_URL,
            "site_name": settings.SITE_NAME,
            "user": self.user,
            "token": self.user.security_key,
            "protocol": protocol,
        }

        UserEmailManager.send_email(
            subject_template_name, email_template_name, context, from_email, to_email
        )
        self.user.save()

        return self.user


class UserActivationConfirmSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    token = serializers.CharField(write_only=True, required=True)

    user = None

    class Meta:
        model = User
        fields = (
            "email",
            "token",
        )

    def validate(self, data):
        email = data.get("email", None)
        token = data.get("token", None)

        if (email == "") or (email is None):
            raise serializers.ValidationError({"email": "This field is required."})

        user = User.objects.get(email=email, security_key=token)

        if not user:
            raise serializers.ValidationError({"token": "Token does not exist."})

        self.user = user
        if self.user.is_active:
            raise serializers.ValidationError({"email": "User is already active."})

        if self.user.security_key != data.get("token"):
            raise serializers.ValidationError({"token": "Invalid value"})

        return data

    def create(self, validated_data):
        if not self.user:
            raise serializers.ValidationError("User instance is required for saving.")

        self.user.is_active = True
        self.user.security_key = None
        self.user.security_key_expires = None
        self.user.save()

        return self.user


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        write_only=True, required=True, min_length=PASSWORD_MIN_LENGTH
    )
    new_password = serializers.CharField(
        write_only=True, required=True, min_length=PASSWORD_MIN_LENGTH
    )
    confirm_password = serializers.CharField(
        write_only=True, required=True, min_length=PASSWORD_MIN_LENGTH
    )

    class Meta:
        model = User
        fields = (
            "old_password",
            "new_password",
            "confirm_password",
        )

    def validate(self, data):
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        request = self.context.get("request")

        if not request or not request.user:
            raise serializers.ValidationError("User is not authenticated.")

        if not request.user.check_password(old_password):
            raise serializers.ValidationError(
                {
                    "old_password": "Your old password was entered incorrectly. Please enter it again."
                }
            )

        # Check that the password entries match
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords don't match."}
            )

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError("User is not authenticated.")
        user = request.user
        user.set_password(validated_data["new_password"])
        user.save()

        return user


class PasswordResetSerializer(serializers.ModelSerializer, UserEmailManager):
    email = serializers.EmailField(required=True)
    user = None

    class Meta:
        model = User
        fields = ("email",)

    def validate(self, data):
        email = data.get("email", None)

        if (email == "") or (email is None):
            raise serializers.ValidationError({"email": "This field is required."})

        user = User.objects.get(email=email)
        if not user:
            raise serializers.ValidationError({"email": "Email does not exist."})

        self.user = user
        if not self.user.is_active:
            msg = "The account has been deactivated."
            raise serializers.ValidationError(msg, code="authorization")

        return data

    def save(self):
        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError("User is not authenticated.")

        if not self.user:
            raise serializers.ValidationError("User instance is required for saving.")

        self.user.security_key, self.user.security_key_expires = (
            UserEmailManager.generate_activation_key()
        )
        subject_template_name = settings.PASSWORD_RESET_EMAIL_SUBJECT
        email_template_name = settings.PASSWORD_RESET_EMAIL_TEMPLATE
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL")
        to_email = self.user.email
        context = {
            "url": settings.PASSWORD_RESET_CONFIRM_URL,
            "domain": settings.DOMAIN_URL,
            "site_name": settings.SITE_NAME,
            "user": self.user,
            "token": self.user.security_key,
            "protocol": "https" if request.is_secure() else "http",
        }
        UserEmailManager.send_email(
            subject_template_name, email_template_name, context, from_email, to_email
        )
        self.user.save()

        return self.user


class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    token = serializers.CharField(write_only=True, required=True)

    user = None

    class Meta:
        model = User
        fields = (
            "new_password",
            "confirm_password",
            "token",
            "email",
        )

    def validate(self, data):
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        email = data.get("email", None)
        token = data.get("token", None)

        if (email == "") or (email is None):
            raise serializers.ValidationError({"email": "This field is required."})

        user = User.objects.get(email=email, security_key=token)

        if not user:
            raise serializers.ValidationError({"token": "Token does not exist."})

        self.user = user

        if not self.user:
            raise serializers.ValidationError("User instance is required for saving.")
        if not self.user.is_active:
            raise serializers.ValidationError("User is not active.")
        elif (
            self.user.security_key_expires
            and self.user.security_key_expires < timezone.now()
        ):
            raise serializers.ValidationError({"token": "Expired value"})

        # Check that the password entries match
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords don't match."}
            )

        return data

    def create(self, validated_data):
        if not self.user:
            raise serializers.ValidationError("User instance is required for saving.")

        self.user.set_password(validated_data["new_password"])
        self.user.security_key = None
        self.user.security_key_expires = None
        self.user.save()

        # delete the token for the user if it exists
        (count, tokens) = Token.objects.filter(user_id=self.user.id).delete()
        logger.debug(f"Tokens deleted count: ${count} and tokens: ${tokens}")

        return self.user
