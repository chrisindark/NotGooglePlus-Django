"""
URL configuration for notgoogleplus_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from notgoogleplus_django.views import GroupViewSet, api_root

simple_router = routers.SimpleRouter()
simple_router.register(r"api/v1/groups", GroupViewSet, basename="groups")

schema_view = get_schema_view(
    openapi.Info(
        title="Notgoogleplus API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@notgoogleplus.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = (
    [
        path("", api_root, name="api-root"),
        path("", include(simple_router.urls)),
        path("admin/", admin.site.urls),
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        path(
            "swagger.<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
        path(
            "api/spectacular/schema/",
            SpectacularAPIView.as_view(),
            name="spectacular-schema",
        ),
        path(
            "api/spectacular/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="spectacular-swagger-ui",
        ),
        path(
            "api/spectacular/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="spectacular-redoc",
        ),
        path("api/v1/health/", include("apps.health_check.urls")),
        path("api/v1/users/", include("apps.users.urls")),
        path("api/v1/auth/", include("apps.authentication.urls")),
        path("api/v1/core/", include("apps.core.urls")),
        path("api/v1/profiles/", include("apps.profiles.urls")),
        path("api/v1/posts/", include("apps.posts.urls")),
        path("api/v1/tags/", include("apps.tags.urls")),
        path("api/v1/articles/", include("apps.articles.urls")),
        path("api/v1/audio-posts/", include("apps.audio_posts.urls")),
        path("api/v1/audio-articles/", include("apps.audio_articles.urls")),
        path("api/v1/transcriptions/", include("apps.transcriptions.urls")),
        # path("api/v1/evaluations/", include("apps.evaluations.urls")),
        # path('api/v1/', include('apps.files.urls')),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
