import logging
from uuid import uuid4

from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audio_posts.models import AudioPost
from apps.audio_posts.pagination import AudioPostPagination
from apps.audio_posts.permissions import IsAudioPostOwner
from apps.audio_posts.serializers import AudioPostSerializer
from apps.audio_posts.tasks import process_post_synthesis
from apps.posts.models import Post
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)

# Create your views here.
class AudioPostViewSet(viewsets.ModelViewSet):
    queryset = AudioPost.objects.all().order_by("-created_at")
    serializer_class = AudioPostSerializer
    pagination_class = AudioPostPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [
                permissions.AllowAny(),
            ]
        return [permissions.IsAuthenticated(), IsAudioPostOwner()]

    def get_queryset(self):
        # Set up eager loading to avoid N + 1 selects
        queryset = self.queryset
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)
        serializer.save(profile=profile)
        self.create_slug(serializer.instance)

    def create_slug(self, instance: AudioPost):
        slug = instance.generate_slug(
            title=instance.title,
        )
        if slug == "":
            return
        instance.slug = slug
        instance.save()
        return instance


class TestPostToAudioView(APIView):
    """
    Test endpoint to trigger the celery audio task.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        
        if not post_id:
            return Response(
                {"error": "post_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Verify the post exists
            Post.objects.get(id=post_id)
            
            # Trigger Celery task asynchronously
            result = process_post_synthesis.delay(post_id)
            logger.info(f"Celery task added successfully: {result.id}")

            return Response({
                "message": f"Transcription task queued successfully for Post {post_id}.",
                "post_id": post_id,
                "result_id": result.id
            }, status=status.HTTP_202_ACCEPTED)
            
        except Post.DoesNotExist:
            return Response(
                {"error": f"Post with id {post_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
