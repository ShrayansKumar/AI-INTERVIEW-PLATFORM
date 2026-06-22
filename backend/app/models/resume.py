import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True, unique=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    cloudinary_url: Mapped[str] = mapped_column(String(500), nullable=True)
    extracted_text: Mapped[str] = mapped_column(Text, nullable=False)
    structured_data: Mapped[dict] = mapped_column(JSONB, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())