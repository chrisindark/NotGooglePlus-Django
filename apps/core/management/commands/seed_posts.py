import json
import random
from os import path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from apps.posts.models import Post
from apps.profiles.models import Profile


class Command(BaseCommand):
    help = "Seeds the database with posts for the posts app/model with random content"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--count", type=int, default=10, help="Number of posts to create"
        )
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> str | None:
        count = options["count"]
        created = 0

        profiles = Profile.objects.all()
        if not profiles:
            self.stdout.write(self.style.ERROR("No profiles found"))
            return

        # Topic pool with weights (realistic distribution)
        topics = [
            ("technology", 3),
            ("health", 2),
            ("finance", 2),
            ("travel", 2),
            ("education", 1),
            ("sports", 1),
        ]

        weighted_topics = [topic for topic, weight in topics for _ in range(weight)]
        print(weighted_topics)

        # Load dataset
        data_file_path = path.join(
            settings.PROJECT_PATH, "apps/core/management/commands/data/posts.json"
        )

        with open(data_file_path, encoding="utf-8") as f:
            data: list = json.load(f)

        if count:
            data = data[:count]

        for index in range(len(data)):
            item = data[index]
            profile = self.pick_profile_with_behavior(profiles)
            title = self.generate_title(item)
            content = self.build_content(item)

            title = self.clean_text(title)
            content = self.clean_text(content)

            Post.objects.create(title=title, content=content, profile=profile)
            created += 1

            self.stdout.write(self.style.SUCCESS(f"Created post: {title}"))

        self.stdout.write(self.style.SUCCESS(f"Total posts created: {created}"))

    def pick_profile_with_behavior(self, profiles):
        """
        Simulate:
        - some users post more (power users)
        - others less
        """
        weights = [random.randint(1, 5) for _ in profiles]
        return random.choices(profiles, weights=weights, k=1)[0]

    def generate_title(self, item):
        """Generate a title based on the item."""
        text = item.get("text", "")
        # Take first sentence or fallback
        title = text.split(".")[0]

        if len(title) < 10:
            title = text[:255]

        return title.strip()

    def build_content(self, item):
        """
        Enhance dataset into AI-friendly structure
        """
        text = item.get("text", "")
        tone = item.get("tone", "")
        tags = item.get("tags", [])
        # engagement = item.get("engagement", 0)
        # Expand short content into structured post
        content_parts = []

        # Intro (adds structure for summarization)
        content_parts.append(f"{text}\n")

        # Add contextual enrichment
        if tone:
            content_parts.append(f"\nTone: {tone}.")

        if tags:
            content_parts.append(f"\nTopics: {', '.join(tags)}.")

        # Simulate longer content (important for TTS & summaries)
        expanded = self.expand_text(text)
        content_parts.append("\n\n" + expanded)

        # Optional engagement hint (future ML feature)
        # content_parts.append(f"\n\n[Engagement Score: {engagement}]")

        return "\n".join(content_parts)

    def expand_text(self, text):
        """
        Turn short social posts into longer blog-like content
        """
        expansions = [
            "This highlights an important trend that many people overlook.",
            "In today's fast-changing world, such patterns are becoming more common.",
            "It raises questions about authenticity and originality.",
            "Many professionals are now rethinking their strategies because of this.",
            "Understanding this can help individuals make better decisions.",
        ]
        paragraphs = [text]

        for _ in range(random.randint(1, 1)):
            paragraphs.append(random.choice(expansions))

        return "\n\n".join(paragraphs)

    def clean_text(self, text: str) -> str:
        """
        Fix broken unicode (surrogate pairs) and remove invalid chars
        """
        if not text:
            return ""

        # Fix surrogate pairs by encoding/decoding safely
        return (
            text.encode("utf-16", "surrogatepass")
            .decode("utf-16", "ignore")
            .encode("utf-8", "ignore")
            .decode("utf-8")
        )
