from django.apps import AppConfig


class FileConfig(AppConfig):
    name = 'apps.files'
    label = 'files'
    verbose_name = 'Files'

    def ready(self):
        import apps.files.signals
        pass
