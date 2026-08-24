# import json
# import requests

# from urllib.parse import parse_qsl

# from django.conf import settings
# from django.contrib.auth import authenticate
# from django.core.validators import RegexValidator

# from rest_framework import serializers
# from rest_framework.authtoken.models import Token
# from rest_framework.exceptions import ValidationError

# # from requests_oauthlib import OAuth1

# from apps.accounts.models import Account
# from apps.users.utils import UserEmailManager
# from apps.core.exceptions import ServiceUnavailable

# from apps.accounts.constants import (
#     GOOGLE_ACCESS_TOKEN_URL, GOOGLE_PEOPLE_API_URL,
#     TWITTER_REQUEST_TOKEN_URL, TWITTER_ACCESS_TOKEN_URL,
#     TWITTER_PEOPLE_API_URL
# )


# class GoogleOauthCallbackSerializer(serializers.Serializer):
#     code = serializers.CharField(write_only=True, required=True)
#     token = serializers.CharField(read_only=True)

#     def create(self, validated_data):
#         pass

#     def update(self, instance, validated_data):
#         pass

#     def get_access_token(self, data):
#         access_token_url = GOOGLE_ACCESS_TOKEN_URL
#         people_api_url = GOOGLE_PEOPLE_API_URL

#         payload = dict(
#             client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
#             client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
#             redirect_uri=settings.GOOGLE_OAUTH2_CALLBACK_URL,
#             grant_type='authorization_code',
#             code=data.get('code'),
#         )

#         # Step 1. Exchange authorization code for access token.
#         req = None
#         try:
#             req = requests.post(access_token_url, data=payload)
#         except requests.exceptions.Timeout as e:
#             raise ServiceUnavailable()
#             # Maybe set up for a retry, or continue in a retry loop
#         except requests.exceptions.TooManyRedirects as e:
#             raise ServiceUnavailable()
#             # Tell the user their URL was bad and try a different one
#         except requests.exceptions.RequestException as e:
#             # catastrophic error. bail.
#             raise ServiceUnavailable()

#         res = json.loads(req.text)
#         if req.status_code != 200:
#             raise serializers.ValidationError(res)

#         # Todo: Do something with the response for future use.
#         print('\n' * 2)
#         print(res)
#         print('\n' * 2)

#         # Step 2. Retrieve information about the current user.
#         headers = {'Authorization': 'Bearer {0}'.format(res['access_token'])}
#         try:
#             req = requests.get(people_api_url, headers=headers)
#         except requests.exceptions.Timeout as e:
#             raise ServiceUnavailable()
#             # Maybe set up for a retry, or continue in a retry loop
#         except requests.exceptions.TooManyRedirects as e:
#             raise ServiceUnavailable()
#             # Tell the user their URL was bad and try a different one
#         except requests.exceptions.RequestException as e:
#             # catastrophic error. bail.
#             raise ServiceUnavailable()

#         res = json.loads(req.text)
#         if req.status_code != 200:
#             raise serializers.ValidationError(res)

#         account = authenticate(email=res['emails'][0]['value'])
#         if account is None:
#             msg = 'Unable to log in with provided credentials.'
#             raise serializers.ValidationError(msg, code='authorization')

#         if not account.is_active:
#             msg = 'The account has been deactivated.'
#             raise serializers.ValidationError(msg, code='authorization')

#         token, created = Token.objects.get_or_create(user=account)
#         data['token'] = token

#         return data

#     def validate(self, data):
#         data = self.get_access_token(data)

#         return data


# class TwitterOauthSerializer(serializers.Serializer):
#     oauth_token = serializers.CharField(read_only=True)
#     oauth_token_secret = serializers.CharField(read_only=True)
#     oauth_callback_confirmed = serializers.BooleanField(read_only=True)

#     def create(self, validated_data):
#         pass

#     def update(self, instance, validated_data):
#         pass

#     def get_request_token(self, data):
#         request_token_url = TWITTER_REQUEST_TOKEN_URL

#         oauth = OAuth1(
#             settings.TWITTER_OAUTH_CONSUMER_KEY,
#             client_secret=settings.TWITTER_OAUTH_CONSUMER_SECRET,
#         )

