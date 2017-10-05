import requests
import json

from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1

from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from notgoogleplus.apps.accounts.constants import (
    GOOGLE_ACCESS_TOKEN_URL, GOOGLE_PEOPLE_API_URL,
    TWITTER_REQUEST_TOKEN_URL, TWITTER_ACCESS_TOKEN_URL,
    TWITTER_PEOPLE_API_URL
)
from notgoogleplus.apps.accounts.utils import UserEmailManager
from notgoogleplus.apps.accounts.models import Account
from notgoogleplus.apps.core.exceptions import ServiceUnavailable


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
        read_only_fields = ()

    def validate(self, data):
        username = data.get('username')
        # Check that the username does not already exist
        if Account.objects.exclude(pk=self.instance.pk).filter(username=username).first():
            raise serializers.ValidationError({
                'username': 'Username already exists. Please try another.'
            })

        return data


class AuthenticatedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'is_active', 'is_staff', 'created_at', 'updated_at',)
        read_only_fields = ('username', 'email', 'is_active', 'is_staff', 'created_at', 'updated_at',)


class AccountRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=255)
    username = serializers.CharField(required=True, validators=[ALPHANUMERIC], max_length=20, min_length=8)
    password = serializers.CharField(write_only=True, required=True, max_length=128, min_length=8)
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
        # set user as inactive to allow verification of email
        user.is_active = True
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
        subject_template_name = settings.ACCOUNT_ACTIVATION_EMAIL_SUBJECT
        email_template_name = settings.ACCOUNT_ACTIVATION_EMAIL_TEMPLATE
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
        to_email = self.user.email
        context = {
            'url': settings.ACCOUNT_ACTIVATION_URL,
            'domain': settings.DOMAIN_URL,
            'site_name': settings.SITE_NAME,
            'user': self.user,
            'token': self.user.security_key,
            'protocol': 'https' if request.is_secure() else 'http'
        }

        UserEmailManager.send_email(subject_template_name, email_template_name,
                                    context, from_email, to_email)
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
    username = serializers.CharField(max_length=255, write_only=True, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('username', 'password', 'token',)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        username = data.get('username', None)
        password = data.get('password', None)
        request = self.context.get('request')

        account = authenticate(request=request, username=username, password=password, allow_inactive=True)
        if account is None:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        if not account.is_active:
            msg = 'The account has been deactivated.'
            raise serializers.ValidationError(msg, code='authorization')

        token, created = Token.objects.get_or_create(user=account)
        data['token'] = token

        return data


class JWTSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, write_only=True, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('username', 'password', 'token',)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        username = data.get('username', None)
        password = data.get('password', None)
        request = self.context.get('request')

        account = authenticate(request=request, username=username, password=password, allow_inactive=True)
        if account is None:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        if not account.is_active:
            msg = 'The account has been deactivated.'
            raise serializers.ValidationError(msg, code='authorization')

        data['token'] = account.token

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
        subject_template_name = settings.PASSWORD_RESET_EMAIL_SUBJECT
        email_template_name = settings.PASSWORD_RESET_EMAIL_TEMPLATE
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
        to_email = self.user.email
        context = {
            'url': settings.PASSWORD_RESET_CONFIRM_URL,
            'domain': settings.DOMAIN_URL,
            'site_name': settings.SITE_NAME,
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
            if not self.user.is_active:
                raise ValidationError('Account is not active.')
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


class GoogleOauthCallbackSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def get_access_token(self, data):
        access_token_url = GOOGLE_ACCESS_TOKEN_URL
        people_api_url = GOOGLE_PEOPLE_API_URL

        payload = dict(
            client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
            client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_OAUTH2_CALLBACK_URL,
            grant_type='authorization_code',
            code=data.get('code'),
        )

        # Step 1. Exchange authorization code for access token.
        req = None
        try:
            req = requests.post(access_token_url, data=payload)
        except requests.exceptions.Timeout as e:
            raise ServiceUnavailable()
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects as e:
            raise ServiceUnavailable()
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise ServiceUnavailable()

        res = json.loads(req.text)
        if req.status_code != 200:
            raise serializers.ValidationError(res)

        # Todo: Do something with the response for future use.
        print('\n' * 2)
        print(res)
        print('\n' * 2)

        # Step 2. Retrieve information about the current user.
        headers = {'Authorization': 'Bearer {0}'.format(res['access_token'])}
        try:
            req = requests.get(people_api_url, headers=headers)
        except requests.exceptions.Timeout as e:
            raise ServiceUnavailable()
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects as e:
            raise ServiceUnavailable()
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise ServiceUnavailable()

        res = json.loads(req.text)
        if req.status_code != 200:
            raise serializers.ValidationError(res)

        account = authenticate(email=res['emails'][0]['value'])
        if account is None:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        if not account.is_active:
            msg = 'The account has been deactivated.'
            raise serializers.ValidationError(msg, code='authorization')

        token, created = Token.objects.get_or_create(user=account)
        data['token'] = token

        return data

    def validate(self, data):
        data = self.get_access_token(data)

        return data


class TwitterOauthSerializer(serializers.Serializer):
    oauth_token = serializers.CharField(read_only=True)
    oauth_token_secret = serializers.CharField(read_only=True)
    oauth_callback_confirmed = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def get_request_token(self, data):
        request_token_url = TWITTER_REQUEST_TOKEN_URL

        oauth = OAuth1(
            settings.TWITTER_OAUTH_CONSUMER_KEY,
            client_secret=settings.TWITTER_OAUTH_CONSUMER_SECRET,
        )

        req = None
        try:
            req = requests.post(url=request_token_url, auth=oauth)
        except requests.exceptions.Timeout as e:
            raise ServiceUnavailable()
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects as e:
            raise ServiceUnavailable()
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise ServiceUnavailable()

        res = dict(parse_qsl(req.text))
        if req.status_code != 200:
            raise ServiceUnavailable()

        return res

    def validate(self, data):
        data = self.get_request_token(data)

        return data


class TwitterOauthCallbackSerializer(serializers.Serializer):
    oauth_verifier = serializers.CharField(write_only=True, required=True)
    oauth_token = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def get_access_token(self, data):
        access_token_url = TWITTER_ACCESS_TOKEN_URL
        people_api_url = TWITTER_PEOPLE_API_URL

        oauth = OAuth1(
            settings.TWITTER_OAUTH_CONSUMER_KEY,
            client_secret=settings.TWITTER_OAUTH_CONSUMER_SECRET,
            resource_owner_key=data.get('oauth_token'),
            verifier=data.get('oauth_verifier'),
        )

        # Step 1. Exchange oauth token and verifier for access token.
        req = None
        try:
            req = requests.post(url=access_token_url, auth=oauth)
        except requests.exceptions.Timeout as e:
            raise ServiceUnavailable()
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects as e:
            raise ServiceUnavailable()
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise ServiceUnavailable()

        res = dict(parse_qsl(req.text))
        if req.status_code != 200:
            # raise serializers.ValidationError(req.text)
            raise ServiceUnavailable()

        # Todo: Do something with the response for future use.
        print('\n' * 2)
        print(res)
        print('\n' * 2)

        oauth = OAuth1(
            settings.TWITTER_OAUTH_CONSUMER_KEY,
            client_secret=settings.TWITTER_OAUTH_CONSUMER_SECRET,
            resource_owner_key=res.get('oauth_token'),
            resource_owner_secret=res.get('oauth_token_secret'),
        )

        # Step 2. Retrieve information about the current user.
        req = None
        try:
            req = requests.get(url=people_api_url, auth=oauth, params={
                'include_email': 'true',
                'skip_status': 'true'
            })
        except requests.exceptions.Timeout as e:
            raise ServiceUnavailable()
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects as e:
            raise ServiceUnavailable()
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise ServiceUnavailable()

        res = json.loads(req.text)
        if req.status_code != 200:
            raise serializers.ValidationError(req.text)

        if not res['email']:
            msg = 'Email not provided or verified by Twitter. Please provide email to continue.'
            raise serializers.ValidationError(msg, code='authorization')

        account = authenticate(email=res['email'])

        if account is None:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        if not account.is_active:
            msg = 'The account has been deactivated.'
            raise serializers.ValidationError(msg, code='authorization')

        token, created = Token.objects.get_or_create(user=account)
        data['token'] = token

        return data

    def validate(self, data):
        data = self.get_access_token(data)

        return data
