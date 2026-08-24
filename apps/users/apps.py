from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "apps.users"
    label = "users"
    verbose_name = "Users"

    def ready(self):
        pass
