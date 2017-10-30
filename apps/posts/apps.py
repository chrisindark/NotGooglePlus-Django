from django.apps import AppConfig


class PostConfig(AppConfig):
    name = 'apps.posts'
    label = 'posts'
    verbose_name = 'Posts'

    def ready(self):
        pass
