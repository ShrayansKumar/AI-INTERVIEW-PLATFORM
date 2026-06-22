import uuid

from sqlalchemy import Text, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.db.base import Base


class ResumeChunk(Base):
    __tablename__ = "resume_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    section: Mapped[str] = mapped_column(String(100), nullable=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=False)