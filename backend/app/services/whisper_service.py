import tempfile
import os

from groq import Groq

from app.config import settings

_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def transcribe_audio(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    """
    Transcribes audio bytes to text using Groq's hosted Whisper API
    (whisper-large-v3-turbo — fast and accurate, much better on names/accents
    than running a small local model on CPU).
    """
    client = _get_client()

    # Groq's SDK expects a file-like object with a name attribute
    suffix = "." + filename.split(".")[-1] if "." in filename else ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(filename, audio_file.read()),
                model="whisper-large-v3-turbo",
                language="en",
                response_format="text",
            )
        # response_format="text" returns a plain string directly
        transcript = transcription if isinstance(transcription, str) else transcription.text
        return transcript.strip()
    finally:
        os.unlink(tmp_path)