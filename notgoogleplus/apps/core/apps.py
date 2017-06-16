from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'notgoogleplus.apps.core'
    label = 'core'
    verbose_name = 'Core'

    def ready(self):
        import notgoogleplus.apps.core.signals
