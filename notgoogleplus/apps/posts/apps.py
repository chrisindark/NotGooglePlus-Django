from django.apps import AppConfig


class PostConfig(AppConfig):
    name = 'notgoogleplus.apps.posts'
    label = 'posts'
    verbose_name = 'Posts'

    def ready(self):
        import notgoogleplus.apps.posts.signals
