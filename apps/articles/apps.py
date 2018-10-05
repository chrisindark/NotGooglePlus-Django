from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'apps.articles'
    label = 'articles'
    verbose_name = 'Articles'

    def ready(self):
        import apps.articles.signals
        pass
