from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include
from django.urls import path, re_path
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Notgoogleplus API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
    # path('api/v1/', include('apps.profiles.urls', namespace='profiles')),
    # path('api/v1/', include('apps.posts.urls', namespace='posts')),
    # path('api/v1/', include('apps.articles.urls', namespace='articles')),
    # path('api/v1/', include('apps.files.urls', namespace='files')),
    # path('api/v1/', include('apps.core.urls', namespace='core')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
