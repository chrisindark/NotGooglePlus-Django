from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'apps.core'
    label = 'core'
    verbose_name = 'Core'

    def ready(self):
        import apps.core.signals
        pass
