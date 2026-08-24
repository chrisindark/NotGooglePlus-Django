from django.db import models
from solo.models import SingletonModel

from apps.common.models import TimestampedModel


# Create a ReadOnlySerializer to fetch the application details
# if needed on the frontend. Add a single object to the model
# and update the object directly in a management command
class AppConfig(SingletonModel, TimestampedModel):
    # A field to save application version according to semantic versioning
    # Given a version number MAJOR.MINOR.PATCH, increment the:
    # MAJOR version when you make incompatible API changes,
    # MINOR version when you add functionality in a backwards-compatible manner, and
    # PATCH version when you make backwards-compatible bug fixes.
    app_version = models.CharField(max_length=20, default="0.0.1")
    min_supported_version = models.CharField(max_length=20, blank=True)
    force_update = models.BooleanField(default=False)
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True)
    feature_flags = models.JSONField(default=dict, blank=True)
    api_base_url = models.URLField(blank=True)
