from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from apps.profiles.models import Profile
from apps.users.models import User


class Command(BaseCommand):
    help = (
        "Seeds the database with profiles for the profiles app/model with random names"
    )

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--limit", type=int, default=10, help="Number of profiles to create"
        )
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> str | None:
        limit = options["limit"]
        created = 0

        faker_instance = Faker()

        # Get users with a limit provided and check if they have a profile associated else create one
        users = User.objects.filter()[:limit]
        for _ in range(len(users)):
            user = users[_]
            if Profile.objects.filter(user=user).exists():
                continue

            first_name = faker_instance.first_name()
            last_name = faker_instance.last_name()
            Profile.objects.create(
                first_name=first_name, last_name=last_name, user=user
            )

            created += 1

            self.stdout.write(
                self.style.SUCCESS(f"Created profile: {first_name} | {last_name}")
            )

        self.stdout.write(self.style.SUCCESS(f"Total profiles created: {created}"))
