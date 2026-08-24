from django.urls import path
from health_check.views import HealthCheckView

urlpatterns = [
    path(
        "",
        HealthCheckView.as_view(
            checks=[
                "health_check.DNS",
                "health_check.Cache",
                "health_check.Database",
                "health_check.Mail",
                "health_check.Storage",
            ]
        ),
        name="health-check",
    ),
]
