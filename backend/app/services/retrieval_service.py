from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge_chunk import KnowledgeChunk
from app.services.embedding_service import generate_embedding


async def retrieve_relevant_chunks(
    db: AsyncSession,
    query: str,
    company: str | None = None,
    top_k: int = 5,
) -> list[KnowledgeChunk]:
    """
    Embeds the query and retrieves the top_k most similar knowledge chunks
    using pgvector's cosine distance operator, optionally filtered by company.
    """
    query_embedding = generate_embedding(query)

    stmt = select(KnowledgeChunk).order_by(
        KnowledgeChunk.embedding.cosine_distance(query_embedding)
    ).limit(top_k)

    if company:
        stmt = stmt.where(KnowledgeChunk.company == company)

    result = await db.execute(stmt)
    return result.scalars().all()