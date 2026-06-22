import uuid

from sqlalchemy import Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("interview_sessions.id"), nullable=False)
    technical: Mapped[float] = mapped_column(Float, nullable=True)
    communication: Mapped[float] = mapped_column(Float, nullable=True)
    problem_solving: Mapped[float] = mapped_column(Float, nullable=True)
    overall: Mapped[float] = mapped_column(Float, nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)