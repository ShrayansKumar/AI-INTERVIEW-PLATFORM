import uuid
from datetime import datetime

from sqlalchemy import String, Float, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SessionStatus:
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    score: Mapped[float] = mapped_column(Float, nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    status: Mapped[str] = mapped_column(String(50), default=SessionStatus.pending)
    session_state: Mapped[dict] = mapped_column(JSONB, nullable=True)