import logging

from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.serializers import JWTSerializer, LoginSerializer

logger = logging.getLogger(__name__)


class LoginView(generics.CreateAPIView):
    """
    Return a token after authenticating the user.
    """

    permission_classes = ()
    serializer_class = LoginSerializer
    # renderer_classes = (CustomJSONRenderer,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        return Response(
            response.data, status=status.HTTP_200_OK, headers=response.headers
        )


class JWTLoginView(generics.CreateAPIView):
    """
    Return a jwt after authenticating the user.
    """

    permission_classes = ()
    serializer_class = JWTSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        return Response(
            response.data, status=status.HTTP_200_OK, headers=response.headers
        )


class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except BaseException:
            logger.info(f"User {request.user} tried to logout but was not logged in.")

        return Response({}, status=status.HTTP_204_NO_CONTENT)
