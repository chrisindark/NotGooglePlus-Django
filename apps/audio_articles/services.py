import logging
from io import BytesIO
from uuid import uuid4

from gtts import gTTS

from apps.audio_articles.constants import (AUDIO_OUTPUT_FORMAT_MP3,
                                           AUDIO_OUTPUT_FORMAT_OGG,
                                           AUDIO_OUTPUT_FORMAT_PCM)
from apps.core.aws_s3_service import AwsS3Service

logger = logging.getLogger(__name__)





import os
import random
import subprocess
import tempfile


class GTtsService:
    default_format = 'mp3'
    def synthesize(self, text: str, lang: str = "en", output_format: str = AUDIO_OUTPUT_FORMAT_MP3, **kwargs) -> bytes:
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=lang)
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except Exception:
            logger.exception("Unexpected error during gTTS synthesis")
            raise

def _pyttsx3_synth_worker(text_to_synth, path_to_save):
    import pyttsx3
    engine = pyttsx3.init()
    engine.save_to_file(text_to_synth, path_to_save)
    engine.runAndWait()

class Pyttsx3Service:
    import sys
    default_format = 'aiff' if sys.platform == 'darwin' else 'wav'
    def synthesize(self, text: str, lang: str = "en", output_format: str = AUDIO_OUTPUT_FORMAT_MP3, **kwargs) -> bytes:
        import multiprocessing

        try:
            with tempfile.NamedTemporaryFile(suffix=f".{self.default_format}", delete=False) as f:
                temp_path = f.name
            try:
                # Use 'spawn' context to ensure a completely fresh process (fixes macOS CoreFoundation issues)
                ctx = multiprocessing.get_context("spawn")
                p = ctx.Process(target=_pyttsx3_synth_worker, args=(text, temp_path))
                p.start()
                p.join()
                
                if p.exitcode != 0:
                    raise RuntimeError(f"pyttsx3 worker process failed with exit code {p.exitcode}")

                with open(temp_path, "rb") as f:
                    return f.read()
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        except Exception:
            logger.exception("Unexpected error during pyttsx3 synthesis")
            raise

class PiperTtsService:
    default_format = 'wav'
    def synthesize(self, text: str, lang: str = "en", output_format: str = AUDIO_OUTPUT_FORMAT_MP3, **kwargs) -> bytes:
        try:
            default_model = "en_US-lessac-medium"
            model_path = kwargs.get("piper_model", os.getenv("PIPER_MODEL_PATH", f"{default_model}.onnx"))
            
            if not os.path.exists(model_path):
                import sys
                logger.info(f"Downloading Piper model {default_model} because {model_path} was not found.")
                # Uses the current python executable (poetry environment)
                subprocess.run([sys.executable, "-m", "piper.download_voices", default_model], check=True)
            with tempfile.NamedTemporaryFile(suffix=f".wav", delete=False) as f:
                temp_path = f.name
            
            try:
                process = subprocess.Popen(
                    ['piper', '-m', model_path, '-f', temp_path],
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                out, err = process.communicate(input=text.encode('utf-8'))
                if process.returncode != 0:
                    err_output = err.decode('utf-8', errors='ignore')
                    # ONNX Runtime on macOS has a known issue where it crashes during process teardown
                    # with a recursive_mutex error (exit code -6). If the file was generated, we can ignore it.
                    if process.returncode == -6 and "recursive_mutex lock failed" in err_output and os.path.getsize(temp_path) > 0:
                        logger.warning("Piper exited with code -6 (known ONNX Runtime teardown issue on macOS), but audio was generated.")
                    else:
                        raise RuntimeError(f"Piper failed with code {process.returncode}: {err_output}")
                
                with open(temp_path, "rb") as f:
                    return f.read()
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        except Exception:
            logger.exception("Unexpected error during piper-tts synthesis")
            raise

def get_random_tts_service():
    services = [
        GTtsService(),
        Pyttsx3Service(),
        PiperTtsService()
    ]
    selected = random.choice(services)
    logger.info(f"Randomly selected TTS service: {selected.__class__.__name__}")
    return selected

class AudioStorageService:
    CONTENT_TYPE_BY_FORMAT = {
        AUDIO_OUTPUT_FORMAT_MP3: "audio/mpeg",
        AUDIO_OUTPUT_FORMAT_OGG: "audio/ogg",
        AUDIO_OUTPUT_FORMAT_PCM: "audio/wav",
    }

    def __init__(self, s3_service: AwsS3Service | None = None):
        self.s3_service = s3_service or AwsS3Service()

    def download_file(self, key: str, download_path: str) -> None:
        """Downloads a file from S3 to the given local path."""
        try:
            return self.s3_service.download_fileobj(key, download_path)
        except Exception:
            logger.exception("Failed to download audio file from S3 for key=%s", key)
            raise

    def upload_bytes(self, audio_bytes: bytes, key: str, output_format: str = AUDIO_OUTPUT_FORMAT_MP3) -> str:
        content_type = self.CONTENT_TYPE_BY_FORMAT.get(
            output_format, "application/octet-stream"
        )
        file_obj = BytesIO(audio_bytes)
        extra_args = {"ContentType": content_type}

        try:
            return self.s3_service.upload_fileobj(file_obj, key, extra_args=extra_args)
        except Exception:
            logger.exception("Failed to upload audio bytes to S3 for key=%s", key)
            raise

    def download_fileobj(self, bucket: str, key: str):
        try:
            return self.s3_service.download_fileobj(bucket, key)
        except Exception:
            logger.exception("Failed to download file from S3 for key=%s", key)
            raise


class AudioGenerationService:
    def __init__(self, tts_service=None, storage_service=None):
        self.tts_service = tts_service or get_random_tts_service()
        self.storage_service = storage_service or AudioStorageService()

    def generate_audio(
        self,
        text: str,
        lang: str = "en",
        **kwargs,
    ) -> tuple[bytes, str]:
        output_format = getattr(self.tts_service, 'default_format', AUDIO_OUTPUT_FORMAT_MP3)
        audio_bytes = self.tts_service.synthesize(
            text, lang=lang, output_format=output_format, **kwargs
        )

        return audio_bytes, output_format

    def upload_to_s3(self, audio_bytes: bytes,
        title: str | None = None,
        output_format: str = AUDIO_OUTPUT_FORMAT_MP3,
        folder_prefix: str = "audio/tts"
    ):
        from django.utils.text import slugify
        safe_title = slugify(title) if title else 'audio'
        file_name = f"{safe_title}-{uuid4()}.{output_format}"
        key = f"{folder_prefix}/{file_name}"

        audio_url = self.storage_service.upload_bytes(
            audio_bytes, key, output_format=output_format
        )

        return audio_url, len(audio_url)