import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.session_service import get_session
from app.services.pdf_generator_service import generate_report_pdf
from app.services.memory_service import update_user_memory

router = APIRouter(prefix="/api/v1/report", tags=["report"])


@router.get("/{session_id}/pdf")
async def download_report_pdf(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    db_session = await get_session(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    if db_session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your session")
    if db_session.status != "completed":
        raise HTTPException(status_code=400, detail="Interview not yet completed")

    state = db_session.session_state
    final_report = state.get("final_report", {})
    evaluations = state.get("evaluations", [])

    pdf_bytes = generate_report_pdf(final_report, evaluations)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=interview_report_{session_id}.pdf"},
    )


@router.post("/{session_id}/save-memory")
async def save_to_memory(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Persists this session's evaluation results into the user's long-term memory
    (strong/weak areas), so future interviews can reference accumulated history.
    """
    db_session = await get_session(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    if db_session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your session")
    if db_session.status != "completed":
        raise HTTPException(status_code=400, detail="Interview not yet completed")

    evaluations = db_session.session_state.get("evaluations", [])
    memory = await update_user_memory(db, current_user.id, evaluations)

    return {
        "strong_areas": memory.strong_areas,
        "weak_areas": memory.weak_areas,
    }