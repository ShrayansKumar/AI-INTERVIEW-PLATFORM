import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.models.knowledge_chunk import KnowledgeChunk
from app.models.user import User
from app.services.embedding_service import generate_embedding


async def list_companies(db: AsyncSession) -> list[Company]:
    result = await db.execute(select(Company))
    return result.scalars().all()


async def create_company(db: AsyncSession, name: str, description: str | None) -> Company:
    company = Company(name=name, description=description)
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company


async def delete_company(db: AsyncSession, company_id: uuid.UUID) -> bool:
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        return False
    await db.delete(company)
    await db.commit()
    return True


async def list_knowledge_chunks(db: AsyncSession, company: str | None = None) -> list[KnowledgeChunk]:
    stmt = select(KnowledgeChunk)
    if company:
        stmt = stmt.where(KnowledgeChunk.company == company)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_knowledge_chunk(
    db: AsyncSession, content: str, source: str, company: str
) -> KnowledgeChunk:
    embedding = generate_embedding(content)
    chunk = KnowledgeChunk(content=content, embedding=embedding, source=source, company=company)
    db.add(chunk)
    await db.commit()
    await db.refresh(chunk)
    return chunk


async def delete_knowledge_chunk(db: AsyncSession, chunk_id: uuid.UUID) -> bool:
    result = await db.execute(select(KnowledgeChunk).where(KnowledgeChunk.id == chunk_id))
    chunk = result.scalar_one_or_none()
    if not chunk:
        return False
    await db.delete(chunk)
    await db.commit()
    return True


async def list_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()