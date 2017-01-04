# from django.contrib.auth import authenticate, login, logout
from rest_framework import (permissions, viewsets, generics,
    views, status, pagination)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import *
from .filters import *
from .permissions import *


class AccountPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    # max_page_size = 1000


class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountRegistrationSerializer
    permission_classes = (IsNotAuthenticated,)

    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return AccountRegistrationSerializer
    #     return AccountSerializer

    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return (IsNotAuthenticated(),)
    #     return (permissions.IsAuthenticated(), IsOwner(),)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer_class()(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # serializer.validated_data.pop('confirm_password', None)
        serializer.save()

    # def dispatch(self, request, *args, **kwargs):
    #     response = super(AccountCreateView, self).dispatch(request, *args, **kwargs)
    #     if response.data.get('id', None):
    #         response.data['success'] = 'Success!'
    #     else:
    #         response.data['error'] = 'Error!'
    #     return response


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated, IsAccountOwner,)

    # def dispatch(self, request, *args, **kwargs):
    #     response = super(AccountDetailView, self).dispatch(request, *args, **kwargs)
    #     if response.data.get('id', None):
    #         response.data['success'] = 'Success!'
    #     else:
    #         response.data['error'] = 'Error!'
    #     return response


class AccountProfileListView(generics.ListAPIView):
    queryset = AccountProfile.objects.all()
    serializer_class = AccountProfileSerializer
    permission_classes = (permissions.AllowAny,)


class AccountProfileDetailView(generics.RetrieveUpdateAPIView):
    lookup_field = 'user__username'
    queryset = AccountProfile.objects.all()
    serializer_class = AccountProfileSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)


class AuthenticatedUserView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        queryset = Account.objects.get(id=request.user.id)
        serializer = AccountSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class LoginView(views.APIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         email = form.get('email')
#         password = form.get('password')
#         if email == None or password == None:
#             return Response({
#                 'error': 'Bad Request',
#                 'message': 'Both fields are required.'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         account = authenticate(email=email, password=password)

#         if account is not None:
#             # if account.is_active:
#             login(request, account)
#             return Response({
#                 'success': 'Success!'
#             }, status=status.HTTP_200_OK)
#             # else:
#             #     return Response({
#             #         'status': 'Unauthorised',
#             #         'message': 'This account has been disabled.'
#             #     }, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response({
#                 'error': 'Unauthorised',
#                 'message': 'Username and password combination is invalid.'
#             }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token.delete()

        return Response({
            'success': 'Success!'
        }, status=status.HTTP_200_OK)


class PasswordChangeView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': 'Success!',
                'detail': 'New password has been saved.'
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(views.APIView):
    permission_classes = (IsNotAuthenticated,)

    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': 'Success!',
                'detail': 'Password reset email has been sent.'
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(views.APIView):
    permission_classes = (IsNotAuthenticated,)

    def post(self, request, format=None):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token = Token.objects.filter(user_id=serializer.user.id)
            if token:
                token.delete()
            return Response({
                'success': 'Success!',
                'detail': 'Password has been reset with the new password.'
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# import datetime
# from django.utils.timezone import utc
# from rest_framework.authentication import TokenAuthentication, get_authorization_header
# from rest_framework.exceptions import AuthenticationFailed

# EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 24)

# class ExpiringTokenAuthentication(TokenAuthentication):
#     def authenticate_credentials(self, key):
#         try:
#             token = self.model.objects.get(key=key)
#         except self.model.DoesNotExist:
#             raise exceptions.AuthenticationFailed('Invalid token')

#         if not token.user.is_active:
#             raise exceptions.AuthenticationFailed('User inactive or deleted')

#         # This is required for the time comparison
#         utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

#         if token.created < utc_now - datetime.timedelta(hours=EXPIRE_HOURS):
#             raise exceptions.AuthenticationFailed('Token has expired')

#         return (token.user, token)


# class ObtainExpiringAuthToken(ObtainAuthToken):
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])

#             utc_now = datetime.datetime.utcnow()
#             if not created and token.created < utc_now - datetime.timedelta(hours=24):
#                 token.delete()
#                 token = Token.objects.create(user=serializer.object['user'])
#                 token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
#                 token.save()

#             return Response({'token': token.key})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'authentication.ExpiringTokenAuthentication',
#     ),
# }