#         req = None
#         try:
#             req = requests.post(url=request_token_url, auth=oauth)
#         except requests.exceptions.Timeout as e:
#             raise ServiceUnavailable()
#             # Maybe set up for a retry, or continue in a retry loop
#         except requests.exceptions.TooManyRedirects as e:
#             raise ServiceUnavailable()
#             # Tell the user their URL was bad and try a different one
#         except requests.exceptions.RequestException as e:
#             # catastrophic error. bail.
#             raise ServiceUnavailable()

#         res = dict(parse_qsl(req.text))
#         if req.status_code != 200:
#             raise ServiceUnavailable()

#         return res

#     def validate(self, data):
#         data = self.get_request_token(data)

#         return data


# class TwitterOauthCallbackSerializer(serializers.Serializer):
#     oauth_verifier = serializers.CharField(write_only=True, required=True)
#     oauth_token = serializers.CharField(write_only=True, required=True)
#     token = serializers.CharField(read_only=True)

#     def create(self, validated_data):
#         pass

#     def update(self, instance, validated_data):
#         pass

#     def get_access_token(self, data):
#         access_token_url = TWITTER_ACCESS_TOKEN_URL
#         people_api_url = TWITTER_PEOPLE_API_URL

#         oauth = OAuth1(
#             settings.TWITTER_OAUTH_CONSUMER_KEY,
#             client_secret=settings.TWITTER_OAUTH_CONSUMER_SECRET,
#             resource_owner_key=data.get('oauth_token'),
#             verifier=data.get('oauth_verifier'),
#         )

#         # Step 1. Exchange oauth token and verifier for access token.
#         req = None
#         try:
#             req = requests.post(url=access_token_url, auth=oauth)
#         except requests.exceptions.Timeout as e:
#             raise ServiceUnavailable()
#             # Maybe set up for a retry, or continue in a retry loop
#         except requests.exceptions.TooManyRedirects as e:
#             raise ServiceUnavailable()
#             # Tell the user their URL was bad and try a different one
#         except requests.exceptions.RequestException as e:
#             # catastrophic error. bail.
#             raise ServiceUnavailable()

#         res = dict(parse_qsl(req.text))
#         if req.status_code != 200:
#             # raise serializers.ValidationError(req.text)
#             raise ServiceUnavailable()

#         # Todo: Do something with the response for future use.
#         print('\n' * 2)
#         print(res)
#         print('\n' * 2)

#         oauth = OAuth1(
#             settings.TWITTER_OAUTH_CONSUMER_KEY,
#             client_secret=settings.TWITTER_OAUTH_CONSUMER_SECRET,
#             resource_owner_key=res.get('oauth_token'),
#             resource_owner_secret=res.get('oauth_token_secret'),
#         )

#         # Step 2. Retrieve information about the current user.
#         req = None
#         try:
#             req = requests.get(url=people_api_url, auth=oauth, params={
#                 'include_email': 'true',
#                 'skip_status': 'true'
#             })
#         except requests.exceptions.Timeout as e:
#             raise ServiceUnavailable()
#             # Maybe set up for a retry, or continue in a retry loop
#         except requests.exceptions.TooManyRedirects as e:
#             raise ServiceUnavailable()
#             # Tell the user their URL was bad and try a different one
#         except requests.exceptions.RequestException as e:
#             # catastrophic error. bail.
#             raise ServiceUnavailable()

#         res = json.loads(req.text)
#         if req.status_code != 200:
#             raise serializers.ValidationError(req.text)

#         if not res['email']:
#             msg = 'Email not provided or verified by Twitter. Please provide email to continue.'
#             raise serializers.ValidationError(msg, code='authorization')

#         account = authenticate(email=res['email'])

#         if account is None:
#             msg = 'Unable to log in with provided credentials.'
#             raise serializers.ValidationError(msg, code='authorization')

#         if not account.is_active:
#             msg = 'The account has been deactivated.'
#             raise serializers.ValidationError(msg, code='authorization')

#         token, created = Token.objects.get_or_create(user=account)
#         data['token'] = token

#         return data

#     def validate(self, data):
#         data = self.get_access_token(data)

#         return data
