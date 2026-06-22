from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.company_schema import RetrievalResponse
from app.services.retrieval_service import retrieve_relevant_chunks

router = APIRouter(prefix="/api/v1/company", tags=["company"])


@router.get("/retrieve", response_model=RetrievalResponse)
async def retrieve_context(
    query: str = Query(..., description="Search query, e.g. 'Amazon DSA questions'"),
    company: str | None = Query(None, description="Optional company filter, e.g. 'Amazon'"),
    top_k: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chunks = await retrieve_relevant_chunks(db, query=query, company=company, top_k=top_k)

    return RetrievalResponse(
        query=query,
        company=company,
        results=chunks,
    )