import random
from contextlib import closing
from typing import Any
from uuid import uuid4

import boto3
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from apps.audio_posts.models import AudioPost
from apps.profiles.models import Profile


class Command(BaseCommand):
    help = (
        "Seeds the database with generated audio posts, uploads audio to storage, "
        "and saves the resulting S3 URL in the audio_posts app."
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
            "--voice",
            type=str,
            default="Joanna",
            help="AWS Polly voice id to use",
        )
        parser.add_argument(
            "--format",
            type=str,
            choices=["mp3", "ogg_vorbis", "pcm"],
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
        voice = options["voice"]
        output_format = options["format"]
        folder_name = options["folder"]

        profiles = list(Profile.objects.all())
        if not profiles:
            self.stdout.write(
                self.style.ERROR("No profiles found. Create profiles first.")
            )
            return

        faker = Faker()
        created = 0

        for index in range(count):
            profile = random.choice(profiles)
            title = self.create_title(profile, index)
            transcript = self.create_conversation(faker)
            description = self.create_description(profile, transcript)

            self.stdout.write(
                self.style.NOTICE(f"Synthesizing audio for post {index + 1}/{count}")
            )
            audio_bytes = self.synthesize_audio(
                transcript, voice=voice, output_format=output_format
            )

            key = f"{folder_name}/{uuid4()}.{output_format}"
            audio_url = self.upload_audio(key, audio_bytes, output_format)

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
                self.style.SUCCESS(f"Created AudioPost {audio_post.id}: {title}")
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

    def synthesize_audio(self, text: str, voice: str, output_format: str) -> bytes:
        polly = boto3.client(
            "polly",
            aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", None),
            aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None),
            region_name=getattr(settings, "AWS_S3_DEFAULT_REGION", None),
        )
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice,
            TextType="text",
        )

        if "AudioStream" not in response:
            raise RuntimeError("Polly did not return audio data")

        with closing(response["AudioStream"]) as stream:
            return stream.read()

    def upload_audio(self, key: str, audio_bytes: bytes, output_format: str) -> str:
        content_type = {
            "mp3": "audio/mpeg",
            "ogg_vorbis": "audio/ogg",
            "pcm": "audio/wav",
        }.get(output_format, "application/octet-stream")

        content = ContentFile(audio_bytes)
        saved_name = default_storage.save(key, content)
        return default_storage.url(saved_name)
