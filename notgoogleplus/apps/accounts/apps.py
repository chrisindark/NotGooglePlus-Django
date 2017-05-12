from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'notgoogleplus.apps.accounts'
    label = 'accounts'
    verbose_name = 'Accounts'

    def ready(self):
        import notgoogleplus.apps.accounts.signals
