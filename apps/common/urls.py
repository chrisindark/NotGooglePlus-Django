from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^resources/$', views.ResourcesView.as_view(), name='resources_view'),
]

