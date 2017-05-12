# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    url(r'^$', get_swagger_view(title='swagger')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', include('notgoogleplus.apps.accounts.urls', namespace='accounts')),
    url(r'', include('notgoogleplus.apps.profiles.urls', namespace='profiles')),
    url(r'', include('notgoogleplus.apps.posts.urls', namespace='posts')),
    url(r'', include('notgoogleplus.apps.articles.urls', namespace='articles')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
