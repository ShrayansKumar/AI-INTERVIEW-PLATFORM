from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.models.user import User
from app.services.whisper_service import transcribe_audio
from app.services.tts_service import generate_speech

router = APIRouter(prefix="/api/v1/voice", tags=["voice"])


class TranscriptionResponse(BaseModel):
    transcript: str
    word_count: int

class SpeechRequest(BaseModel):
    text: str
    voice: str = "austin"

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """
    Accepts an audio file (webm/wav/mp3) and returns the transcribed text.
    Called by the frontend after the candidate finishes speaking.
    """
    allowed_types = {
        "audio/webm",
        "audio/wav",
        "audio/mp3",
        "audio/mpeg",
        "audio/ogg",
        "audio/x-wav",
        "video/webm",  # Chrome's MediaRecorder often sends webm with video/webm MIME type
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format: {file.content_type}. Use webm, wav, or mp3."
        )

    audio_bytes = await file.read()

    if len(audio_bytes) < 1000:
        raise HTTPException(
            status_code=400,
            detail="Audio file too small — likely empty or silent recording."
        )

    transcript = transcribe_audio(audio_bytes, filename=file.filename or "audio.webm")

    if not transcript:
        raise HTTPException(
            status_code=422,
            detail="Could not transcribe any speech from the audio. Please speak clearly and try again."
        )

    return TranscriptionResponse(
        transcript=transcript,
        word_count=len(transcript.split()),
    )

@router.post("/speak")
async def speak(payload: SpeechRequest, current_user: User = Depends(get_current_user)):
    """
    Converts text (e.g. an interview question) into spoken audio (WAV bytes).
    """
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    audio_bytes = generate_speech(payload.text, voice=payload.voice)

    return Response(content=audio_bytes, media_type="audio/wav")