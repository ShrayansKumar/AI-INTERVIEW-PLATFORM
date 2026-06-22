import uuid
from typing import Optional

from pydantic import BaseModel


class StartSessionRequest(BaseModel):
    resume_text: str
    company_name: str = "Amazon"


class StartSessionResponse(BaseModel):
    session_id: uuid.UUID
    first_question: str
    total_questions: int


class SubmitAnswerRequest(BaseModel):
    session_id: uuid.UUID
    answer: str


class SubmitAnswerResponse(BaseModel):
    session_id: uuid.UUID
    next_question: Optional[str]
    interview_complete: bool
    current_question_index: int


class SessionReportResponse(BaseModel):
    session_id: uuid.UUID
    final_report: dict
    evaluations: list
    feedback: dict

class VoiceAnswerResponse(BaseModel):
    session_id: uuid.UUID
    transcript: str
    next_question: Optional[str]
    interview_complete: bool
    current_question_index: int
    next_question_audio_url: Optional[str] = None