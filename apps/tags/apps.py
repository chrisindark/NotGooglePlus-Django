from django.apps import AppConfig


class TagsConfig(AppConfig):
    name = "apps.tags"
    label = "tags"
    verbose_name = "Tags"

    def ready(self):
        pass
