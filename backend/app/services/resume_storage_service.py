import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume


async def get_user_resume(db: AsyncSession, user_id: uuid.UUID) -> Resume | None:
    result = await db.execute(select(Resume).where(Resume.user_id == user_id))
    return result.scalar_one_or_none()


async def save_user_resume(
    db: AsyncSession,
    user_id: uuid.UUID,
    filename: str,
    cloudinary_url: str,
    extracted_text: str,
    structured_data: dict,
) -> Resume:
    existing = await get_user_resume(db, user_id)

    if existing:
        existing.filename = filename
        existing.cloudinary_url = cloudinary_url
        existing.extracted_text = extracted_text
        existing.structured_data = structured_data
        resume = existing
    else:
        resume = Resume(
            user_id=user_id,
            filename=filename,
            cloudinary_url=cloudinary_url,
            extracted_text=extracted_text,
            structured_data=structured_data,
        )
        db.add(resume)

    await db.commit()
    await db.refresh(resume)
    return resume