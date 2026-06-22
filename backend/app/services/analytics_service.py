import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interview_session import InterviewSession, SessionStatus


async def get_score_trend(db: AsyncSession, user_id: uuid.UUID) -> list[dict]:
    """
    Returns a chronological list of {date, score} for every completed
    session -- feeds a line chart showing improvement over time.
    """
    result = await db.execute(
        select(InterviewSession)
        .where(InterviewSession.user_id == user_id)
        .where(InterviewSession.status == SessionStatus.completed)
        .order_by(InterviewSession.date)
    )
    sessions = result.scalars().all()

    return [
        {"date": s.date.isoformat(), "score": s.score, "session_id": str(s.id)}
        for s in sessions
    ]


async def get_topic_breakdown(db: AsyncSession, user_id: uuid.UUID) -> dict:
    """
    Aggregates average scores per metric (technical, communication, etc.)
    across all completed sessions -- feeds a radar/bar chart.
    """
    result = await db.execute(
        select(InterviewSession)
        .where(InterviewSession.user_id == user_id)
        .where(InterviewSession.status == SessionStatus.completed)
    )
    sessions = result.scalars().all()

    if not sessions:
        return {
            "average_technical_accuracy": 0,
            "average_communication": 0,
            "average_problem_solving": 0,
            "average_depth": 0,
            "total_sessions": 0,
        }

    totals = {"technical_accuracy": 0, "communication": 0, "problem_solving": 0, "depth": 0}
    count = 0

    for s in sessions:
        state = s.session_state or {}
        metrics = state.get("final_report", {}).get("interview_metrics", {})
        if not metrics:
            continue
        totals["technical_accuracy"] += metrics.get("average_technical_accuracy", 0)
        totals["communication"] += metrics.get("average_communication", 0)
        totals["problem_solving"] += metrics.get("average_problem_solving", 0)
        totals["depth"] += metrics.get("average_depth", 0)
        count += 1

    if count == 0:
        count = 1  # avoid division by zero

    return {
        "average_technical_accuracy": round(totals["technical_accuracy"] / count, 2),
        "average_communication": round(totals["communication"] / count, 2),
        "average_problem_solving": round(totals["problem_solving"] / count, 2),
        "average_depth": round(totals["depth"] / count, 2),
        "total_sessions": len(sessions),
    }