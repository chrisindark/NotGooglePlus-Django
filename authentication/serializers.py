from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.encoding import force_text
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.validators import RegexValidator
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Account, AccountProfile


MIN_LENGTH = 8
MAX_LENGTH = 20
ALPHABET = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')
ALPHANUMERIC = RegexValidator(
    r'^[a-z][a-z0-9]*$',
    'Only lowercase letters and numbers are allowed. Value should start with a letter.'
)


class AccountSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(read_only=True, required=False)
    username = serializers.CharField(required=False, validators=[ALPHANUMERIC], max_length=20, min_length=8)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',)
        read_only_fields = ('email', 'is_admin', 'created_at', 'updated_at',)

    def validate_username(self, username):
        # Check that the username does not already exist
        if Account.objects.exclude(pk=self.instance.pk).filter(username=username).first():
            raise serializers.ValidationError('Username already exists. Please try another.')
        return username


class AccountRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=255)
    username = serializers.CharField(required=True, validators=[ALPHANUMERIC], max_length=20, min_length=8)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'password', 'confirm_password',)

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Check that the email does not already exist
        if Account.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'email': 'Email already exists. Was it you?'
            })

        # Check that the username does not already exist
        if Account.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                'username': 'Username already exists. Please try another.'
            })

        # Check that the password entries match
        if password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords don\'t match.'
            })
        return data

    def create(self, validated_data):
        print("awesome")
        user = Account(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('old_password', 'new_password', 'confirm_password',)

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        request = self.context.get('request')

        if not request.user.check_password(old_password):
            raise serializers.ValidationError({
                'old_password': 'Your old password was entered incorrectly. Please enter it again.'
            })

        # Check that the password entries match
        if new_password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords don\'t match.'
            })
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data['new_password'])
        user.save()
        return user


class PasswordResetSerializer(serializers.ModelSerializer):
    password_reset_form_class = PasswordResetForm

    email = serializers.EmailField(required = True)

    class Meta:
        model = Account
        fields = ('email',)

    def validate_email(self, email):
        # Create PasswordResetForm with the serializer
        self.reset_password_form = self.password_reset_form_class(data=self.initial_data)

        if not self.reset_password_form.is_valid():
            raise serializers.ValidationError(self.reset_password_form.errors)
        if not Account.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')
        return email

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        extra_email_context = {
            'url': settings.PASSWORD_RESET_CONFIRM_URL
        }

        self.reset_password_form.save(
            extra_email_context=extra_email_context,
            email_template_name=settings.PASSWORD_RESET_EMAIL_TEMPLATE,
            **opts)


class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)
    uid = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(write_only=True, required=True)

    set_password_form_class = SetPasswordForm

    class Meta:
        model = Account
        fields = ('new_password', 'confirm_password','uid', 'token',)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        # Decode the uid to get User object id
        try:
            uid = force_text(uid_decoder(data['uid']))
            self.user = Account._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.set_password_form = self.set_password_form_class(user=self.user, data=data)

        if not default_token_generator.check_token(self.user, data['token']):
            raise ValidationError({'token': ['Invalid value']})
        # if not self.set_password_form.is_valid():
        #     raise serializers.ValidationError(self.set_password_form.errors)
        # Check that the password entries match
        if new_password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords don\'t match.'
            })

        return data

    def create(self, validated_data):
        user = self.user
        user.set_password(validated_data['new_password'])
        user.save()
        return user


class AccountProfileSerializer(serializers.ModelSerializer):
    # user = AccountSerializer(read_only=True, required=False)
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True, validators=[ALPHABET], max_length=20)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True, validators=[ALPHABET], max_length=20)
    nickname = serializers.CharField(required=False, allow_null=True, allow_blank=True, validators=[ALPHABET], max_length=20)
    tagline = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=140)
    bio = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=1000)

    class Meta:
        model = AccountProfile
        fields = ('id', 'first_name', 'last_name', 'nickname', 'tagline', 'bio', 'dob', 'gender', 'user',)
        read_only_fields = ('user',)


# class DynamicModelSerializer(serializers.ModelSerializer):
# """
# A ModelSerializer that takes an additional `fields` argument that
# controls which fields should be displayed, and takes in a "nested"
# argument to return nested serializers
# """

# def __init__(self, *args, **kwargs):
#     fields = kwargs.pop("fields", None)
#     exclude = kwargs.pop("exclude", None)
#     nest = kwargs.pop("nest", None)

#     if nest is not None:
#         if nest == True:
#             self.Meta.depth = 1

#     super(DynamicModelSerializer, self).__init__(*args, **kwargs)

#     if fields is not None:
#         # Drop any fields that are not specified in the `fields` argument.
#         allowed = set(fields)
#         existing = set(self.fields.keys())
#         for field_name in existing - allowed:
#             self.fields.pop(field_name)

#     if exclude is not None:
#         for field_name in exclude:
#             self.fields.pop(field_name)
