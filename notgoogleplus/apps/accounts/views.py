from rest_framework import (permissions, generics,
                            views, status, pagination)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Account
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
        serializer.save()
        self.send_activation_email(serializer.data)

    def send_activation_email(self, user):
        serializer = AccountActivateSerializer(data=user, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
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


class AuthenticatedUserView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, request):
        queryset = Account.objects.get(id=request.user.id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountActivateView(views.APIView):
    permission_classes = (IsNotAuthenticated,)
    serializer_class = AccountActivateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': 'Success!',
                'detail': 'Account activation email has been sent.'
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountConfirmView(views.APIView):
    permission_classes = (IsNotAuthenticated,)
    serializer_class = AccountConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                'success': 'Success!',
                'detail': 'Your account has been activated.'
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    """
    Return a token after authenticating the user.
    """
    permission_classes = (IsNotAuthenticated,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
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
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
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
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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
