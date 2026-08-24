import ast
import csv
import random
from os import path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from apps.articles.models import Article
from apps.profiles.models import Profile
from apps.tags.models import Tag


class Command(BaseCommand):
    help = "Seeds the database with profiles for the articles app/model with random content"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--count", type=int, default=10, help="Number of articles to create"
        )
        parser.add_argument(
            "--offset",
            type=int,
            default=0,
            help="Number of articles to skip from the dataset",
        )
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> str | None:
        count: int = options.get("count", 10)
        offset: int = options.get("offset", 0)
        count = count + offset
        created = 0

        profiles = Profile.objects.all()
        if not profiles:
            self.stdout.write(self.style.ERROR("No profiles found"))
            return

        # Load dataset
        data_file_path = path.join(
            settings.PROJECT_PATH, "apps/core/management/commands/data/articles.csv"
        )

        with open(data_file_path, encoding="utf-8", newline="\n") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row if present
            i = 0
            for row in reader:
                i += 1

                if i <= offset:
                    continue
                # Parse and transform the row data
                title = row[0]  # Adjust indices based on your CSV structure
                content = row[1]
                description = row[2]
                raw_tag = row[5]

                parsed_tags = ast.literal_eval(raw_tag)

                tags = []
                for _ in parsed_tags:
                    tag = Tag.objects.filter(tag=_).exists()
                    if not tag:
                        tag = Tag(tag=_)
                        slug = tag.generate_slug(_)
                        tag.slug = slug
                        tag.save()
                    tags.append(tag)

                profile = self.pick_profile_with_behavior(profiles)
                article = Article(
                    title=title,
                    content=content,
                    description=description,
                    profile=profile,
                )
                slug = article.generate_slug(title)
                article.slug = slug

                article.save()
                article.tags.set(tags)

                created += 1
                if i == count:
                    break
                self.stdout.write(self.style.SUCCESS(f"Created article: {title}"))

        self.stdout.write(self.style.SUCCESS(f"Total articles created: {created}"))

    def pick_profile_with_behavior(self, profiles):
        """
        Simulate:
        - some users post more (power users)
        - others less
        """
        weights = [random.randint(1, 5) for _ in profiles]
        return random.choices(profiles, weights=weights, k=1)[0]
