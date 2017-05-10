from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from notgoogleplus.apps.accounts.utils import UserEmailManager
from .models import Account

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
        fields = ('id', 'username',)
        read_only_fields = ('email', 'is_staff', 'created_at', 'updated_at',)

    def validate(self, data):
        username = data.get('username')
        # Check that the username does not already exist
        if Account.objects.exclude(pk=self.instance.pk).filter(username=username).first():
            raise serializers.ValidationError({
                'username': 'Username already exists. Please try another.'
            })
        return username


class AccountRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=255)
    username = serializers.CharField(required=True, validators=[ALPHANUMERIC], max_length=20, min_length=8)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('email', 'username', 'password', 'confirm_password',)

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
        user = Account(
            email=validated_data.get('email'),
            username=validated_data.get('username')
        )
        user.set_password(validated_data.get('password'))
        user.is_active = False
        user.save()
        return user


class AccountActivateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    user = None

    class Meta:
        model = Account
        fields = ('email',)

    def validate(self, data):
        email = data.get('email', None)
        if not Account.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'email': 'Email does not exist.'
            })

        self.user = Account.objects.get(email=email)
        if self.user.is_active:
            raise serializers.ValidationError({
                'email': 'Account is already active.'
            })

        return data

    def save(self, **kwargs):
        self.user.security_key, self.user.security_key_expires = UserEmailManager.generate_activation_key()
        request = self.context.get('request')
        subject_template_name = 'account_confirm_subject.txt'
        email_template_name = 'account_confirm_email.html'  # settings.ACCOUNT_ACTIVATION_EMAIL_TEMPLATE
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
        to_email = self.user.email
        context = {
            'url': '#/account/confirm',  # settings.ACCOUNT_CONFIRMATION_URL,
            'domain': '127.0.0.1:8000',  # settings.DOMAIN_URL,
            'site_name': 'NotGooglePlus',  # settings.SITE_NAME,
            'user': self.user,
            'token': self.user.security_key,
            'protocol': 'https' if request.is_secure() else 'http'
        }

        UserEmailManager.send_email(subject_template_name, email_template_name, context,
                                    from_email, to_email)
        self.user.save()
        return self.user


class AccountConfirmSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True, required=True)

    user = None

    class Meta:
        model = Account
        fields = ('token',)

    def validate(self, data):
        try:
            self.user = Account.objects.get(security_key=data['token'])
            if self.user.is_active:
                raise ValidationError('Account is already active.')
            # elif self.user.security_key_expires < datetime.now():
            #     raise ValidationError({'token': 'Expired value'})
        except Account.DoesNotExist:
            raise ValidationError({'token': 'Invalid value'})

        return data

    def create(self, validated_data):
        self.user.is_active = True
        self.user.security_key = None
        self.user.security_key_expires = None
        self.user.save()
        return self.user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('username', 'password', 'token',)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        account = authenticate(username=username, password=password, allow_inactive=True)
        if account is None:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        if not account.is_active:
            msg = 'The account has been deactivated.'
            raise serializers.ValidationError(msg, code='authorization')

        token, created = Token.objects.get_or_create(user=account)
        data['token'] = token

        return data


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


class PasswordResetSerializer(serializers.ModelSerializer, UserEmailManager):
    email = serializers.EmailField(required=True)

    user = None

    class Meta:
        model = Account
        fields = ('email',)

    def validate(self, data):
        email = data.get('email', None)
        if not Account.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'email': 'Email does not exist.'
            })

        self.user = Account.objects.get(email=email)
        if not self.user.is_active:
            msg = 'The account has been deactivated.'
            raise serializers.ValidationError(msg, code='authorization')

        return data

    def save(self):
        request = self.context.get('request')
        self.user.security_key, self.user.security_key_expires = UserEmailManager.generate_activation_key()
        subject_template_name = 'account_password_reset_subject.txt'  # settings.PASSWORD_RESET_EMAIL_SUBJECT
        email_template_name = 'account_password_reset_email.html'  # settings.PASSWORD_RESET_EMAIL_TEMPLATE
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
        to_email = self.user.email
        context = {
            'url': '#/password/reset/confirm',  # settings.PASSWORD_RESET_CONFIRM_URL,
            'domain': '127.0.0.1:8000',  # settings.DOMAIN_URL,
            'site_name': 'NotGooglePlus',  # settings.SITE_NAME,
            'user': self.user,
            'token': self.user.security_key,
            'protocol': 'https' if request.is_secure() else 'http'
        }

        UserEmailManager.send_email(subject_template_name, email_template_name, context,
                                    from_email, to_email)
        self.user.save()
        return self.user


class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(write_only=True, required=True)

    user = None

    class Meta:
        model = Account
        fields = ('new_password', 'confirm_password', 'token',)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        try:
            self.user = Account.objects.get(security_key=data['token'])
            if self.user.is_active:
                raise ValidationError('Account is already active.')
            # elif self.user.security_key_expires < datetime.now():
            #     raise ValidationError({'token': 'Expired value'})
        except Account.DoesNotExist:
            raise serializers.ValidationError({'token': 'Invalid value'})

        # Check that the password entries match
        if new_password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords don\'t match.'
            })

        return data

    def create(self, validated_data):
        user = self.user
        user.set_password(validated_data['new_password'])
        self.user.security_key = None
        self.user.security_key_expires = None
        user.save()
        return user
