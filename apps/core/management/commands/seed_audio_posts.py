import random
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from apps.audio_posts.models import AudioPost
from apps.audio_posts.services import AudioGenerationService
from apps.profiles.models import Profile


class Command(BaseCommand):
    help = (
        "Seeds the database with generated audio posts, uploads audio to storage, "
        "and saves the resulting storage URL in the audio_posts app using gTTS."
    )

    AUDIO_FOLDER = "audio_posts"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of audio posts to create",
        )
        parser.add_argument(
            "--lang",
            type=str,
            default="en",
            help="Language code for gTTS (default: 'en')",
        )
        parser.add_argument(
            "--format",
            type=str,
            choices=["mp3"],
            default="mp3",
            help="Audio output format",
        )
        parser.add_argument(
            "--folder",
            type=str,
            default=self.AUDIO_FOLDER,
            help="Storage folder prefix for uploaded audio files",
        )
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> str | None:
        count = options["count"]
        lang = options.get("lang", "en")
        output_format = options["format"]
        folder_name = options["folder"]

        profiles = list(Profile.objects.all())
        if not profiles:
            self.stdout.write(
                self.style.ERROR("No profiles found. Create profiles first.")
            )
            return

        faker = Faker()
        audio_service = AudioGenerationService()
        created = 0

        for index in range(count):
            profile = random.choice(profiles)
            title = self.create_title(profile, index)
            transcript = self.create_conversation(faker)
            description = self.create_description(profile, transcript)

            self.stdout.write(
                self.style.NOTICE(f"Synthesizing audio for post {index + 1}/{count}")
            )
            audio_url, _ = audio_service.generate_audio(
                text=transcript,
                title=f"post-{index + 1}",
                lang=lang,
                output_format=output_format,
                folder_prefix=folder_name,
            )

            audio_post = AudioPost.objects.create(
                profile=profile,
                title=title,
                description=description,
                audio_file=audio_url,
            )
            audio_post.slug = audio_post.generate_slug(title=title)
            audio_post.save(update_fields=["slug"])

            created += 1
            self.stdout.write(
                self.style.SUCCESS(f"Created AudioPost {audio_post.pk}: {title}")
            )

        self.stdout.write(self.style.SUCCESS(f"Total audio posts created: {created}"))

    def create_title(self, profile: Profile, index: int) -> str:
        persona = profile.first_name or profile.nickname or profile.user.username
        return f"Conversation with {persona} #{index + 1}"

    def create_conversation(self, faker: Faker) -> str:
        speakers = ["Alex", "Jordan", "Taylor", "Morgan", "Sam"]
        lines = random.randint(3, 5)
        topic = random.choice(
            [
                "the latest technology trends",
                "a weekend travel plan",
                "a study summary from a new dataset",
                "a creative project idea",
                "a music recommendation",
            ]
        )
        conversation = [f"Narrator: This conversation is about {topic}."]
        for _ in range(lines):
            speaker = random.choice(speakers)
            text = faker.sentence(nb_words=random.randint(8, 16))
            conversation.append(f"{speaker}: {text}")

        return "\n".join(conversation)

    def create_description(self, profile: Profile, transcript: str) -> str:
        return (
            f"Generated audio conversation for {profile.first_name or profile.nickname or profile.user.username}. "
            f"Transcript:\n{transcript}"
        )

