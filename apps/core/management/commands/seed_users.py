import random
import string
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from apps.users.models import User


class Command(BaseCommand):
    help = "Seeds the database with users for the users app/model with random email, username and password."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--count", type=int, default=10, help="Number of users to create"
        )
        return super().add_arguments(parser)

    def generate_password(self, length=10):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def handle(self, *args: Any, **options: Any) -> str | None:
        count = options["count"]
        created = 0

        faker_instance = Faker()
        for _ in range(count):
            email = faker_instance.email()
            username = faker_instance.user_name()

            # Generate a strong random password
            password = self.generate_password()

            # Avoid duplicate email
            if User.objects.filter(email=email).exists():
                continue
            # Avoid duplicate username
            if User.objects.filter(username=username).exists():
                continue

            user = User(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.is_active = True
            user.save()

            created += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created user: {username} | {email} | password: {password}"
                )
            )

        self.stdout.write(self.style.SUCCESS(f"Total users created: {created}"))
