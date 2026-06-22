def compute_next_difficulty(evaluations: list[dict]) -> str:
    """
    Looks at scores so far and decides whether the next question
    should be easier, harder, or similar difficulty.

    Returns one of: "easier", "similar", "harder"
    """
    if not evaluations:
        return "similar"  # first question, no data yet

    # Average the last 2 evaluations (recent performance matters more than overall)
    recent = evaluations[-2:]

    avg_score = sum(
        (e.get("technical_accuracy", 0) + e.get("problem_solving", 0)) / 2
        for e in recent
    ) / len(recent)

    if avg_score >= 7.5:
        return "harder"
    elif avg_score <= 3.5:
        return "easier"
    else:
        return "similar"


def difficulty_instruction(level: str) -> str:
    """
    Converts a difficulty level into a prompt instruction fragment,
    to be injected into the question generation prompt.
    """
    if level == "harder":
        return "The candidate is performing well. Make this question noticeably more challenging than the previous ones — introduce a harder system design constraint or a deeper technical tradeoff."
    elif level == "easier":
        return "The candidate is struggling. Make this question more approachable — focus on a more fundamental concept or break it into a simpler, more concrete ask."
    else:
        return "Keep this question at a similar difficulty to the previous ones."