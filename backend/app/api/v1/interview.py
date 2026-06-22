import base64
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.interview_session import SessionStatus
from app.agents.graph_builder import interview_graph
from app.agents.interview_agent import interview_agent
from app.agents.evaluation_agent import evaluation_agent
from app.agents.feedback_agent import feedback_agent
from app.agents.report_agent import report_agent
from app.agents.resume_agent import resume_agent
from app.agents.question_agent import question_agent
from app.services.whisper_service import transcribe_audio
from app.services.session_service import delete_session  
from app.services.tts_service import generate_speech
from app.schemas.session_schema import (
    StartSessionRequest,
    StartSessionResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
    SessionReportResponse,
    VoiceAnswerResponse,
)
from app.services.session_service import (
    create_session,
    get_session,
    save_session_state,
    complete_session,
)

router = APIRouter(prefix="/api/v1/interview", tags=["interview"])


# ── Production Routes (text-based) ──────────────────────────────

@router.post("/start", response_model=StartSessionResponse)
async def start_interview(
    payload: StartSessionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_session = await create_session(db, current_user.id)

    state = {
    "resume_text": payload.resume_text,
    "company_name": payload.company_name,
    "user_id": str(current_user.id),  # NEW
    "current_question_index": 0,
    "conversation_history": [],
    "latest_answer": "",
    "followup_count": 0,
    "interview_complete": False,
}

    resume_result = resume_agent(state)
    state.update(resume_result)

    question_result = await question_agent(state)
    state.update(question_result)

    questions = state["questions"]
    first_question = questions[0] if questions else "No questions generated"

    state["next_question"] = first_question

    serializable_state = _make_serializable(state)
    await save_session_state(db, db_session, serializable_state, SessionStatus.in_progress)

    return StartSessionResponse(
        session_id=db_session.id,
        first_question=first_question,
        total_questions=len(questions),
    )


@router.post("/answer", response_model=SubmitAnswerResponse)
async def submit_answer(
    payload: SubmitAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_session = await get_session(db, payload.session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    if db_session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your session")
    if db_session.status == SessionStatus.completed:
        raise HTTPException(status_code=400, detail="Interview already completed")

    state = dict(db_session.session_state)
    state["latest_answer"] = payload.answer

    turn_result = interview_agent(state)
    state.update(turn_result)

    if state.get("interview_complete"):
        eval_result = evaluation_agent(state)
        state.update(eval_result)

        feedback_result = feedback_agent(state)
        state.update(feedback_result)

        report_result = report_agent(state)
        state.update(report_result)

        overall_score = state["final_report"]["interview_metrics"]["overall_score"]
        serializable_state = _make_serializable(state)
        await complete_session(db, db_session, serializable_state, overall_score)
    else:
        serializable_state = _make_serializable(state)
        await save_session_state(db, db_session, serializable_state, SessionStatus.in_progress)

    return SubmitAnswerResponse(
        session_id=payload.session_id,
        next_question=state.get("next_question"),
        interview_complete=state.get("interview_complete", False),
        current_question_index=state.get("current_question_index", 0),
    )


@router.get("/report/{session_id}", response_model=SessionReportResponse)
async def get_report(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_session = await get_session(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    if db_session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your session")
    if db_session.status != SessionStatus.completed:
        raise HTTPException(status_code=400, detail="Interview not yet completed")

    state = db_session.session_state

    return SessionReportResponse(
        session_id=session_id,
        final_report=state.get("final_report", {}),
        evaluations=state.get("evaluations", []),
        feedback=state.get("feedback", {}),
    )


# ── Production Routes (voice-based) ─────────────────────────────

@router.post("/start-voice", response_model=VoiceAnswerResponse)
async def start_interview_voice(
    payload: StartSessionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_session = await create_session(db, current_user.id)

    state = {
    "resume_text": payload.resume_text,
    "company_name": payload.company_name,
    "user_id": str(current_user.id),  # NEW
    "current_question_index": 0,
    "conversation_history": [],
    "latest_answer": "",
    "followup_count": 0,
    "interview_complete": False,
}

    resume_result = resume_agent(state)
    state.update(resume_result)

    question_result = await question_agent(state)
    state.update(question_result)

    questions = state["questions"]
    first_question = questions[0] if questions else "No questions generated"
    state["next_question"] = first_question

    serializable_state = _make_serializable(state)
    await save_session_state(db, db_session, serializable_state, SessionStatus.in_progress)

    audio_bytes_out = generate_speech(first_question, voice="austin")
    audio_b64 = base64.b64encode(audio_bytes_out).decode("utf-8")

    return VoiceAnswerResponse(
        session_id=db_session.id,
        transcript="",
        next_question=first_question,
        interview_complete=False,
        current_question_index=0,
        next_question_audio_url=audio_b64,
    )


@router.post("/answer-voice", response_model=VoiceAnswerResponse)
async def submit_voice_answer(
    session_id: uuid.UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_session = await get_session(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    if db_session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your session")
    if db_session.status == SessionStatus.completed:
        raise HTTPException(status_code=400, detail="Interview already completed")

    audio_bytes = await file.read()
    if len(audio_bytes) < 1000:
        raise HTTPException(status_code=400, detail="Audio file too small or empty")

    transcript = transcribe_audio(audio_bytes, filename=file.filename or "audio.webm")
    if not transcript:
        raise HTTPException(status_code=422, detail="Could not transcribe any speech")

    state = dict(db_session.session_state)
    state["latest_answer"] = transcript

    turn_result = interview_agent(state)
    state.update(turn_result)

    next_question_audio_b64 = None

    if state.get("interview_complete"):
        eval_result = evaluation_agent(state)
        state.update(eval_result)

        feedback_result = feedback_agent(state)
        state.update(feedback_result)

        report_result = report_agent(state)
        state.update(report_result)

        overall_score = state["final_report"]["interview_metrics"]["overall_score"]
        serializable_state = _make_serializable(state)
        await complete_session(db, db_session, serializable_state, overall_score)
    else:
        next_q = state.get("next_question")
        if next_q:
            audio_bytes_out = generate_speech(next_q, voice="austin")
            next_question_audio_b64 = base64.b64encode(audio_bytes_out).decode("utf-8")

        serializable_state = _make_serializable(state)
        await save_session_state(db, db_session, serializable_state, SessionStatus.in_progress)

    return VoiceAnswerResponse(
        session_id=session_id,
        transcript=transcript,
        next_question=state.get("next_question"),
        interview_complete=state.get("interview_complete", False),
        current_question_index=state.get("current_question_index", 0),
        next_question_audio_url=next_question_audio_b64,
    )


# ── Helper ──────────────────────────────────────────────────────

def _make_serializable(state: dict) -> dict:
    import json
    return json.loads(json.dumps(state, default=str))


# ── Test/Debug Routes (kept from earlier days) ──────────────────

class GraphTestRequest(BaseModel):
    resume_text: str
    company_name: str = "Amazon"


class FullInterviewTestRequest(BaseModel):
    resume_text: str
    company_name: str = "Amazon"
    simulated_answers: list[str]


class InterviewTurnRequest(BaseModel):
    questions: list[str]
    current_question_index: int = 0
    conversation_history: list[dict] = []
    latest_answer: str
    followup_count: int = 0


class EvaluationTestRequest(BaseModel):
    conversation_history: list[dict]


@router.post("/test-graph")
async def test_graph(payload: GraphTestRequest, current_user: User = Depends(get_current_user)):
    initial_state = {
        "resume_text": payload.resume_text,
        "company_name": payload.company_name,
        "user_id": str(current_user.id),
    }
    result = await interview_graph.ainvoke(initial_state)
    return result


@router.post("/test-turn")
async def test_turn(payload: InterviewTurnRequest, current_user: User = Depends(get_current_user)):
    state = {
        "questions": payload.questions,
        "current_question_index": payload.current_question_index,
        "conversation_history": payload.conversation_history,
        "latest_answer": payload.latest_answer,
        "followup_count": payload.followup_count,
    }
    result = interview_agent(state)
    return result


@router.post("/test-evaluation")
async def test_evaluation(payload: EvaluationTestRequest, current_user: User = Depends(get_current_user)):
    state = {"conversation_history": payload.conversation_history}
    result = evaluation_agent(state)
    return result


@router.post("/full-test")
async def full_interview_test(
    payload: FullInterviewTestRequest,
    current_user: User = Depends(get_current_user),
):
    state = {
        "resume_text": payload.resume_text,
        "company_name": payload.company_name,
        "current_question_index": 0,
        "conversation_history": [],
        "latest_answer": "",
        "followup_count": 0,
        "interview_complete": False,
    }

    resume_result = resume_agent(state)
    state.update(resume_result)

    question_result = await question_agent(state)
    state.update(question_result)

    questions = state["questions"]

    for i, answer in enumerate(payload.simulated_answers):
        if i >= len(questions):
            break
        state["latest_answer"] = answer
        state["current_question_index"] = i
        state["followup_count"] = 0
        turn_result = interview_agent(state)
        state.update(turn_result)

    state["interview_complete"] = True

    eval_result = evaluation_agent(state)
    state.update(eval_result)

    feedback_result = feedback_agent(state)
    state.update(feedback_result)

    report_result = report_agent(state)
    state.update(report_result)

    return state

@router.delete("/{session_id}")
async def abandon_interview(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Permanently deletes an in-progress interview session, with no save.
    Used when the candidate exits early via the 'quiet exit' button.
    """
    deleted = await delete_session(db, session_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted"}