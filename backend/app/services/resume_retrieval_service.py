import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume_chunk import ResumeChunk


async def retrieve_resume_chunks(
    db: AsyncSession, user_id: str, query: str = None, top_k: int = None
) -> list[ResumeChunk]:
    """
    Returns ALL resume chunks for this user, unranked.

    A single resume produces only ~10-15 chunks total, so there's no real
    benefit to similarity-based filtering -- it risks silently dropping
    relevant sections (e.g. an "experience" chunk written in different
    vocabulary than the query) for no real gain. Returning everything
    guarantees the LLM sees the full resume.
    """
    user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id

    stmt = select(ResumeChunk).where(ResumeChunk.user_id == user_uuid)

    result = await db.execute(stmt)
    return result.scalars().all()