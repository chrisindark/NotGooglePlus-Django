import os
import random
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from apps.audio_posts.services import TextToSpeechService


class Command(BaseCommand):
    help = "Generates test audio files locally using gTTS without uploading to S3 or creating DB records."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--count",
            type=int,
            default=3,
            help="Number of test audio files to generate",
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
            "--dir",
            type=str,
            default="test_audio_files",
            help="Local directory to save the generated audio files",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        count = options["count"]
        lang = options.get("lang", "en")
        output_format = options["format"]
        directory = options["dir"]

        if not os.path.exists(directory):
            os.makedirs(directory)
            self.stdout.write(self.style.NOTICE(f"Created directory: {directory}"))

        faker = Faker()
        tts_service = TextToSpeechService()

        success_count = 0
        for index in range(count):
            transcript = self.create_conversation(faker)

            self.stdout.write(
                self.style.NOTICE(f"Synthesizing audio file {index + 1}/{count}...")
            )
            try:
                audio_bytes = tts_service.synthesize(transcript, lang=lang)

                filename = f"test_audio_{index + 1}.{output_format}"
                filepath = os.path.join(directory, filename)

                with open(filepath, "wb") as f:
                    f.write(audio_bytes)

                self.stdout.write(self.style.SUCCESS(f"Saved: {filepath}"))
                success_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to synthesize audio: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccess! Generated {success_count} local test files in '{directory}/'."
            )
        )

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


