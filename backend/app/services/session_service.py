import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interview_session import InterviewSession, SessionStatus


async def create_session(db: AsyncSession, user_id: uuid.UUID) -> InterviewSession:
    session = InterviewSession(
        user_id=user_id,
        status=SessionStatus.pending,
        session_state={},
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def get_session(db: AsyncSession, session_id: uuid.UUID) -> InterviewSession | None:
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == session_id)
    )
    return result.scalar_one_or_none()


async def save_session_state(
    db: AsyncSession,
    session: InterviewSession,
    state: dict,
    status: SessionStatus = SessionStatus.in_progress,
) -> InterviewSession:
    session.session_state = state
    session.status = status
    await db.commit()
    await db.refresh(session)
    return session


async def complete_session(
    db: AsyncSession,
    session: InterviewSession,
    state: dict,
    overall_score: float,
) -> InterviewSession:
    session.session_state = state
    session.status = SessionStatus.completed
    session.score = overall_score
    await db.commit()
    await db.refresh(session)
    return session

async def delete_session(db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    session = await get_session(db, session_id)
    if not session or session.user_id != user_id:
        return False

    await db.delete(session)
    await db.commit()
    return True