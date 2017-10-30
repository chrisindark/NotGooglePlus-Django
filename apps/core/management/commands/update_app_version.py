from django.core.management.base import BaseCommand

from apps.core.models import AppModel


class Command(BaseCommand):
    help = 'Updates version of application in database by providing major, minor and patch boolean flags.'

    def add_arguments(self, parser):
        parser.add_argument('--major', action='store_true', help='flag to increment major count by one')
        parser.add_argument('--minor', action='store_true', help='flag to increment minor count by one')
        parser.add_argument('--patch', action='store_true', help='flag to increment patch count by one')

    def handle(self, *args, **options):
        app_model = AppModel.objects.first()
        if app_model is None:
            app_model = AppModel.objects.create()
        app_model_arr = app_model.app_version.split('.')

        if options['major']:
            app_model_arr[0] = str(int(app_model_arr[0]) + 1)
        if options['minor']:
            app_model_arr[1] = str(int(app_model_arr[1]) + 1)
        if options['patch']:
            app_model_arr[2] = str(int(app_model_arr[2]) + 1)

        app_model_arr = '.'.join(app_model_arr)
        app_model.app_version = app_model_arr
        app_model.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully updated app version to "%s"' % app_model.app_version
        ))
