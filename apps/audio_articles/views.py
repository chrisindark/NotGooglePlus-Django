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

from apps.audio_articles.models import AudioArticle
from apps.audio_articles.pagination import AudioArticlePagination
from apps.audio_articles.permissions import IsAudioArticleOwner
from apps.audio_articles.serializers import AudioArticleSerializer
from apps.audio_articles.tasks import process_article_synthesis
from apps.articles.models import Article
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)

# Create your views here.
class AudioArticleViewSet(viewsets.ModelViewSet):
    queryset = AudioArticle.objects.all().order_by("-created_at")
    serializer_class = AudioArticleSerializer
    pagination_class = AudioArticlePagination
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [
                permissions.AllowAny(),
            ]
        return [permissions.IsAuthenticated(), IsAudioArticleOwner()]

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

    def create_slug(self, instance: AudioArticle):
        slug = instance.generate_slug(
            title=instance.title,
        )
        if slug == "":
            return
        instance.slug = slug
        instance.save()
        return instance


class TestArticleToAudioView(APIView):
    """
    Test endpoint to trigger the celery audio task.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        article_id = request.data.get("article_id")
        
        if not article_id:
            return Response(
                {"error": "article_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Verify the article exists
            Article.objects.get(id=article_id)
            
            # Trigger Celery task asynchronously
            result = process_article_synthesis.delay(article_id)
            logger.info(f"Celery task added successfully: {result.id}")

            return Response({
                "message": f"Audio synthesis task queued successfully for Article {article_id}.",
                "article_id": article_id,
                "result_id": result.id
            }, status=status.HTTP_202_ACCEPTED)
            
        except Article.DoesNotExist:
            return Response(
                {"error": f"Article with id {article_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
