import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_memory import UserMemory


async def get_user_memory(db: AsyncSession, user_id: uuid.UUID) -> UserMemory | None:
    result = await db.execute(select(UserMemory).where(UserMemory.user_id == user_id))
    return result.scalar_one_or_none()


def _extract_topics_from_evaluations(evaluations: list[dict]) -> tuple[list[str], list[str]]:
    """
    Looks at evaluation scores to classify which questions the candidate
    handled well vs. poorly, returning (strong_topics, weak_topics).
    Uses the question text itself as a rough topic label, truncated for readability.
    """
    strong = []
    weak = []

    for ev in evaluations:
        avg = (
            ev.get("technical_accuracy", 0)
            + ev.get("problem_solving", 0)
            + ev.get("depth", 0)
        ) / 3
        question_snippet = ev.get("question", "")[:80]

        if avg >= 7:
            strong.append(question_snippet)
        elif avg <= 4:
            weak.append(question_snippet)

    return strong, weak


async def update_user_memory(
    db: AsyncSession, user_id: uuid.UUID, evaluations: list[dict]
) -> UserMemory:
    """
    Updates (or creates) a user's memory record based on the latest
    interview's evaluations -- merging new strong/weak areas with existing ones.
    """
    strong_new, weak_new = _extract_topics_from_evaluations(evaluations)

    memory = await get_user_memory(db, user_id)

    if memory is None:
        memory = UserMemory(
            user_id=user_id,
            strong_areas=strong_new,
            weak_areas=weak_new,
        )
        db.add(memory)
    else:
        # Merge, keeping the list bounded so it doesn't grow unbounded over many sessions
        existing_strong = memory.strong_areas or []
        existing_weak = memory.weak_areas or []

        memory.strong_areas = list(set(existing_strong + strong_new))[:20]
        memory.weak_areas = list(set(existing_weak + weak_new))[:20]

    await db.commit()
    await db.refresh(memory)
    return memory