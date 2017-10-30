from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'notgoogleplus.apps.articles'
    label = 'articles'
    verbose_name = 'Articles'

    def ready(self):
        import notgoogleplus.apps.articles.signals
