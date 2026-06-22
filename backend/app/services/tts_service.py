from groq import Groq

from app.config import settings

_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def generate_speech(text: str, voice: str = "austin") -> bytes:
    """
    Converts text to spoken audio using Groq's Orpheus TTS.
    Returns raw WAV audio bytes.
    """
    client = _get_client()

    response = client.audio.speech.create(
        model="canopylabs/orpheus-v1-english",
        voice=voice,
        input=text,
        response_format="wav",
    )

    return response.read()  # raw audio bytes