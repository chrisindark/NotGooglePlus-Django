from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from notgoogleplus_django.serializers import GroupSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    return Response({})


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
