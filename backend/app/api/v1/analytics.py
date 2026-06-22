from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.analytics_service import get_score_trend, get_topic_breakdown

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/score-trend")
async def score_trend(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_score_trend(db, current_user.id)


@router.get("/topic-breakdown")
async def topic_breakdown(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_topic_breakdown(db, current_user.id)