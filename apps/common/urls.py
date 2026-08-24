from django.urls import path

from . import views

urlpatterns = [
    path("resources/", views.ResourcesView.as_view(), name="resources_view"),
]
