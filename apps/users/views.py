import logging

from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.profiles.models import Profile
from apps.users.models import User
from apps.users.pagination import UserPagination
from apps.users.permissions import IsUserNotAuthenticated, IsUserOwner
from apps.users.serializers import (AuthorizedUserSerializer,
                                    PasswordChangeSerializer,
                                    PasswordResetConfirmSerializer,
                                    PasswordResetSerializer,
                                    UserActivateSerializer,
                                    UserActivationConfirmSerializer,
                                    UserRegistrationSerializer, UserSerializer)

logger = logging.getLogger(__name__)


class UserMixin(generics.GenericAPIView):
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def get_queryset(self):
        if hasattr(self.serializer_class, "setup_eager_loading"):
            queryset = self.serializer_class.setup_eager_loading(self.queryset)
        # if hasattr(self.serializer_class, "annotate_profile_id"):
        #     queryset = self.serializer_class.annotate_profile_id(self.queryset)
        return queryset


class UserListCreateView(UserMixin, generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing users.

    post:
    Create a new user instance.
    """

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserRegistrationSerializer
        return self.serializer_class

    def get_permissions(self):
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        logger.info(f"Creating new user: '{serializer.validated_data.get('email')}'")
        instance = serializer.save()
        self.create_profile(instance)

    def send_activation_email(self, user):
        serializer = UserActivateSerializer(
            data=user, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        logger.info(f"Sending activation email for user: '{user.email}'")
        serializer.save()

    def create_profile(self, user):
        """Creates user profile when a user is created successfully."""
        logger.info(f"Creating new profile for user: '{user.id}'")
        (user_profile, created) = Profile.objects.get_or_create(user=user)
        logger.info(f"Created new profile for user with '{user.id}': {created}")
        return user_profile


class UserRetrieveDetailView(UserMixin, generics.RetrieveAPIView):
    """
    get:
    Return the details of a user instance.
    """


class UserUpdateView(UserMixin, generics.UpdateAPIView):
    """
    put:
    Update the details of a user instance.
    """

    permission_classes = (
        permissions.IsAuthenticated,
        IsUserOwner,
    )


class UserDestroyView(UserMixin, generics.DestroyAPIView):
    """
    delete:
    Delete a user instance.
    """

    permission_classes = [
        permissions.IsAuthenticated,
        IsUserOwner,
    ]


class AuthorizedUserView(UserMixin, generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsUserOwner,
    ]
    serializer_class = AuthorizedUserSerializer

    def get(self, request, *args, **kwargs):
        self.kwargs["pk"] = request.user.id
        logger.info(f"Get authenticated user: '{request.user.email}'")
        return super().get(request, *args, **kwargs)


class UserActivateView(generics.CreateAPIView):
    permission_classes = (IsUserNotAuthenticated,)
    serializer_class = UserActivateSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"User activation requested for email: '{request.data.get('email')}'"
        )
        super().post(request, *args, **kwargs)
        logger.info(
            f"User activation email sent for email: '{request.data.get('email')}'"
        )

        return Response(
            {"detail": "User activation email has been sent."},
            status=status.HTTP_200_OK,
        )


class UserActivationConfirmView(generics.CreateAPIView):
    permission_classes = (IsUserNotAuthenticated,)
    serializer_class = UserActivationConfirmSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"User activation confirmation requested with token: '{request.data.get('token')}'"
        )
        super().post(request, *args, **kwargs)
        logger.info(f"User account activated with token: '{request.data.get('token')}'")

        return Response(
            {"detail": "Your account has been activated."}, status=status.HTTP_200_OK
        )


class PasswordChangeView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        logger.info(f"Password change requested for user: '{request.user.email}'")
        response = super().post(request, *args, **kwargs)
        logger.info(f"Password change successful for user: '{request.user.email}'")

        return Response(
            {"detail": "New password has been saved."},
            status=status.HTTP_200_OK,
            headers=response.headers,
        )


class PasswordResetView(generics.CreateAPIView):
    permission_classes = (IsUserNotAuthenticated,)
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Password reset requested for email: '{request.data.get('email')}'"
        )
        response = super().post(request, *args, **kwargs)
        logger.info(
            f"Password reset email sent for email: '{request.data.get('email')}'"
        )

        return Response(
            {"detail": "Password reset email has been sent."},
            status=status.HTTP_200_OK,
            headers=response.headers,
        )


class PasswordResetConfirmView(generics.CreateAPIView):
    permission_classes = (IsUserNotAuthenticated,)
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        logger.info(
            f"Password reset confirmation requested with token: '{request.data.get('token')}'"
        )
        response = super().post(request, *args, **kwargs)
        logger.info(
            f"Password reset successful with token: '{request.data.get('token')}'"
        )

        return Response(
            {"detail": "Password has been reset with the new password."},
            status=status.HTTP_200_OK,
            headers=response.headers,
        )
