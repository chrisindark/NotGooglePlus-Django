from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'apps.accounts'
    label = 'accounts'
    verbose_name = 'Accounts'

    def ready(self):
        import apps.accounts.signals
        pass
