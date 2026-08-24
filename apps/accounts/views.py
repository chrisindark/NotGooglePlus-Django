# from rest_framework import serializers
# from rest_framework import (
#     generics,
#     views, status, pagination
# )
# from rest_framework.response import Response

# from apps.core.renderers import CustomJSONRenderer
# from .filters import *
# from ..users.permissions import *
# from .serializers import *


# class GoogleOauthCallbackView(generics.CreateAPIView):
#     permission_classes = (IsNotAuthenticated,)
#     serializer_class = GoogleOauthCallbackSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class TwitterOauthView(generics.CreateAPIView):
#     permission_classes = (IsNotAuthenticated,)
#     serializer_class = TwitterOauthSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class TwitterOauthCallbackView(generics.CreateAPIView):
#     permission_classes = (IsNotAuthenticated,)
#     serializer_class = TwitterOauthCallbackSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class GithubOauthCallbackSerializer(serializers.Serializer):
#     code = serializers.CharField(write_only=True, required=True)
#     token = serializers.CharField(read_only=True)

#     def create(self, validated_data):
#         pass

#     def update(self, instance, validated_data):
#         pass

#     def get_access_token(self, data):
#         access_token_url = GITHUB_ACCESS_TOKEN_URL
#         people_api_url = GITHUB_PEOPLE_API_URL

#         payload = dict(
#             client_id=settings.GITHUB_OAUTH2_CLIENT_ID,
#             client_secret=settings.GITHUB_OAUTH2_CLIENT_SECRET,
#             redirect_uri=settings.GITHUB_OAUTH2_CALLBACK_URL,
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
#         params = {'access_token': res['access_token']}
#         try:
#             req = requests.get(people_api_url, params=params)
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


# class GithubOauthCallbackView(generics.CreateAPIView):
#     permission_classes = (IsNotAuthenticated,)
#     serializer_class = GithubOauthCallbackSerializer


# class StripeOauthCallbackSerializer(serializers.Serializer):
#     code = serializers.CharField(write_only=True, required=True)
#     token = serializers.CharField(read_only=True)

#     def create(self, validated_data):
#         pass

#     def update(self, instance, validated_data):
#         pass

#     def get_access_token(self, data):
#         access_token_url = STRIPE_ACCESS_TOKEN_URL
#         people_api_url = STRIPE_PEOPLE_API_URL

#         payload = dict(
#             client_id=settings.STRIPE_OAUTH2_CLIENT_ID,
#             client_secret=settings.STRIPE_OAUTH2_CLIENT_SECRET,
#             redirect_uri=settings.STRIPE_OAUTH2_CALLBACK_URL,
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


# class StripeOauthCallbackView(generics.CreateAPIView):
#     permission_classes = (IsNotAuthenticated,)
#     serializer_class = StripeOauthCallbackSerializer
